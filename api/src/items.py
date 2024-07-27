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


class Item(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "namespace_name", "name", name="item_name_is_unique_in_namespace"
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
def create_item(
    namespace_name: str, newItem: Item, session: Session = Depends(get_session)
) -> Item:
    item = Item()
    item.namespace = read_namespace(namespace_name)
    item.name = newItem.name
    item.labels = newItem.labels
    item.annotations = newItem.annotations
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("")
def read_items(
    namespace_name: str | None = None, session: Session = Depends(get_session)
) -> Iterable[Item]:
    statement = select(Item)
    if namespace_name is not None:
        statement = statement.where(Item.namespace_name == namespace_name)
    return session.exec(statement).all()


@router.get("/{item_name}")
def read_item(
    namespace_name: str, item_name: str, session: Session = Depends(get_session)
) -> Item:
    statement = select(Item)
    statement = statement.where(Item.namespace_name == namespace_name)
    statement = statement.where(Item.name == item_name)
    return session.exec(statement).one()


@router.put("/{item_name}")
def update_item(
    namespace_name: str,
    item_name: str,
    updateItem: Item,
    session: Session = Depends(get_session),
) -> Item:
    item = read_item(namespace_name, item_name)
    if name := updateItem.name:
        item.name = name
    if labels := updateItem.labels:
        item.labels = labels
    if annotations := updateItem.annotations:
        item.annotations = annotations
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_name}")
def delete_item(
    namespace_name: str, item_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    item = read_item(namespace_name, item_name)
    session.delete(item)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Item deleted"}
    )
