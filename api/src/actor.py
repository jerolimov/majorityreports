import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship, UniqueConstraint
from typing import Iterable, Dict
from .db import get_session
from .namespaces import Namespace


class Actor(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("namespace_name", "name", name="actor_name_is_unique_in_namespace"),
    )

    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: Namespace = Relationship()
    name: str = Field()
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_actor(newActor: Actor, session: Session = Depends(get_session)) -> Actor:
    actor = Actor()
    actor.name = newActor.name
    session.add(actor)
    session.commit()
    session.refresh(actor)
    return actor


@router.get("")
def get_actors(session: Session = Depends(get_session)) -> Iterable[Actor]:
    statement = select(Actor)
    return session.exec(statement).all()


@router.get("/{actor_id}")
def get_actor_by_actor_id(actor_id: int, session: Session = Depends(get_session)) -> Actor:
    actor = session.get_one(Actor, actor_id)
    return actor


@router.put("/{actor_id}")
def update_actor_by_actor_id(
    actor_id: int, updateActor: Actor, session: Session = Depends(get_session)
) -> Actor:
    actor = session.get_one(Actor, actor_id)
    if name := updateActor.name:
        actor.name = name
    session.commit()
    session.refresh(actor)
    return actor


@router.delete("/{actor_id}")
def delete_actor_by_actor_id(
    actor_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    actor = session.get_one(Actor, actor_id)
    session.delete(actor)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Actor deleted"}
    )
