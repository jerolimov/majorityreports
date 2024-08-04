import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, desc
from sqlalchemy import Column, DateTime, func
from typing import Iterable, Dict, Optional
from .db import get_session


class Namespace(SQLModel, table=True):
    uid: uuid.UUID = Field(unique=True, default_factory=uuid.uuid4)
    name: str = Field(primary_key=True)
    creationTimestamp: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updateTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)


class NamespacesResult(SQLModel):
    count: int | None = None # fix types
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

    result = NamespacesResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result


@router.get("/latest")
def read_latest_namespaces(
    limit: int = 10, session: Session = Depends(get_session)
) -> Iterable[Namespace]:
    statement = select(Namespace)
    statement = statement.order_by(desc(Namespace.creationTimestamp))
    statement = statement.limit(limit)
    return session.exec(statement).all()


@router.get("/{namespace_name}")
def read_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> Namespace:
    statement = select(Namespace)
    statement = statement.where(Namespace.name == namespace_name)
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
    # or how can we run a delete query directly?
    namespace = read_namespace(namespace_name)
    session.delete(namespace)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Namespace deleted"}
    )
