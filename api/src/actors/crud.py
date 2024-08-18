from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from typing import Iterable

from ..db import get_session
from ..namespaces.crud import read_namespace
from .entity import ActorEntity as Actor


class ActorsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Actor] | None = None


router = APIRouter()


@router.post("")
def create_actor(
    namespace_name: str, newActor: Actor, session: Session = Depends(get_session)
) -> Actor:
    actor = Actor()
    actor.namespace = read_namespace(namespace_name)
    actor.name = newActor.name
    actor.labels = newActor.labels
    actor.annotations = newActor.annotations
    session.add(actor)
    session.commit()
    session.refresh(actor)
    return actor


@router.get("/{actor_name}")
def read_actor(
    namespace_name: str, actor_name: str, session: Session = Depends(get_session)
) -> Actor:
    statement = select(Actor)
    statement = statement.where(Actor.namespace_name == namespace_name)
    statement = statement.where(Actor.name == actor_name)
    statement = statement.where(Actor.deletedTimestamp == null())
    return session.exec(statement).one()


@router.put("/{actor_name}")
def update_actor(
    namespace_name: str,
    actor_name: str,
    updateActor: Actor,
    session: Session = Depends(get_session),
) -> Actor:
    actor = read_actor(namespace_name, actor_name)
    if name := updateActor.name:
        actor.name = name
    if labels := updateActor.labels:
        actor.labels = labels
    if annotations := updateActor.annotations:
        actor.annotations = annotations
    session.commit()
    session.refresh(actor)
    return actor


@router.delete("/{actor_name}")
def delete_actor(
    namespace_name: str, actor_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    namespace = read_namespace(namespace_name)
    actor = read_actor(namespace_name, actor_name)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        actor.deletedTimestamp = datetime.now()
        actor.annotations = {}
        session.add(actor)
        session.commit()
    else:
        session.delete(actor)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Actor deleted"}
    )
