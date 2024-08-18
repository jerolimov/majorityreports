import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel, UniqueConstraint, JSON, null, not_
from sqlalchemy import Column, DateTime, func, desc
from typing import Dict, Optional

from .types import NamespaceQuery


class NamespaceEntity(SQLModel, table=True):
    __tablename__ = "namespace"
    __table_args__ = (
        UniqueConstraint("name", "deletedTimestamp", name="namespace_name_is_unique"),
    )

    uid: uuid.UUID = Field(unique=True, default_factory=uuid.uuid4)
    name: str = Field(primary_key=True)
    creationTimestamp: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updateTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    deletedTimestamp: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    labels: Dict[str, str] = Field(default={}, sa_type=JSON)
    annotations: Dict[str, str] = Field(default={}, sa_type=JSON)


def apply_query(sql, query: NamespaceQuery, count: bool = False):
    # sql = select(Namespace)

    if filter := query.filter:
        if filter.label_selector:
            sql = sql.where(NamespaceEntity.labels == filter.label_selector)
        if filter.names:
            sql = sql.where(NamespaceEntity.name.in_(filter.names))

    if exclude := query.exclude:
        if exclude.label_selector:
            sql = sql.where(not_(NamespaceEntity.labels == exclude.label_selector))
        if exclude.names:
            sql = sql.where(not_(NamespaceEntity.name.in_(exclude.names)))

    sql = sql.where(NamespaceEntity.deletedTimestamp == null())

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
