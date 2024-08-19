from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Session,
    select,
    null,
)

from ..db import get_session
from .entity import ItemEntity
from .types import Item, ItemMeta, ItemSpec


router = APIRouter()


def find_item_entity(
    namespace_name: str, item_name: str, session: Session
) -> ItemEntity:
    statement = select(ItemEntity)
    statement = statement.where(ItemEntity.namespace == namespace_name)
    statement = statement.where(ItemEntity.name == item_name)
    statement = statement.where(ItemEntity.deletedTimestamp == null())
    return session.exec(statement).one()


def serialize(entity: ItemEntity) -> Item:
    return Item(
        meta=ItemMeta(**entity.model_dump()),
        spec=ItemSpec(**entity.model_dump()),
    )


@router.post("")
def create_item(
    namespace_name: str, newItem: Item, session: Session = Depends(get_session)
) -> Item:
    entity = ItemEntity()
    if newItem.meta:
        entity.sqlmodel_update(newItem.meta.model_dump(exclude_unset=True))
    if newItem.spec:
        entity.sqlmodel_update(newItem.spec.model_dump(exclude_unset=True))
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.get("/{item_name}")
def read_item(
    namespace_name: str, item_name: str, session: Session = Depends(get_session)
) -> Item:
    entity = find_item_entity(namespace_name, item_name, session)
    return serialize(entity)


@router.put("/{item_name}")
def update_item(
    namespace_name: str,
    item_name: str,
    updateItem: Item,
    session: Session = Depends(get_session),
) -> Item:
    entity = find_item_entity(namespace_name, item_name, session)
    if updateItem.meta:
        entity.sqlmodel_update(updateItem.meta.model_dump(exclude_unset=True))
    if updateItem.spec:
        entity.sqlmodel_update(updateItem.spec.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(entity)
    return serialize(entity)


@router.delete("/{item_name}")
def delete_item(
    namespace_name: str, item_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    entity = find_item_entity(namespace_name, item_name, session)

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
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Item deleted"}
    )
