from fastapi import APIRouter, Depends
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from sqlalchemy import func
from typing import Iterable

from ..db import get_session
from .entity import ItemEntity as Item


class ItemsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Item] | None = None


router = APIRouter()


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
