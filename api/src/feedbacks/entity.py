import uuid
from datetime import datetime
from sqlmodel import (
    Field,
    SQLModel,
    UniqueConstraint,
    JSON,
    Relationship,
)
from sqlalchemy import Column, DateTime, func
from typing import Dict, Optional

from ..namespaces.entity import NamespaceEntity
from ..actors.entity import ActorEntity
from ..items.entity import ItemEntity


class FeedbackEntity(SQLModel, table=True):
    __tablename__ = "feedback"
    __table_args__ = (
        UniqueConstraint(
            "namespace_name", "name", name="feedback_name_is_unique_in_namespace"
        ),
    )

    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    namespace_name: str = Field(foreign_key="namespace.name")
    namespace: NamespaceEntity = Relationship()
    name: str = Field()
    actor_name: str = Field(foreign_key="actor.name")
    actor: ActorEntity = Relationship()
    item_name: str = Field(foreign_key="item.name")
    item: ItemEntity = Relationship()
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
    type: Optional[str] = Field(nullable=True)
    value: str = Field()
