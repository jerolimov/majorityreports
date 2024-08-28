from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, text, select, func, null, col
from sqlalchemy.engine import Row
from typing import Dict, List, Iterable

from ..db import get_session
from .entity import NamespaceEntity

router = APIRouter()


class Item(SQLModel):
    value: str
    count: int


class NamespaceTagsResult(SQLModel):
    apiVersion: str = "v1alpha1"
    kind: str = "NamespaceTagsResult"
    items: List[Item]


@router.get("/tags/generic")
def get_tags_generic(session: Session = Depends(get_session)) -> NamespaceTagsResult:
    statement = select(NamespaceEntity)

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
    return NamespaceTagsResult(items=items)


@router.get("/tags/generic2")
def get_tags_generic2(session: Session = Depends(get_session)) -> NamespaceTagsResult:
    statement = (
        select(NamespaceEntity.tags)
        .select_from(NamespaceEntity)
        .where(NamespaceEntity.tags != null())
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
    return NamespaceTagsResult(items=items)


@router.get("/tags/generic3")
def get_tags_generic3(session: Session = Depends(get_session)) -> NamespaceTagsResult:
    statement = (
        select(NamespaceEntity.tags, func.count("*"))
        .select_from(NamespaceEntity)
        .group_by(col(NamespaceEntity.tags))
        .where(NamespaceEntity.tags != null())
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
    return NamespaceTagsResult(items=items)


@router.get("/tags/sqlite")
def get_tags_sqlite(session: Session = Depends(get_session)) -> NamespaceTagsResult:
    statement = text(
        "select j.value as value, count(*) as count from namespace, json_each(namespace.tags) j group by j.value order by count desc"
    )

    rows: Iterable[Row] = session.exec(statement).all()  # type: ignore

    items = map(lambda row: row._asdict(), rows)

    return NamespaceTagsResult(items=items)
