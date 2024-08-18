from fastapi import APIRouter, Depends
from sqlmodel import (
    Session,
    select,
)
from sqlalchemy import func
from pydantic import BaseModel
from typing import Sequence

from ..db import get_session
from .entity import NamespaceEntity as Namespace, apply_query
from .types import NamespaceQuery, ListMeta, Pagination


class NamespaceList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "NamespaceList"
    meta: ListMeta
    items: Sequence[Namespace]


router = APIRouter()


@router.get("")
def read_namespaces(
    start: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> NamespaceList:
    # convert all http query parameters to a NamespaceQuery
    # filter.label_selector=...    or label_selector=...
    # exclude.label_selector=...   or label_selector!=...
    # order=name DESC
    # order=name DESC
    # start=
    # limit=
    query = NamespaceQuery(
        filter={},
        exclude={},
        order=[],
        pagination=Pagination(
            start=start,
            limit=limit,
        ),
    )

    return query_namespaces(query, session)


@router.post("/query")
def query_namespaces(
    query: NamespaceQuery, session: Session = Depends(get_session)
) -> NamespaceList:
    countSelect = select(func.count("*")).select_from(Namespace)
    itemsSelect = select(Namespace)

    countSelect = apply_query(countSelect, query, count=True)
    itemsSelect = apply_query(itemsSelect, query)

    start = query.pagination.start if query.pagination and query.pagination.start else 0
    limit = (
        query.pagination.limit if query.pagination and query.pagination.limit else 10
    )
    itemCount = session.exec(countSelect).one()
    remainingItemCount = max(itemCount - start - limit, 0)

    return NamespaceList(
        meta=ListMeta(
            start=start,
            limit=limit,
            itemCount=itemCount,
            remainingItemCount=remainingItemCount,
        ),
        items=session.exec(itemsSelect).all(),
    )
