from fastapi import APIRouter, Depends
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from sqlalchemy import func
from typing import Iterable

from ..db import get_session
from .entity import FeedbackEntity as Feedback


class FeedbacksResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Feedback] | None = None


router = APIRouter()


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
