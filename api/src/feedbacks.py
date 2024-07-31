from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship, desc
from sqlalchemy import Column, DateTime, func
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace, read_namespace
from .actors import Actor
from .items import Item


class Feedback(SQLModel, table=True):
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
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    type: Optional[str] = Field(nullable=True)
    value: str = Field()


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
    namespace_name: str | None = None, session: Session = Depends(get_session)
) -> Iterable[Feedback]:
    statement = select(Feedback)
    if namespace_name is not None:
        statement = statement.where(Actor.namespace_name == namespace_name)
    return session.exec(statement).all()


@router.get("/latest")
def read_latest_feedbacks(
    namespace_name: str | None = None,
    type_filter: str | None = None,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[Feedback]:
    statement = select(Feedback)
    if namespace_name is not None:
        statement = statement.where(Actor.namespace_name == namespace_name)
    if type_filter is not None:
        statement = statement.where(Feedback.type == type_filter)
    statement = statement.order_by(desc(Feedback.creationTimestamp))
    statement = statement.limit(limit)
    return session.exec(statement).all()


@router.get("/{feedback_id}")
def read_feedback(
    namespace_name: str, feedback_name: str, session: Session = Depends(get_session)
) -> Feedback:
    statement = select(Feedback)
    statement = statement.where(Feedback.namespace_name == namespace_name)
    statement = statement.where(Feedback.name == feedback_name)
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
    # or how can we run a delete query directly?
    feedback = read_feedback(namespace_name, feedback_name)
    session.delete(feedback)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Feedback deleted"}
    )
