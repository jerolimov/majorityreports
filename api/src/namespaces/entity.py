import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel, UniqueConstraint, JSON
from sqlalchemy import Column, DateTime, func
from typing import Dict, Optional


class NamespaceEntity(SQLModel, table=True):
    __tablename__ = "namespace"
    __table_args__ = (
        UniqueConstraint("name", "deletedTimestamp", name="namespace_name_is_unique"),
    )

    # name
    name: str = Field(primary_key=True)

    # uuid
    uid: uuid.UUID = Field(unique=True, default_factory=uuid.uuid4)

    # common
    title: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = Field(sa_type=JSON)
    annotations: Optional[Dict[str, str]] = Field(sa_type=JSON)
    tags: Optional[list[str]] = Field(sa_type=JSON)
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

    # spec
    lifecycle: Optional[str] = None
    owner: Optional[str] = None
    contact: Optional[str] = None