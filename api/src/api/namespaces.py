from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import (
    Session,
    select,
    null,
)
from sqlalchemy import func
from pydantic import BaseModel
from typing import Sequence

from ..types.v1alpha1.namespace import NamespaceQuery, ListMeta, Pagination

from ..db import get_session
from ..db.namespace import Namespace, apply_query


class NamespaceList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "NamespaceList"
    meta: ListMeta
    items: Sequence[Namespace]


router = APIRouter()


@router.post("")
def create_namespace(
    newNamespace: Namespace, session: Session = Depends(get_session)
) -> Namespace:
    namespace = Namespace()
    namespace.name = newNamespace.name
    namespace.labels = newNamespace.labels
    namespace.annotations = newNamespace.annotations
    session.add(namespace)
    session.commit()
    session.refresh(namespace)
    return namespace


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


@router.get("/{namespace_name}")
def read_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> Namespace:
    statement = select(Namespace)
    statement = statement.where(Namespace.name == namespace_name)
    statement = statement.where(Namespace.deletedTimestamp == null())
    return session.exec(statement).one()


@router.put("/{namespace_name}")
def update_namespace(
    namespace_name: str,
    updateNamespace: Namespace,
    session: Session = Depends(get_session),
) -> Namespace:
    namespace = read_namespace(namespace_name)
    if name := updateNamespace.name:
        namespace.name = name
    if labels := updateNamespace.labels:
        namespace.labels = labels
    if annotations := updateNamespace.annotations:
        namespace.annotations = annotations
    session.commit()
    session.refresh(namespace)
    return namespace


@router.delete("/{namespace_name}")
def delete_namespace(
    namespace_name: str, session: Session = Depends(get_session)
) -> JSONResponse:
    namespace = read_namespace(namespace_name, session)

    softDelete = namespace.labels.get("soft-delete") == "true"

    if softDelete:
        namespace.deletedTimestamp = datetime.now()
        namespace.annotations = {}
        session.add(namespace)
        session.commit()
    else:
        session.delete(namespace)
        session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Namespace deleted"}
    )
