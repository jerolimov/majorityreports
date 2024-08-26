from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, func, and_, desc
from sqlmodel.sql.expression import Select
from typing import Iterable, Dict, Optional, cast

from ..db import get_session
from ..items.entity import ItemEntity
from ..events.entity import EventEntity


router = APIRouter()


class ItemWithEventCount(SQLModel):
    uid: uuid.UUID
    namespace_name: str
    name: str
    creationTimestamp: datetime
    updatedTimestamp: Optional[datetime]
    labels: Dict[str, str]
    annotations: Dict[str, str]
    count: int


@router.get("/items")
def get_items_with_most_events(
    namespace_name: str | None = None,
    type_filter: str | None = None,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[ItemWithEventCount]:
    statement = cast(
        Select[ItemWithEventCount],
        select(  # type: ignore
            ItemEntity.uid,
            ItemEntity.namespace,
            ItemEntity.name,
            ItemEntity.creationTimestamp,
            ItemEntity.updatedTimestamp,
            ItemEntity.labels,
            ItemEntity.annotations,
        )
        .select_from(ItemEntity)
        .add_columns(func.count(EventEntity.name).label("count")),  # type: ignore
    )

    statement = statement.join(
        EventEntity,
        and_(
            ItemEntity.name == EventEntity.item,
            ItemEntity.namespace == EventEntity.namespace,
        ),
        isouter=True,
    )
    statement = statement.group_by(ItemEntity.uid)  # type: ignore
    statement = statement.order_by(desc("count"))

    if namespace_name is not None:
        statement = statement.where(ItemEntity.namespace == namespace_name)

    if type_filter is not None:
        statement = statement.where(EventEntity.type == type_filter)

    statement = statement.limit(limit)

    return session.exec(statement).all()
