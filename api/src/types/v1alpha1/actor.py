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
class ActorMeta(
    BaseModel,
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class ActorSpec(BaseModel):
    pass


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
    filter: ActorFilter
    exclude: Optional[ActorFilter] = None


class ActorList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ActorList"
    meta: ListMeta
    items: list[Actor]
