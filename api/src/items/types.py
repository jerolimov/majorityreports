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
class ItemMeta(
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class ItemSpec(BaseModel):
    type: Optional[str] = None
    features: Optional[Dict[str, str]] = None


class Item(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Item"
    meta: ItemMeta
    spec: ItemSpec


class ItemFilter(LabelSelectorFilter, NamesFilter):
    pass


class ItemQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ItemQuery"
    namespace: Optional[str] = None
    filter: Optional[ItemFilter] = None
    exclude: Optional[ItemFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = Field(default=Pagination())


class ItemList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ItemList"
    meta: ListMeta
    items: list[Item]
