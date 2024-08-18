from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import Iterable

from ..db import get_session
from ..items.entity import ItemEntity as Item


router = APIRouter()


@router.get("/item")
def get_random_item(
    namespace_name: str | None = None, session: Session = Depends(get_session)
) -> Item:
    statement = select(Item)
    if namespace_name is not None:
        statement = statement.where(Item.namespace_name == namespace_name)
    statement = statement.order_by(func.random())
    statement = statement.limit(1)
    return session.exec(statement).one()


@router.get("/items")
def get_random_items(
    namespace_name: str | None = None,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> Iterable[Item]:
    statement = select(Item)
    if namespace_name is not None:
        statement = statement.where(Item.namespace_name == namespace_name)
    statement = statement.order_by(func.random())
    statement = statement.limit(limit)
    return session.exec(statement).all()
