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


class FeedbackEntity(SQLModel, table=True):
    __tablename__ = "feedback"
    __table_args__ = (
        UniqueConstraint(
            "namespace",
            "name",
            "deletedTimestamp",
            name="feedback_name_is_unique_in_namespace",
        ),
    )

    # ids
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace: str = Field(foreign_key="namespace.name")
    name: str = Field()

    # meta
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
    actor: str = Field(foreign_key="actor.name")
    item: str = Field(foreign_key="item.name")
    type: Optional[str] = Field(nullable=True)
    value: str = Field()
