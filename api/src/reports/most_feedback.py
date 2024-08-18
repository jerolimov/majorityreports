from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, func, and_, desc
from sqlmodel.sql.expression import Select
from typing import Iterable, Dict, Optional, cast

from ..db import get_session
from ..items.entity import ItemEntity as Item
from ..feedbacks.entity import FeedbackEntity as Feedback


router = APIRouter()


class ItemWithFeedbackCount(SQLModel):
    uid: uuid.UUID
    namespace_name: str
    name: str
    creationTimestamp: datetime
    updateTimestamp: Optional[datetime]
    labels: Dict[str, str]
    annotations: Dict[str, str]
    count: int


@router.get("/items")
def get_items_with_most_feedback(
    namespace_name: str | None = None,
    type_filter: str | None = None,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[ItemWithFeedbackCount]:
    statement = cast(
        Select[ItemWithFeedbackCount],
        select(  # type: ignore
            Item.uid,
            Item.namespace_name,
            Item.name,
            Item.creationTimestamp,
            Item.updateTimestamp,
            Item.labels,
            Item.annotations,
        )
        .select_from(Item)
        .add_columns(func.count(Feedback.name).label("count")),  # type: ignore
    )

    statement = statement.join(
        Feedback,
        and_(
            Item.name == Feedback.item_name,
            Item.namespace_name == Feedback.namespace_name,
        ),
        isouter=True,
    )
    statement = statement.group_by(Item.uid)  # type: ignore
    statement = statement.order_by(desc("count"))

    if namespace_name is not None:
        statement = statement.where(Item.namespace_name == namespace_name)

    if type_filter is not None:
        statement = statement.where(Feedback.type == type_filter)

    statement = statement.limit(limit)

    return session.exec(statement).all()
