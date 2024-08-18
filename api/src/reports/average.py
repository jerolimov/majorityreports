from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel, select, func
from typing import Iterable, Dict, Optional

from ..db import get_session
from ..feedbacks.entity import FeedbackEntity as Feedback
from ..items.entity import ItemEntity as Item


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
    updateTimestamp: Optional[datetime]
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
        func.count(Feedback.uid).label("count"),  # type: ignore
        func.min(Feedback.value).label("min"),
        func.max(Feedback.value).label("max"),
        # func.avg(Feedback.value).label('avg'),
    ).select_from(Feedback)

    statement = statement.where(Feedback.namespace_name == namespace_name)

    return session.exec(statement).one()  # type: ignore


@router.get("/item/{item_name}")
def get_item_minmax(
    namespace_name: str,
    item_name: str,
    session: Session = Depends(get_session),
) -> MinMax:
    statement = select(  # type: ignore
        func.count(Feedback.uid).label("count"),  # type: ignore
        func.min(Feedback.value).label("min"),
        func.max(Feedback.value).label("max"),
        # func.avg(Feedback.value).label('avg'),
    ).select_from(Feedback)

    statement = statement.where(Feedback.namespace_name == namespace_name)

    statement = statement.where(Feedback.name == item_name)

    return session.exec(statement).one()  # type: ignore


@router.get("/items")
def get_all_items_minmax(
    namespace_name: str | None = None,
    session: Session = Depends(get_session),
) -> Iterable[ItemMinMax]:
    statement = (
        select(  # type: ignore
            Item.uid,
            Item.namespace_name,
            Item.name,
            Item.creationTimestamp,
            Item.updateTimestamp,
            Item.labels,
            Item.annotations,
            func.count(Feedback.uid).label("count"),  # type: ignore
            func.min(Feedback.value).label("min"),
            func.max(Feedback.value).label("max"),
            # func.avg(Feedback.value).label('avg'),
        )
        .select_from(Feedback)
        .group_by(Feedback.item_name)
    )

    statement = statement.where(Feedback.namespace_name == namespace_name)

    return session.exec(statement).all()  # type: ignore
