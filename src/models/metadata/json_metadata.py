from dataclasses import dataclass
from typing import ClassVar, Type

@dataclass(frozen=True)
class JsonMetadata:
    METADATA_NAMESPACE: ClassVar[str] = "json"
    in_file: bool = True
    form_type: Type = None