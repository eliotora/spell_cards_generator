from dataclasses import fields, Field
from typing import ClassVar

from src.models.collections.base_collection import BaseCollection

class ExplorableMixin:
    """For any class that should be able to be search and filtered in a tab"""
    METADATA_NAMESPACE = "explorer"
    REQUIRED_METADATA = "explorer"

    collection: ClassVar[BaseCollection]

    @classmethod
    def explorer_fields(cls) -> list[tuple[Field, dict]]:
        result = []

        for f in fields(cls):
            meta = f.metadata.get(cls.METADATA_NAMESPACE)

            if meta:
                result.append((f,meta))

        return result

    @classmethod
    def validate_metadata(cls):
        for f in fields(cls):
            if cls.REQUIRED_METADATA not in f.metadata:
                raise AttributeError(f"{cls.__name__}.{f.name} missing explorer metadata")

    @classmethod
    def get_collection(cls) -> BaseCollection:
        return cls.collection