from dataclasses import asdict, fields
from typing import ClassVar
from pathlib import Path
import json



class JsonMixin:
    """Mixing for models that either have to be saved to JSON or loaded from a JSON file"""
    METADATA_NAMESPACE = "json"
    REQUIRED_METADATA = "json"

    DATA_FOLDER: ClassVar[Path]

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        try:
            return cls(**json.loads(text))
        except Exception as e:
            print(cls.__name__, text)
            raise e


    @classmethod
    def json_fields(cls):
        result = []

        for f in fields(cls):
            meta = f.metadata.get(cls.METADATA_NAMESPACE)

            if meta and meta.in_file:
                result.append((f, meta))

        return result

    @classmethod
    def validate_metadata(cls):
        for f in fields(cls):
            if cls.REQUIRED_METADATA not in f.metadata:
                print(
                    f"{cls.__name__}.{f.name} missing json metadata"
                )

    @classmethod
    def data_folder(cls) -> Path:
        return Path(cls.DATA_FOLDER)