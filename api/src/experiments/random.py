from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import Iterable

from ..db import get_session
from ..items import Item


router = APIRouter()


@router.get("/item")
def get_random_item(session: Session = Depends(get_session)) -> Item:
    statement = select(Item).order_by(func.random()).limit(1)
    return session.exec(statement).one()


@router.get("/items")
def get_random_items(limit: int = 10, session: Session = Depends(get_session)) -> Iterable[Item]:
    statement = select(Item).order_by(func.random()).limit(limit)
    return session.exec(statement).all()

