from typing import Optional, Dict
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
class ActorMeta(
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class ActorSpec(BaseModel):
    type: Optional[str] = None
    features: Optional[Dict[str, str]] = None


class Actor(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Actor"
    meta: ActorMeta
    spec: ActorSpec


class ActorFilter(LabelSelectorFilter, NamesFilter):
    pass


class ActorQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ActorQuery"
    namespace: Optional[str] = None
    filter: Optional[ActorFilter] = None
    exclude: Optional[ActorFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = Field(default=Pagination())


class ActorList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ActorList"
    meta: ListMeta
    items: list[Actor]
