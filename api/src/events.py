import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict, Optional
from .db import get_session
from .namespaces import Namespace
from .actor import Actor


class Event(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    actor_name: Optional[str] = Field(foreign_key="actor.name")
    actor: Optional[Actor] = Relationship()
    name: Optional[str] = Field(nullable=True)
    type: Optional[str] = Field(nullable=True)
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)
    value: Optional[str] = Field(nullable=True)


router = APIRouter()


@router.post("")
def create_event(newEvent: Event, session: Session = Depends(get_session)) -> Event:
    event = Event()
    event.name = newEvent.name
    event.type = newEvent.type
    event.labels = newEvent.labels
    event.annotations = newEvent.annotations
    event.value = newEvent.value
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("")
def get_events(session: Session = Depends(get_session)) -> Iterable[Event]:
    statement = select(Event)
    return session.exec(statement).all()


@router.get("/{event_id}")
def get_event_by_event_id(
    event_id: int, session: Session = Depends(get_session)
) -> Event:
    event = session.get_one(Event, event_id)
    return event


@router.put("/{event_id}")
def update_event_by_event_id(
    event_id: int, updateEvent: Event, session: Session = Depends(get_session)
) -> Event:
    event = session.get_one(Event, event_id)
    if name := updateEvent.name:
        event.name = name
    if type := updateEvent.type:
        event.type = type
    if labels := updateEvent.labels:
        event.labels = labels
    if annotations := updateEvent.annotations:
        event.annotations = annotations
    if value := updateEvent.value:
        event.value = value
    session.commit()
    session.refresh(event)
    return event


@router.delete("/{event_id}")
def delete_event_by_event_id(
    event_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    event = session.get_one(Event, event_id)
    session.delete(event)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Event deleted"}
    )
