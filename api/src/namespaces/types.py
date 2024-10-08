from typing import Optional
from pydantic import BaseModel, Field

from ..shared.types import (
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
class NamespaceMeta(OptionalCommonMeta, HasUUID, OptionalNameOrGenerateName):
    pass


class NamespaceSpec(BaseModel):
    lifecycle: Optional[str] = None
    owner: Optional[str] = None
    contact: Optional[str] = None


class Namespace(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Namespace"
    meta: NamespaceMeta
    spec: Optional[NamespaceSpec] = None


class NamespaceFilter(LabelSelectorFilter, NamesFilter):
    pass


class NamespaceQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "NamespaceQuery"
    filter: Optional[NamespaceFilter] = None
    exclude: Optional[NamespaceFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = Field(default=Pagination())


class NamespaceList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "NamespaceList"
    meta: ListMeta
    items: list[Namespace]


# class NamespaceStatsResult(BaseModel):
#     apiVersion: str = "v1alpha1"
#     kind: str = "NamespaceStatsResult"
#     actors: int
#     items: int
#     events: int
#     feedbacks: int
