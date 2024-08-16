from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from sqlalchemy import func
from typing import Iterable
from ..db import get_session
from ..db.namespace import Namespace


class NamespacesResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Namespace] | None = None


router = APIRouter()


@router.post("")
def create_namespace(
    newNamespace: Namespace, session: Session = Depends(get_session)
) -> Namespace:
    namespace = Namespace()
    namespace.name = newNamespace.name
    namespace.labels = newNamespace.labels
    namespace.annotations = newNamespace.annotations
    session.add(namespace)
    session.commit()
    session.refresh(namespace)
    return namespace


@router.get("")
def read_namespaces(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> NamespacesResult:
    countSelect = select(func.count("*")).select_from(Namespace)
    itemsSelect = select(Namespace).offset(offset).limit(limit)

    countSelect = countSelect.where(Namespace.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Namespace.deletedTimestamp == null())

    result = NamespacesResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result


@router.get("/{namespace_name}")
def read_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> Namespace:
    statement = select(Namespace)
    statement = statement.where(Namespace.name == namespace_name)
    statement = statement.where(Namespace.deletedTimestamp == null())
    return session.exec(statement).one()


@router.put("/{namespace_name}")
def update_namespace(
    namespace_name: str,
    updateNamespace: Namespace,
    session: Session = Depends(get_session),
) -> Namespace:
    namespace = read_namespace(namespace_name)
    if name := updateNamespace.name:
        namespace.name = name
    if labels := updateNamespace.labels:
        namespace.labels = labels
    if annotations := updateNamespace.annotations:
        namespace.annotations = annotations
    session.commit()
    session.refresh(namespace)
    return namespace


@router.delete("/{namespace_name}")
def delete_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    namespace = read_namespace(namespace_name, session)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        namespace.deletedTimestamp = datetime.now()
        namespace.annotations = {}
        session.add(namespace)
        session.commit()
    else:
        session.delete(namespace)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Namespace deleted"}
    )
