from datetime import datetime
from uuid import UUID, uuid4 as create_uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict


class HasUUID:
    uid: UUID = Field(default_factory=create_uuid)


class OptionalNameOrGenerateName:
    name: Optional[str] = None
    generateName: Optional[str] = None


class OptionalNamespace:
    namespace: Optional[str] = None


class OptionalCommonMeta:
    title: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None
    tags: Optional[list[str]] = None

    creationTimestamp: Optional[datetime] = None
    updateTimestamp: Optional[datetime] = None
    deletedTimestamp: Optional[datetime] = None


class DateTimeFilter:
    # alternative: gt, ge, eq, lt, le ???
    after: Optional[datetime] = None
    afterIncl: Optional[bool] = None  # default true?
    before: Optional[datetime] = None
    beforeIncl: Optional[bool] = None  # default false?


class ListMeta(BaseModel):
    start: Optional[int] = None
    limit: Optional[int] = None
    # remainingItemCount: Optional[int] = None
    # next: Optional[str] = None


class NamesFilter:
    names: Optional[list[str]] = None


class LabelSelectorFilter:
    labelSelector: Optional[Dict[str, str]] = None
