import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace
from .actor import Actor


class Feedback(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    actor_name: str = Field(foreign_key="actor.name")
    actor: Actor = Relationship()
    name: Optional[str] = Field(nullable=True)
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    value: int


router = APIRouter()


@router.post("")
def create_feedback(
    newFeedback: Feedback, session: Session = Depends(get_session)
) -> Feedback:
    feedback = Feedback()
    feedback.name = newFeedback.name
    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


@router.get("")
def get_feedbacks(session: Session = Depends(get_session)) -> Iterable[Feedback]:
    statement = select(Feedback)
    return session.exec(statement).all()


@router.get("/{feedback_id}")
def get_feedback_by_feedback_id(
    feedback_id: int, session: Session = Depends(get_session)
) -> Feedback:
    feedback = session.get_one(Feedback, feedback_id)
    return feedback


@router.put("/{feedback_id}")
def update_feedback_by_feedback_id(
    feedback_id: int, updateFeedback: Feedback, session: Session = Depends(get_session)
) -> Feedback:
    feedback = session.get_one(Feedback, feedback_id)
    if name := updateFeedback.name:
        feedback.name = name
    session.commit()
    session.refresh(feedback)
    return feedback


@router.delete("/{feedback_id}")
def delete_feedback_by_feedback_id(
    feedback_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    feedback = session.get_one(Feedback, feedback_id)
    session.delete(feedback)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Feedback deleted"}
    )
