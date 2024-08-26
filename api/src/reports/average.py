from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel, select, func
from typing import Iterable, Dict, Optional

from ..db import get_session
from ..feedbacks.entity import FeedbackEntity
from ..items.entity import ItemEntity


router = APIRouter()


class MinMax(SQLModel):
    count: int
    min: str | None
    max: str | None
    # avg: str


class ItemMinMax(SQLModel):
    uid: uuid.UUID
    namespace_name: str
    name: str
    creationTimestamp: datetime
    updatedTimestamp: Optional[datetime]
    labels: Dict[str, str]
    annotations: Dict[str, str]
    count: int
    min: str | None
    max: str | None
    # avg: str


@router.get("/minmax")
def get_minmax(
    namespace_name: str,
    session: Session = Depends(get_session),
) -> MinMax:
    statement = select(  # type: ignore
        func.count(FeedbackEntity.uid).label("count"),  # type: ignore
        func.min(FeedbackEntity.value).label("min"),
        func.max(FeedbackEntity.value).label("max"),
        # func.avg(Feedback.value).label('avg'),
    ).select_from(FeedbackEntity)

    statement = statement.where(FeedbackEntity.namespace == namespace_name)

    return session.exec(statement).one()  # type: ignore


@router.get("/item/{item_name}")
def get_item_minmax(
    namespace_name: str,
    item_name: str,
    session: Session = Depends(get_session),
) -> MinMax:
    statement = select(  # type: ignore
        func.count(FeedbackEntity.uid).label("count"),  # type: ignore
        func.min(FeedbackEntity.value).label("min"),
        func.max(FeedbackEntity.value).label("max"),
        # func.avg(FeedbackEntity.value).label('avg'),
    ).select_from(FeedbackEntity)

    statement = statement.where(FeedbackEntity.namespace == namespace_name)

    statement = statement.where(FeedbackEntity.name == item_name)

    return session.exec(statement).one()  # type: ignore


@router.get("/items")
def get_all_items_minmax(
    namespace_name: str | None = None,
    session: Session = Depends(get_session),
) -> Iterable[ItemMinMax]:
    statement = (
        select(  # type: ignore
            ItemEntity.uid,
            ItemEntity.namespace,
            ItemEntity.name,
            ItemEntity.creationTimestamp,
            ItemEntity.updatedTimestamp,
            ItemEntity.labels,
            ItemEntity.annotations,
            func.count(FeedbackEntity.uid).label("count"),  # type: ignore
            func.min(FeedbackEntity.value).label("min"),
            func.max(FeedbackEntity.value).label("max"),
            # func.avg(FeedbackEntity.value).label('avg'),
        )
        .select_from(FeedbackEntity)
        .group_by(FeedbackEntity.item)
    )

    statement = statement.where(FeedbackEntity.namespace == namespace_name)

    return session.exec(statement).all()  # type: ignore
