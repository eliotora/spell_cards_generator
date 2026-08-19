from dataclasses import asdict, fields, Field
from typing import Any, ClassVar, get_type_hints, get_origin, get_args
from pathlib import Path
from enum import Enum
from typing import get_args, get_origin, Union
from types import UnionType
from enum import Enum
import json

from src.models.metadata import JsonMetadata

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        return super().default(obj)

def _convert_to_serializable(obj: Any) -> Any:
    """Convertit récursivement les enums et dataclasses en objets sérialisables."""
    if isinstance(obj, Enum):
        return obj.value
    elif hasattr(obj, "__dataclass_fields__"):
        return {k: _convert_to_serializable(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, dict):
        return {k: _convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_to_serializable(item) for item in obj]
    return obj

def _deserialize_field(value: Any, field_type: Any) -> Any:
    """Reconstruit un champ à partir de sa valeur JSON et son type hint."""
    if value is None:
        return None

    # Gérer Optional[T] et Union
    origin = get_origin(field_type)
    if origin is not None:
        args = get_args(field_type)
        # Pour Optional et Union, prendre le premier type non-None
        field_type = next((t for t in args if t is not type(None)), args[0])

    # Converter les Enums
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(value)

    # Converter les nested dataclasses
    if isinstance(field_type, type) and hasattr(field_type, "__dataclass_fields__"):
        if isinstance(value, dict):
            return field_type(**value)

    return value

class JsonMixin:
    """Mixing for models that either have to be saved to JSON or loaded from a JSON file"""
    REQUIRED_METADATA = "json"

    DATA_FOLDER: ClassVar[Path]

    def to_json(self):
        data = _convert_to_serializable(self)
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        try:
            data = json.loads(text)
            return cls.from_dict(data)

        except Exception as e:
            print(cls.__name__, text)
            raise e

    @classmethod
    def from_dict(cls, data: dict[str: Any]):
        # Récupérer les type hints de la classe
        hints = get_type_hints(cls)

        # Reconstruire les champs avec les bons types
        for field_name, value in data.items():
            if field_name in hints:
                data[field_name] = _deserialize_field(value, hints[field_name])

        return cls(**data)

    @classmethod
    def json_fields(cls) -> list[tuple[Field[Any], JsonMetadata]]:
        result = []

        for f in fields(cls):
            meta = f.metadata.get(JsonMetadata.METADATA_NAMESPACE)

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

    @classmethod
    def data_to_field(cls, value, expected_type:type):
        origin = get_origin(expected_type)
        if origin is Union or origin is UnionType: # Multiple possible types
            args = get_args(expected_type)

            for t in args:
                if get_origin(t) is None and isinstance(t, type) and type(value) is t:
                    return value
            errors: list[tuple[Exception, Any, type]] = []
            for t in args: # Each possible type
                try:
                    v = cls.data_to_field(value, t) # We try to convert
                    return v
                except Exception as e:
                    errors.append((e, value, t))
            raise ValueError(f"Could not convert value {value} to any {args} from arguments of {expected_type}.\nGot the following errors: {"\n".join([f"{str(e)} ; {v} ; {t}" for e,v,t in errors])}") # If none work we raise an error
        elif origin is list or origin is set: # The expected type is a list or a set
            args = get_args(expected_type)
            if isinstance(value, list) or isinstance(value, set) or isinstance(value, dict): # And the type of the value is too
                value = list(value)
                for i,v in enumerate(value): # We transform each element of the list or set
                    tv = cls.data_to_field(v, args[0])
                    value[i] = tv
                return origin(value) # Then we transform the value iterable to the origin type
            else:
                return origin([cls.data_to_field(value, args[0])])
        elif origin is None:
            if isinstance(value, expected_type):
                return value
            if issubclass(expected_type, Enum):
                return expected_type[value]
            if expected_type is None:
                return None
            else:
                return expected_type(value)
        elif origin is dict:
            args = get_args(expected_type)
            if isinstance(value, dict):
                res = {}
                for key, val in value.items():
                    k = cls.data_to_field(key, args[0])
                    v = cls.data_to_field(val, args[1])
                    res[k] = v
                return res
            else:
                raise ValueError(f"Could not convert value {value} to {expected_type}")
        else:
            raise(ValueError(f"Unexpected origin was {origin}"))