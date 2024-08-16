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
class FeedbackMeta(
    BaseModel,
    OptionalCommonMeta,
    HasUUID,
    OptionalNameOrGenerateName,
    OptionalNamespace,
):
    pass


class FeedbackSpec(BaseModel):
    type: Optional[str] = None
    actor: str
    item: str
    value: str


class Feedback(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "Feedback"
    meta: FeedbackMeta
    spec: FeedbackSpec


class FeedbackFilter(BaseModel, NamesFilter, LabelSelectorFilter):
    pass


class FeedbackQuery(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "FeedbackQuery"
    filter: FeedbackFilter
    exclude: Optional[FeedbackFilter] = None


class FeedbackList(BaseModel):
    apiVersion: str = "v1alpha1"
    kind: str = "FeedbackList"
    meta: ListMeta
    items: list[Feedback]
