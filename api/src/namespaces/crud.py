from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Session,
    select,
    null,
)

from ..db import get_session
from .entity import NamespaceEntity
from .types import Namespace, NamespaceMeta, NamespaceSpec


router = APIRouter()


def find_namespace_entity(namespace_name: str, session: Session) -> NamespaceEntity:
    statement = select(NamespaceEntity)
    statement = statement.where(NamespaceEntity.name == namespace_name)
    statement = statement.where(NamespaceEntity.deletedTimestamp == null())
    return session.exec(statement).one()


def serialize(entity: NamespaceEntity) -> Namespace:
    return Namespace(
        meta=NamespaceMeta(**entity.model_dump()),
        spec=NamespaceSpec(**entity.model_dump()),
    )


@router.post("")
def create_namespace(
    newNamespace: Namespace, session: Session = Depends(get_session)
) -> Namespace:
    entity = NamespaceEntity()
    if newNamespace.meta:
        entity.sqlmodel_update(newNamespace.meta.model_dump(exclude_unset=True))
    if newNamespace.spec:
        entity.sqlmodel_update(newNamespace.spec.model_dump(exclude_unset=True))
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return newNamespace


@router.get("/{namespace_name}")
def read_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> Namespace:
    entity = find_namespace_entity(namespace_name, session)
    return serialize(entity)


@router.put("/{namespace_name}")
def update_namespace(
    namespace_name: str,
    updateNamespace: Namespace,
    session: Session = Depends(get_session),
) -> Namespace:
    entity = find_namespace_entity(namespace_name, session)
    if updateNamespace.meta:
        entity.sqlmodel_update(updateNamespace.meta.model_dump(exclude_unset=True))
    if updateNamespace.spec:
        entity.sqlmodel_update(updateNamespace.spec.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.delete("/{namespace_name}")
def delete_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    entity = find_namespace_entity(namespace_name, session)

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
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Namespace deleted"}
    )
