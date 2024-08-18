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
from .entity import EventEntity as Event


class EventsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Event] | None = None


router = APIRouter()


@router.get("")
def read_events(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> EventsResult:
    countSelect = select(func.count("*")).select_from(Event)
    itemsSelect = select(Event).offset(offset).limit(limit)

    if namespace_name is not None:
        countSelect = countSelect.where(Event.namespace_name == namespace_name)
        itemsSelect = itemsSelect.where(Event.namespace_name == namespace_name)

    countSelect = countSelect.where(Event.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Event.deletedTimestamp == null())

    result = EventsResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result
