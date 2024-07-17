from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


router = APIRouter()


@router.post("")
def create_event(newEvent: Event, session: Session = Depends(get_session)) -> Event:
    event = Event()
    event.name = newEvent.name
    if isinstance(newEvent.done, bool):
        event.done = newEvent.done
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
    if done := updateEvent.done:
        event.done = done
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
