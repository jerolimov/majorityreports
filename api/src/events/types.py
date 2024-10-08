from typing import Optional
from pydantic import BaseModel, Field

from ..shared.types import (
    OptionalNamespace,
    OptionalNameOrGenerateName,
    HasUUID,
    OptionalCommonMeta,
    ListMeta,
    NamesFilter,
    LabelSelectorFilter,
    OrderBy,
    Pagination,
)


# JSON output order is from right to left
class EventMeta(
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class EventSpec(BaseModel):
    type: Optional[str] = Field(default=None, max_length=63)
    actor: Optional[str] = None
    item: Optional[str] = None
    value: Optional[str] = None
    # count: int = Field(default=0) ???


class Event(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Event"
    meta: EventMeta
    spec: EventSpec


class EventFilter(LabelSelectorFilter, NamesFilter):
    pass


class EventQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "EventQuery"
    namespace: Optional[str] = None
    filter: Optional[EventFilter] = None
    exclude: Optional[EventFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = Field(default=Pagination())


class EventList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "EventList"
    meta: ListMeta
    items: list[Event]
