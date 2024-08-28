from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, text, select, func, null, col
from sqlalchemy.engine import Row
from typing import Dict, List, Iterable

from ..db import get_session
from .entity import ItemEntity

router = APIRouter()


class Item(SQLModel):
    value: str
    count: int


class ItemTagsResult(SQLModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ItemTagsResult"
    items: List[Item]


@router.get("/tags/generic")
def get_tags_generic(session: Session = Depends(get_session)) -> ItemTagsResult:
    statement = select(ItemEntity)

    rows = session.exec(statement).all()
    dict: Dict[str, Item] = {}

    for row in rows:
        if tags := row.tags:
            for tag in tags:
                if tag in dict:
                    dict[tag].count += 1
                else:
                    dict[tag] = Item(value=tag, count=1)

    items = list(dict.values())
    items.sort(key=lambda item: item.count, reverse=True)
    return ItemTagsResult(items=items)


@router.get("/tags/generic2")
def get_tags_generic2(session: Session = Depends(get_session)) -> ItemTagsResult:
    statement = (
        select(ItemEntity.tags).select_from(ItemEntity).where(ItemEntity.tags != null())
    )

    rows = session.exec(statement).all()
    dict: Dict[str, Item] = {}

    for row in rows:
        if tags := row:
            for tag in tags:
                if tag in dict:
                    dict[tag].count += 1
                else:
                    dict[tag] = Item(value=tag, count=1)

    items = list(dict.values())
    items.sort(key=lambda item: item.count, reverse=True)
    return ItemTagsResult(items=items)


@router.get("/tags/generic3")
def get_tags_generic3(session: Session = Depends(get_session)) -> ItemTagsResult:
    statement = (
        select(ItemEntity.tags, func.count("*"))
        .select_from(ItemEntity)
        .group_by(col(ItemEntity.tags))
        .where(ItemEntity.tags != null())
    )

    rows = session.exec(statement).all()
    dict: Dict[str, Item] = {}

    for row in rows:
        tags, count = row
        if tags:
            for tag in tags:
                if tag in dict:
                    dict[tag].count += count
                else:
                    dict[tag] = Item(value=tag, count=count)

    items = list(dict.values())
    items.sort(key=lambda item: item.count, reverse=True)
    return ItemTagsResult(items=items)


@router.get("/tags/sqlite")
def get_tags_sqlite(session: Session = Depends(get_session)) -> ItemTagsResult:
    statement = text(
        "select j.value as value, count(*) as count from item, json_each(item.tags) j group by j.value order by count desc"
    )

    rows: Iterable[Row] = session.exec(statement).all()  # type: ignore

    items = map(lambda row: row._asdict(), rows)

    return ItemTagsResult(items=items)
