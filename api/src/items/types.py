from typing import Optional
from pydantic import BaseModel

from ..shared.types import (
    OptionalNamespace,
    OptionalNameOrGenerateName,
    HasUUID,
    OptionalCommonMeta,
    ListMeta,
    NamesFilter,
    LabelSelectorFilter,
)


# JSON output order is from right to left
class ItemMeta(
    BaseModel,
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class ItemSpec(BaseModel):
    pass


class Item(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Item"
    meta: ItemMeta
    spec: ItemSpec


class ItemFilter(BaseModel, NamesFilter, LabelSelectorFilter):
    pass


class ItemQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ItemQuery"
    filter: ItemFilter
    exclude: Optional[ItemFilter] = None


class ItemList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "ItemList"
    meta: ListMeta
    items: list[Item]
