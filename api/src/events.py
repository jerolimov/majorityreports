from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Field,
    SQLModel,
    UniqueConstraint,
    Session,
    select,
    JSON,
    Relationship,
    null,
)
from sqlalchemy import Column, DateTime, func
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace, read_namespace
from .actors import Actor
from .items import Item


class Event(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "namespace_name", "name", name="event_name_is_unique_in_namespace"
        ),
    )

    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    name: str = Field()
    actor_name: Optional[str] = Field(foreign_key="actor.name")
    actor: Optional[Actor] = Relationship()
    item_name: Optional[str] = Field(foreign_key="item.name")
    item: Optional[Item] = Relationship()
    creationTimestamp: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updateTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    deletedTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    type: Optional[str] = Field(nullable=True)
    value: Optional[str] = Field(nullable=True)
    # count: int = Field(default=0) ???


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
