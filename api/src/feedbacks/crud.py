from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, null

from ..db import get_session
from .entity import FeedbackEntity
from .types import Feedback, FeedbackMeta, FeedbackSpec


router = APIRouter()


def find_feedback_entity(
    namespace_name: str, feedback_name: str, session: Session
) -> FeedbackEntity:
    statement = select(FeedbackEntity)
    statement = statement.where(FeedbackEntity.namespace == namespace_name)
    statement = statement.where(FeedbackEntity.name == feedback_name)
    statement = statement.where(FeedbackEntity.deletedTimestamp == null())
    return session.exec(statement).one()


def serialize(entity: FeedbackEntity) -> Feedback:
    return Feedback(
        meta=FeedbackMeta(**entity.model_dump()),
        spec=FeedbackSpec(**entity.model_dump()),
    )


@router.post("")
def create_feedback(
    namespace_name: str, newFeedback: Feedback, session: Session = Depends(get_session)
) -> Feedback:
    entity = FeedbackEntity()
    if newFeedback.meta:
        entity.sqlmodel_update(newFeedback.meta.model_dump(exclude_unset=True))
    if newFeedback.spec:
        entity.sqlmodel_update(newFeedback.spec.model_dump(exclude_unset=True))
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.get("/{feedback_id}")
def read_feedback(
    namespace_name: str, feedback_name: str, session: Session = Depends(get_session)
) -> Feedback:
    entity = find_feedback_entity(namespace_name, feedback_name, session)
    return serialize(entity)


@router.put("/{feedback_id}")
def update_feedback(
    namespace_name: str,
    feedback_name: str,
    updateFeedback: Feedback,
    session: Session = Depends(get_session),
) -> Feedback:
    entity = find_feedback_entity(namespace_name, feedback_name, session)
    if updateFeedback.meta:
        entity.sqlmodel_update(updateFeedback.meta.model_dump(exclude_unset=True))
    if updateFeedback.spec:
        entity.sqlmodel_update(updateFeedback.spec.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.delete("/{feedback_id}")
def delete_feedback(
    namespace_name: str, feedback_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    entity = find_feedback_entity(namespace_name, feedback_name, session)

    softDelete = entity.labels and entity.labels.get("soft-delete") == "true"

    if softDelete:
        entity.deletedTimestamp = datetime.now()
        entity.annotations = {}
        session.add(entity)
        session.commit()
    else:
        session.delete(entity)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Feedback deleted"}
    )
