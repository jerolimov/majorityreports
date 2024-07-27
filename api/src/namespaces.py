import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON
from typing import Iterable, Dict
from .db import get_session


class Namespace(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(unique=True)
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_namespace(
    newNamespace: Namespace, session: Session = Depends(get_session)
) -> Namespace:
    namespace = Namespace()
    namespace.name = newNamespace.name
    session.add(namespace)
    session.commit()
    session.refresh(namespace)
    return namespace


@router.get("")
def get_namespaces(session: Session = Depends(get_session)) -> Iterable[Namespace]:
    statement = select(Namespace)
    return session.exec(statement).all()


@router.get("/{namespace_id}")
def get_namespace_by_namespace_id(
    namespace_id: int, session: Session = Depends(get_session)
) -> Namespace:
    namespace = session.get_one(Namespace, namespace_id)
    return namespace


@router.put("/{namespace_id}")
def update_namespace_by_namespace_id(
    namespace_id: int, updateNamespace: Namespace, session: Session = Depends(get_session)
) -> Namespace:
    namespace = session.get_one(Namespace, namespace_id)
    if name := updateNamespace.name:
        namespace.name = name
    session.commit()
    session.refresh(namespace)
    return namespace


@router.delete("/{namespace_id}")
def delete_namespace_by_namespace_id(
    namespace_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    namespace = session.get_one(Namespace, namespace_id)
    session.delete(namespace)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Namespace deleted"}
    )
