import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Field,
    SQLModel,
    Session,
    select,
    JSON,
    Relationship,
    UniqueConstraint,
)
from typing import Iterable, Dict
from .db import get_session
from .namespaces import Namespace, read_namespace


class Actor(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "namespace_name", "name", name="actor_name_is_unique_in_namespace"
        ),
    )

    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    name: str = Field()
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)


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


@router.get("")
def read_actors(
    namespace_name: str | None = None, session: Session = Depends(get_session)
) -> Iterable[Actor]:
    statement = select(Actor)
    if namespace_name is not None:
        statement = statement.where(Actor.namespace_name == namespace_name)
    return session.exec(statement).all()


@router.get("/{actor_name}")
def read_actor(
    namespace_name: str, actor_name: str, session: Session = Depends(get_session)
) -> Actor:
    statement = select(Actor)
    statement = statement.where(Actor.namespace_name == namespace_name)
    statement = statement.where(Actor.name == actor_name)
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
    # or how can we run a delete query directly?
    actor = read_actor(namespace_name, actor_name)
    session.delete(actor)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Actor deleted"}
    )