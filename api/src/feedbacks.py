from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Field,
    SQLModel,
    UniqueConstraint,
    Session,
    select,
    JSON,
    Relationship,
    null,
)
from sqlalchemy import Column, DateTime, func
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace, read_namespace
from .actors import Actor
from .items import Item


class Feedback(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "namespace_name", "name", name="feedback_name_is_unique_in_namespace"
        ),
    )

    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    name: str = Field()
    actor_name: str = Field(foreign_key="actor.name")
    actor: Actor = Relationship()
    item_name: str = Field(foreign_key="item.name")
    item: Item = Relationship()
    creationTimestamp: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updateTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    deletedTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    type: Optional[str] = Field(nullable=True)
    value: str = Field()


class FeedbacksResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Feedback] | None = None


router = APIRouter()


@router.post("")
def create_feedback(
    namespace_name: str, newFeedback: Feedback, session: Session = Depends(get_session)
) -> Feedback:
    feedback = Feedback()
    feedback.namespace = read_namespace(namespace_name)
    feedback.name = newFeedback.name
    feedback.type = newFeedback.type
    feedback.labels = newFeedback.labels
    feedback.annotations = newFeedback.annotations
    feedback.value = newFeedback.value
    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


@router.get("")
def read_feedbacks(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> FeedbacksResult:
    countSelect = select(func.count("*")).select_from(Feedback)
    itemsSelect = select(Feedback).offset(offset).limit(limit)

    if namespace_name is not None:
        countSelect = countSelect.where(Feedback.namespace_name == namespace_name)
        itemsSelect = itemsSelect.where(Feedback.namespace_name == namespace_name)

    countSelect = countSelect.where(Feedback.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Feedback.deletedTimestamp == null())

    result = FeedbacksResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result


@router.get("/{feedback_id}")
def read_feedback(
    namespace_name: str, feedback_name: str, session: Session = Depends(get_session)
) -> Feedback:
    statement = select(Feedback)
    statement = statement.where(Feedback.namespace_name == namespace_name)
    statement = statement.where(Feedback.name == feedback_name)
    statement = statement.where(Feedback.deletedTimestamp == null())
    return session.exec(statement).one()


@router.put("/{feedback_id}")
def update_feedback(
    namespace_name: str,
    feedback_name: str,
    updateFeedback: Feedback,
    session: Session = Depends(get_session),
) -> Feedback:
    feedback = read_feedback(namespace_name, feedback_name)
    if name := updateFeedback.name:
        feedback.name = name
    if type := updateFeedback.type:
        feedback.type = type
    if labels := updateFeedback.labels:
        feedback.labels = labels
    if annotations := updateFeedback.annotations:
        feedback.annotations = annotations
    if value := updateFeedback.value:
        feedback.value = value
    session.commit()
    session.refresh(feedback)
    return feedback


@router.delete("/{feedback_id}")
def delete_feedback(
    namespace_name: str, feedback_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    namespace = read_namespace(namespace_name)
    feedback = read_feedback(namespace_name, feedback_name)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        feedback.deletedTimestamp = datetime.now()
        feedback.annotations = {}
        session.add(feedback)
        session.commit()
    else:
        session.delete(feedback)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Feedback deleted"}
    )
