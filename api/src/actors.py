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
    desc,
    null,
)
from sqlalchemy import Column, DateTime, func
from typing import Iterable, Dict, Optional
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


@router.get("")
def read_actors(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> ActorsResult:
    countSelect = select(func.count("*")).select_from(Actor)
    itemsSelect = select(Actor).offset(offset).limit(limit)

    if namespace_name is not None:
        countSelect = countSelect.where(Actor.namespace_name == namespace_name)
        itemsSelect = itemsSelect.where(Actor.namespace_name == namespace_name)

    countSelect = countSelect.where(Actor.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Actor.deletedTimestamp == null())

    result = ActorsResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result


@router.get("/latest")
def read_latest_actors(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[Actor]:
    statement = select(Actor)
    if namespace_name is not None:
        statement = statement.where(Actor.namespace_name == namespace_name)
    statement = statement.where(Actor.deletedTimestamp == null())
    statement = statement.order_by(desc(Actor.creationTimestamp))
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()


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
