from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, null

from ..db import get_session
from .entity import ActorEntity
from .types import Actor, ActorMeta, ActorSpec


router = APIRouter()


def find_actor_entity(
    namespace_name: str, actor_name: str, session: Session
) -> ActorEntity:
    statement = select(ActorEntity)
    statement = statement.where(ActorEntity.namespace == namespace_name)
    statement = statement.where(ActorEntity.name == actor_name)
    statement = statement.where(ActorEntity.deletedTimestamp == null())
    return session.exec(statement).one()


def serialize(entity: ActorEntity) -> Actor:
    return Actor(
        meta=ActorMeta(**entity.model_dump()),
        spec=ActorSpec(**entity.model_dump()),
    )


@router.post("")
def create_actor(
    namespace_name: str, newActor: Actor, session: Session = Depends(get_session)
) -> Actor:
    entity = ActorEntity()
    if newActor.meta:
        entity.sqlmodel_update(newActor.meta.model_dump(exclude_unset=True))
    if newActor.spec:
        entity.sqlmodel_update(newActor.spec.model_dump(exclude_unset=True))
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.get("/{actor_name}")
def read_actor(
    namespace_name: str, actor_name: str, session: Session = Depends(get_session)
) -> Actor:
    entity = find_actor_entity(namespace_name, actor_name, session)
    return serialize(entity)


@router.put("/{actor_name}")
def update_actor(
    namespace_name: str,
    actor_name: str,
    updateActor: Actor,
    session: Session = Depends(get_session),
) -> Actor:
    entity = find_actor_entity(namespace_name, actor_name, session)
    if updateActor.meta:
        entity.sqlmodel_update(updateActor.meta.model_dump(exclude_unset=True))
    if updateActor.spec:
        entity.sqlmodel_update(updateActor.spec.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.delete("/{actor_name}")
def delete_actor(
    namespace_name: str, actor_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    entity = find_actor_entity(namespace_name, actor_name, session)

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
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Actor deleted"}
    )
