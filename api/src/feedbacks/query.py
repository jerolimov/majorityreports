from fastapi import APIRouter, Depends
from sqlmodel import Session, select, null, not_, col
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy import func, desc
from typing import TypeVar

from ..db import get_session
from ..shared.types import ListMeta, Pagination
from .entity import FeedbackEntity
from .types import FeedbackList, FeedbackQuery
from .crud import serialize


router = APIRouter()


T = TypeVar("T")


def apply_query(
    sql: SelectOfScalar[T],
    query: FeedbackQuery,
    count: bool = False,
) -> SelectOfScalar[T]:
    if query.namespace:
        sql = sql.where(FeedbackEntity.namespace == query.namespace)

    if filter := query.filter:
        if filter.label_selector:
            sql = sql.where(FeedbackEntity.labels == filter.label_selector)
        if filter.names:
            sql = sql.where(col(FeedbackEntity.name).in_(filter.names))

    if exclude := query.exclude:
        if exclude.label_selector:
            sql = sql.where(not_(FeedbackEntity.labels == exclude.label_selector))
        if exclude.names:
            sql = sql.where(not_(col(FeedbackEntity.name).in_(exclude.names)))

    sql = sql.where(FeedbackEntity.deletedTimestamp == null())

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
    namespace_name: str | None = None,
    start: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> FeedbackList:
    # convert all http query parameters to a FeedbackQuery
    # filter.label_selector=...    or label_selector=...
    # exclude.label_selector=...   or label_selector!=...
    # order=name DESC
    # order=name DESC
    # start=
    # limit=
    query = FeedbackQuery(
        namespace=namespace_name,
        filter=None,
        exclude=None,
        order=None,
        pagination=Pagination(
            start=start,
            limit=limit,
        ),
    )

    return query_items(query, namespace_name, session)


@router.post("/query", response_model_exclude_none=True)
def query_items(
    query: FeedbackQuery,
    namespace_name: str | None = None,
    session: Session = Depends(get_session),
) -> FeedbackList:
    query.namespace = namespace_name

    countSelect = select(func.count("*")).select_from(FeedbackEntity)
    itemsSelect = select(FeedbackEntity)

    countSelect = apply_query(countSelect, query, count=True)
    itemsSelect = apply_query(itemsSelect, query)

    start = query.pagination.start if query.pagination and query.pagination.start else 0
    limit = (
        query.pagination.limit if query.pagination and query.pagination.limit else 10
    )
    itemCount = session.exec(countSelect).one()
    remainingItemCount = max(itemCount - start - limit, 0)

    entities = session.exec(itemsSelect).all()

    return FeedbackList(
        meta=ListMeta(
            start=start,
            limit=limit,
            itemCount=itemCount,
            remainingItemCount=remainingItemCount,
        ),
        items=list(map(serialize, entities)),
    )
