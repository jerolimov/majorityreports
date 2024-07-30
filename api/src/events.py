import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace, read_namespace
from .actors import Actor
from .items import Item


class Event(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    name: str = Field()
    actor_name: Optional[str] = Field(foreign_key="actor.name")
    actor: Optional[Actor] = Relationship()
    item_name: Optional[str] = Field(foreign_key="item.name")
    item: Optional[Item] = Relationship()
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    type: Optional[str] = Field(nullable=True)
    value: Optional[str] = Field(nullable=True)
    # count: int = Field(default=0) ???


router = APIRouter()


@router.post("")
def create_event(
    namespace_name: str, newEvent: Event, session: Session = Depends(get_session)
) -> Event:
    event = Event()
    event.namespace = read_namespace(namespace_name)
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
    namespace_name: str | None = None, session: Session = Depends(get_session)
) -> Iterable[Event]:
    statement = select(Event)
    if namespace_name is not None:
        statement = statement.where(Actor.namespace_name == namespace_name)
    return session.exec(statement).all()


@router.get("/{event_name}")
def read_event(
    namespace_name: str, event_name: str, session: Session = Depends(get_session)
) -> Event:
    statement = select(Event)
    statement = statement.where(Event.namespace_name == namespace_name)
    statement = statement.where(Event.name == event_name)
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
    namespace_name: str, event_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    event = read_event(namespace_name, event_name)
    session.delete(event)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Event deleted"}
    )
