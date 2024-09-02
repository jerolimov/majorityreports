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
class FeedbackMeta(
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class FeedbackSpec(BaseModel):
    type: Optional[str] = Field(default=None, max_length=63)
    actor: str
    item: str
    value: str


class Feedback(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Feedback"
    meta: FeedbackMeta
    spec: FeedbackSpec


class FeedbackFilter(LabelSelectorFilter, NamesFilter):
    pass


class FeedbackQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "FeedbackQuery"
    namespace: Optional[str] = None
    filter: Optional[FeedbackFilter] = None
    exclude: Optional[FeedbackFilter] = None
    order: Optional[list[OrderBy]] = None
    pagination: Optional[Pagination] = Field(default=Pagination())


class FeedbackList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "FeedbackList"
    meta: ListMeta
    items: list[Feedback]
