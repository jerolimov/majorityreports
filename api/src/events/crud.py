from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, null

from ..db import get_session
from .entity import EventEntity
from .types import Event, EventMeta, EventSpec


router = APIRouter()


def find_event_entity(
    namespace_name: str, item_name: str, session: Session
) -> EventEntity:
    statement = select(EventEntity)
    statement = statement.where(EventEntity.namespace == namespace_name)
    statement = statement.where(EventEntity.name == item_name)
    statement = statement.where(EventEntity.deletedTimestamp == null())
    return session.exec(statement).one()


def serialize(entity: EventEntity) -> Event:
    return Event(
        meta=EventMeta(**entity.model_dump()),
        spec=EventSpec(**entity.model_dump()),
    )


@router.post("")
def create_event(
    namespace_name: str,
    newEvent: Event,
    session: Session = Depends(get_session),
) -> Event:
    entity = EventEntity()
    if newEvent.meta:
        entity.sqlmodel_update(newEvent.meta.model_dump(exclude_unset=True))
    if newEvent.spec:
        entity.sqlmodel_update(newEvent.spec.model_dump(exclude_unset=True))
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.get("/{event_name}")
def read_event(
    namespace_name: str, event_name: str, session: Session = Depends(get_session)
) -> Event:
    entity = find_event_entity(namespace_name, event_name, session)
    return serialize(entity)


@router.put("/{event_name}")
def update_event(
    namespace_name: str,
    event_name: str,
    updateEvent: Event,
    session: Session = Depends(get_session),
) -> Event:
    entity = find_event_entity(namespace_name, event_name, session)
    if updateEvent.meta:
        entity.sqlmodel_update(updateEvent.meta.model_dump(exclude_unset=True))
    if updateEvent.spec:
        entity.sqlmodel_update(updateEvent.spec.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.delete("/{event_name}")
def delete_event(
    namespace_name: str,
    event_name: str,
    session: Session = Depends(get_session),
) -> JSONResponse:
    entity = find_event_entity(namespace_name, event_name, session)

    softDelete = entity.labels and entity.labels.get("soft-delete") == "true"

    if softDelete:
        entity.deletedTimestamp = datetime.now()
        entity.annotations = {}
        session.add(entity)
        session.commit()
    else:
        session.delete(entity)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Event deleted"}
    )
