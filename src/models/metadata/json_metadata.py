from dataclasses import dataclass

@dataclass(frozen=True)
class JsonMetadata:
    in_file: bool = True