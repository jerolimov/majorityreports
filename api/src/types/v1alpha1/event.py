from typing import Optional
from pydantic import BaseModel

from .shared import (
    OptionalNamespace,
    OptionalNameOrGenerateName,
    HasUUID,
    OptionalCommonMeta,
    ListMeta,
    NamesFilter,
    LabelSelectorFilter,
)


# JSON output order is from right to left
class EventMeta(
    BaseModel,
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class EventSpec(BaseModel):
    type: Optional[str] = None
    actor: Optional[str] = None
    item: Optional[str] = None
    value: Optional[str] = None
    # count: int = Field(default=0) ???


class Event(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Event"
    meta: EventMeta
    spec: EventSpec


class EventFilter(BaseModel, NamesFilter, LabelSelectorFilter):
    pass


class EventQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "EventQuery"
    filter: EventFilter
    exclude: Optional[EventFilter] = None


class EventList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "EventList"
    meta: ListMeta
    items: list[Event]
