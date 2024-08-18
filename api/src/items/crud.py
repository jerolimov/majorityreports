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
from .entity import ItemEntity as Item


class ItemsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Item] | None = None


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


@router.get("/{item_name}")
def read_item(
    namespace_name: str, item_name: str, session: Session = Depends(get_session)
) -> Item:
    statement = select(Item)
    statement = statement.where(Item.namespace_name == namespace_name)
    statement = statement.where(Item.name == item_name)
    statement = statement.where(Item.deletedTimestamp == null())
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
    namespace = read_namespace(namespace_name)
    item = read_item(namespace_name, item_name)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        item.deletedTimestamp = datetime.now()
        item.annotations = {}
        session.add(item)
        session.commit()
    else:
        session.delete(item)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Item deleted"}
    )
