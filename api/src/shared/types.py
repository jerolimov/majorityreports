from datetime import datetime
from uuid import UUID, uuid4 as create_uuid
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
import re

# aligned with kubernetes resource names (and RFC 1123)
# see https://kubernetes.io/docs/concepts/overview/working-with-objects/names/
# This means the name must:
# - contain at most 63 characters
# - contain only lowercase alphanumeric characters or '-'
# - start with an alphanumeric character
# - end with an alphanumeric character
name_max_length = 63
name_pattern = r"^[a-z0-9]$|^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"

# aligned with kubernetes labels
# see https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
label_prefix_max_length = 253
label_prefix_pattern = r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$"
label_name_max_length = 63
label_name_pattern = r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-_\\.]{0,61}[a-zA-Z0-9])$"
label_value_max_length = 63
label_value_pattern = r"^$|^[a-zA-Z0-9]$|^[a-zA-Z0-9][a-zA-Z0-9-_\.]{0,61}[a-zA-Z0-9]$"

annotation_prefix_max_length = 253
annotation_prefix_pattern = r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$"
annotation_name_max_length = 63
annotation_name_pattern = r"^[a-zA-Z0-9]$|^[a-zA-Z0-9][a-zA-Z0-9-_\.]{0,61}[a-zA-Z0-9]$"
annotation_value_max_length = 1000


class HasUUID(BaseModel):
    uid: UUID = Field(
        default_factory=create_uuid,
        # max_length=uid_max_length,
        # pattern=uid_pattern,
    )


class OptionalNameOrGenerateName(BaseModel):
    name: Optional[str] = Field(
        default=None, max_length=name_max_length, pattern=name_pattern
    )
    generateName: Optional[str] = Field(
        default=None, max_length=name_max_length - 6, pattern=name_pattern
    )


class OptionalNamespace(BaseModel):
    namespace: Optional[str] = None


class OptionalCommonMeta(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None
    tags: Optional[list[str]] = None

    importedTimestamp: Optional[datetime] = None
    creationTimestamp: Optional[datetime] = None
    updatedTimestamp: Optional[datetime] = None
    deletedTimestamp: Optional[datetime] = None

    @field_validator("labels")
    @classmethod
    def check_labels(cls, labels: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        if labels is not None:
            for name, value in labels.items():
                assert len(name) > 0, "label name must not an empty string"
                parts = name.split("/")
                assert (
                    len(parts) <= 2
                ), "label name must not contain more than one slash (/)"
                if len(parts) == 2:
                    prefix = parts[0]
                    assert (
                        len(prefix) <= label_prefix_max_length
                    ), f"label prefix max length {label_prefix_max_length}"
                    assert re.match(
                        label_prefix_pattern, prefix
                    ), f"label prefix does not match pattern {label_prefix_pattern}"
                    name = parts[1]
                assert (
                    len(name) <= label_name_max_length
                ), f"label name max length {label_name_max_length}"
                assert re.match(
                    label_name_pattern, name
                ), f"label name does not match pattern {label_name_pattern}"
                assert (
                    len(value) <= label_value_max_length
                ), f"label value max length {label_value_max_length}"
                assert re.match(
                    label_value_pattern, value
                ), f"label value does not match the pattern {label_value_pattern}"
        return labels

    @field_validator("annotations")
    @classmethod
    def check_annotations(
        cls, annotations: Optional[Dict[str, str]]
    ) -> Optional[Dict[str, str]]:
        if annotations is not None:
            for name, value in annotations.items():
                assert len(name) > 0, "annotation name must not an empty string"
                parts = name.split("/")
                assert (
                    len(parts) <= 2
                ), "annotation name must not contain more than one slash (/)"
                if len(parts) == 2:
                    prefix = parts[0]
                    assert (
                        len(prefix) <= annotation_prefix_max_length
                    ), f"annotation prefix max length {annotation_prefix_max_length}"
                    assert re.match(
                        annotation_prefix_pattern, prefix
                    ), f"annotation prefix does not match pattern {annotation_prefix_pattern}"
                    name = parts[1]
                assert (
                    len(name) <= annotation_name_max_length
                ), f"annotation name max length {annotation_name_max_length}"
                assert re.match(
                    annotation_name_pattern, name
                ), f"annotation name does not match pattern {annotation_name_pattern}"
                assert (
                    len(value) <= annotation_value_max_length
                ), f"annotation value max length {annotation_value_max_length}"
        return annotations


class DateTimeFilter(BaseModel):
    # alternative: gt, ge, eq, lt, le ???
    after: Optional[datetime] = None
    afterIncl: Optional[bool] = None  # default true?
    before: Optional[datetime] = None
    beforeIncl: Optional[bool] = None  # default false?


class ListMeta(BaseModel):
    start: Optional[int] = None
    limit: Optional[int] = None
    itemCount: Optional[int] = None
    remainingItemCount: Optional[int] = None
    next: Optional[str] = None


class NamesFilter(BaseModel):
    names: Optional[list[str]] = None


class LabelSelectorFilter(BaseModel):
    label_selector: Optional[Dict[str, str]] = Field(
        default=None, validation_alias="labelSelector"
    )


class OrderBy(BaseModel):
    attribute: str
    direction: Optional[str] = None


class Pagination(BaseModel):
    start: Optional[int] = Field(default=None, ge=0)
    limit: Optional[int] = Field(default=10, ge=0, le=100)
