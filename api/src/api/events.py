from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from sqlalchemy import func
from typing import Iterable
from ..db import get_session
from ..db.event import Event
from .namespaces import read_namespace


class EventsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Event] | None = None


router = APIRouter()


@router.post("")
def create_event(
    namespace_name: str,
    newEvent: Event,
    session: Session = Depends(get_session),
) -> Event:
    event = Event()
    event.namespace = read_namespace(namespace_name, session)
    event.name = newEvent.name
    event.actor = newEvent.actor
    event.labels = newEvent.labels
    event.annotations = newEvent.annotations
    event.type = newEvent.type
    event.value = newEvent.value
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


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


@router.get("/{event_name}")
def read_event(
    namespace_name: str, event_name: str, session: Session = Depends(get_session)
) -> Event:
    statement = select(Event)
    statement = statement.where(Event.namespace_name == namespace_name)
    statement = statement.where(Event.name == event_name)
    statement = statement.where(Event.deletedTimestamp == null())
    return session.exec(statement).one()


@router.put("/{event_name}")
def update_event(
    namespace_name: str,
    event_name: str,
    updateEvent: Event,
    session: Session = Depends(get_session),
) -> Event:
    event = read_event(namespace_name, event_name)
    if name := updateEvent.name:
        event.name = name
    if actor := updateEvent.actor:
        event.actor = actor
    if labels := updateEvent.labels:
        event.labels = labels
    if annotations := updateEvent.annotations:
        event.annotations = annotations
    if type := updateEvent.type:
        event.type = type
    if value := updateEvent.value:
        event.value = value
    session.commit()
    session.refresh(event)
    return event


@router.delete("/{event_name}")
def delete_event(
    namespace_name: str,
    event_name: str,
    session: Session = Depends(get_session),
) -> JSONResponse:
    namespace = read_namespace(namespace_name, session)
    event = read_event(namespace_name, event_name, session)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        event.deletedTimestamp = datetime.now()
        event.annotations = {}
        session.add(event)
        session.commit()
    else:
        session.delete(event)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Event deleted"}
    )
