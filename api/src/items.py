import uuid
from datetime import datetime
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


@router.get("")
def read_items(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> ItemsResult:
    countSelect = select(func.count("*")).select_from(Item)
    itemsSelect = select(Item).offset(offset).limit(limit)

    if namespace_name is not None:
        countSelect = countSelect.where(Item.namespace_name == namespace_name)
        itemsSelect = itemsSelect.where(Item.namespace_name == namespace_name)

    countSelect = countSelect.where(Item.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Item.deletedTimestamp == null())

    result = ItemsResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result


@router.get("/latest")
def read_latest_items(
    namespace_name: str | None = None,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[Item]:
    statement = select(Item)
    if namespace_name is not None:
        statement = statement.where(Item.namespace_name == namespace_name)
    statement = statement.where(Item.deletedTimestamp == null())
    statement = statement.order_by(desc(Item.creationTimestamp))
    statement = statement.limit(limit)
    return session.exec(statement).all()


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
