from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, and_, desc, null
from sqlmodel.sql.expression import Select
from typing import Iterable, Dict, Optional, cast

from ..db import get_session
from ..items.entity import ItemEntity
from ..events.entity import EventEntity


router = APIRouter()


class ItemWithEventDetails(SQLModel):
    uid: uuid.UUID
    namespace_name: str
    name: str
    creationTimestamp: datetime
    updatedTimestamp: Optional[datetime]
    labels: Dict[str, str]
    annotations: Dict[str, str]

    eventUid: uuid.UUID
    eventName: str
    eventActor: Optional[str]
    eventCreated: Optional[datetime]
    eventUpdated: Optional[datetime]
    eventLabels: Dict[str, str]
    eventAnnotations: Dict[str, str]
    eventType: Optional[str]
    eventValue: Optional[str]


@router.get("/items")
def get_items_with_latest_events(
    namespace_name: str | None = None,
    actor_filter: str | None = None,
    type_filter: str | None = None,
    unique_items: bool = True,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[ItemWithEventDetails]:
    statement = cast(
        Select[ItemWithEventDetails],
        select(  # type: ignore
            ItemEntity.uid,
            ItemEntity.namespace,
            ItemEntity.name,
            ItemEntity.creationTimestamp,
            ItemEntity.updatedTimestamp,
            ItemEntity.labels,
            ItemEntity.annotations,
            EventEntity.uid.label("eventUid"),  # type: ignore
            EventEntity.name.label("eventName"),  # type: ignore
            EventEntity.actor.label("eventActor"),  # type: ignore
            EventEntity.creationTimestamp.label("eventCreated"),  # type: ignore
            EventEntity.updatedTimestamp.label("eventUpdated"),  # type: ignore
            EventEntity.labels.label("eventLabels"),  # type: ignore
            EventEntity.annotations.label("eventAnnotations"),  # type: ignore
            EventEntity.type.label("eventType"),  # type: ignore
            EventEntity.value.label("eventValue"),  # type: ignore
        )
        .select_from(EventEntity)
        .where(EventEntity.item != null())
        .join(
            ItemEntity,
            and_(
                EventEntity.item == ItemEntity.name,
                EventEntity.namespace == ItemEntity.namespace,
            ),
        ),
    )

    if namespace_name is not None:
        statement = statement.where(EventEntity.namespace == namespace_name)

    if actor_filter is not None:
        statement = statement.where(EventEntity.actor == actor_filter)

    if type_filter is not None:
        statement = statement.where(EventEntity.type == type_filter)

    if unique_items:
        statement = statement.group_by(ItemEntity.uid)  # type: ignore

    statement = statement.order_by(desc(EventEntity.creationTimestamp))

    statement = statement.limit(limit)

    return session.exec(statement).all()
