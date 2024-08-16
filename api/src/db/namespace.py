import uuid
from datetime import datetime
from sqlmodel import (
    Field,
    SQLModel,
    UniqueConstraint,
    JSON,
)
from sqlalchemy import Column, DateTime, func
from typing import Dict, Optional


class Namespace(SQLModel, table=True):
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
