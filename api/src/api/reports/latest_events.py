from datetime import datetime
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, and_, desc, null
from sqlmodel.sql.expression import Select
from typing import Iterable, Dict, Optional, cast

from ...db import get_session
from ..items import Item
from ..events import Event


router = APIRouter()


class ItemWithEventDetails(SQLModel):
    uid: uuid.UUID
    namespace_name: str
    name: str
    creationTimestamp: datetime
    updateTimestamp: Optional[datetime]
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
            Item.uid,
            Item.namespace_name,
            Item.name,
            Item.creationTimestamp,
            Item.updateTimestamp,
            Item.labels,
            Item.annotations,
            Event.uid.label("eventUid"),  # type: ignore
            Event.name.label("eventName"),  # type: ignore
            Event.actor_name.label("eventActor"),  # type: ignore
            Event.creationTimestamp.label("eventCreated"),  # type: ignore
            Event.updateTimestamp.label("eventUpdated"),  # type: ignore
            Event.labels.label("eventLabels"),  # type: ignore
            Event.annotations.label("eventAnnotations"),  # type: ignore
            Event.type.label("eventType"),  # type: ignore
            Event.value.label("eventValue"),  # type: ignore
        )
        .select_from(Event)
        .where(Event.item != null())
        .join(
            Item,
            and_(
                Event.item_name == Item.name,
                Event.namespace_name == Item.namespace_name,
            ),
        ),
    )

    if namespace_name is not None:
        statement = statement.where(Event.namespace_name == namespace_name)

    if actor_filter is not None:
        statement = statement.where(Event.actor_name == actor_filter)

    if type_filter is not None:
        statement = statement.where(Event.type == type_filter)

    if unique_items:
        statement = statement.group_by(Item.uid)  # type: ignore

    statement = statement.order_by(desc(Event.creationTimestamp))

    statement = statement.limit(limit)

    return session.exec(statement).all()
