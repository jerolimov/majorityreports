from typing import Optional, Dict
from pydantic import BaseModel

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
    BaseModel,
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class ActorSpec(BaseModel):
    features: Optional[Dict[str, str]] = None


class Actor(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Actor"
    meta: ActorMeta
    spec: ActorSpec


class ActorFilter(BaseModel, NamesFilter, LabelSelectorFilter):
    pass


class ActorQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ActorQuery"
    filter: Optional[ActorFilter] = None
    exclude: Optional[ActorFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = None


class ActorList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ActorList"
    meta: ListMeta
    items: list[Actor]
