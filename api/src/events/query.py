from fastapi import APIRouter, Depends
from sqlmodel import Session, select, null, not_, col
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy import func, desc
from typing import TypeVar

from ..db import get_session
from ..shared.types import ListMeta, Pagination
from .entity import EventEntity
from .types import EventList, EventQuery
from .crud import serialize


router = APIRouter()


T = TypeVar("T")


def apply_query(
    sql: SelectOfScalar[T],
    query: EventQuery,
    count: bool = False,
) -> SelectOfScalar[T]:
    # sql = select(Event)

    if filter := query.filter:
        if filter.label_selector:
            sql = sql.where(EventEntity.labels == filter.label_selector)
        if filter.names:
            sql = sql.where(col(EventEntity.name).in_(filter.names))

    if exclude := query.exclude:
        if exclude.label_selector:
            sql = sql.where(not_(EventEntity.labels == exclude.label_selector))
        if exclude.names:
            sql = sql.where(not_(col(EventEntity.name).in_(exclude.names)))

    sql = sql.where(EventEntity.deletedTimestamp == null())

    if not count:
        if order := query.order:
            for order_by in order:
                if order_by.direction == "DESC":
                    sql = sql.order_by(desc(order_by.attribute))
                else:
                    sql = sql.order_by(order_by.attribute)

        if pagination := query.pagination:
            sql = sql.offset(pagination.start)
            sql = sql.limit(pagination.limit)

    return sql


@router.get("", response_model_exclude_none=True)
def read_items(
    start: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> EventList:
    # convert all http query parameters to a EventQuery
    # filter.label_selector=...    or label_selector=...
    # exclude.label_selector=...   or label_selector!=...
    # order=name DESC
    # order=name DESC
    # start=
    # limit=
    query = EventQuery(
        filter=None,
        exclude=None,
        order=None,
        pagination=Pagination(
            start=start,
            limit=limit,
        ),
    )

    return query_items(query, session)


@router.post("/query", response_model_exclude_none=True)
def query_items(
    query: EventQuery, session: Session = Depends(get_session)
) -> EventList:
    countSelect = select(func.count("*")).select_from(EventEntity)
    itemsSelect = select(EventEntity)

    countSelect = apply_query(countSelect, query, count=True)
    itemsSelect = apply_query(itemsSelect, query)

    start = query.pagination.start if query.pagination and query.pagination.start else 0
    limit = (
        query.pagination.limit if query.pagination and query.pagination.limit else 10
    )
    itemCount = session.exec(countSelect).one()
    remainingItemCount = max(itemCount - start - limit, 0)

    entities = session.exec(itemsSelect).all()

    return EventList(
        meta=ListMeta(
            start=start,
            limit=limit,
            itemCount=itemCount,
            remainingItemCount=remainingItemCount,
        ),
        items=list(map(serialize, entities)),
    )
