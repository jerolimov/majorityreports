from fastapi import APIRouter, Depends
from sqlmodel import Session, select, null, not_, col
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy import func, desc
from typing import TypeVar

from ..db import get_session
from ..shared.types import ListMeta, Pagination
from .entity import ActorEntity
from .types import ActorList, ActorQuery
from .crud import serialize


router = APIRouter()


T = TypeVar("T")


def apply_query(
    sql: SelectOfScalar[T],
    query: ActorQuery,
    count: bool = False,
) -> SelectOfScalar[T]:
    # sql = select(Actor)

    if filter := query.filter:
        if filter.label_selector:
            sql = sql.where(ActorEntity.labels == filter.label_selector)
        if filter.names:
            sql = sql.where(col(ActorEntity.name).in_(filter.names))

    if exclude := query.exclude:
        if exclude.label_selector:
            sql = sql.where(not_(ActorEntity.labels == exclude.label_selector))
        if exclude.names:
            sql = sql.where(not_(col(ActorEntity.name).in_(exclude.names)))

    sql = sql.where(ActorEntity.deletedTimestamp == null())

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
) -> ActorList:
    # convert all http query parameters to a ActorQuery
    # filter.label_selector=...    or label_selector=...
    # exclude.label_selector=...   or label_selector!=...
    # order=name DESC
    # order=name DESC
    # start=
    # limit=
    query = ActorQuery(
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
    query: ActorQuery, session: Session = Depends(get_session)
) -> ActorList:
    countSelect = select(func.count("*")).select_from(ActorEntity)
    itemsSelect = select(ActorEntity)

    countSelect = apply_query(countSelect, query, count=True)
    itemsSelect = apply_query(itemsSelect, query)

    start = query.pagination.start if query.pagination and query.pagination.start else 0
    limit = (
        query.pagination.limit if query.pagination and query.pagination.limit else 10
    )
    itemCount = session.exec(countSelect).one()
    remainingItemCount = max(itemCount - start - limit, 0)

    entities = session.exec(itemsSelect).all()

    return ActorList(
        meta=ListMeta(
            start=start,
            limit=limit,
            itemCount=itemCount,
            remainingItemCount=remainingItemCount,
        ),
        items=list(map(serialize, entities)),
    )
