import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict
from .db import get_session
from .projects import Project
from .users import User


class Event(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    project_name: str = Field(foreign_key="project.name")
    project: Project = Relationship()
    user_name: str = Field(foreign_key="user.name")
    user: User = Relationship()
    name: str = Field()
    features: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_event(newEvent: Event, session: Session = Depends(get_session)) -> Event:
    event = Event()
    event.name = newEvent.name
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
