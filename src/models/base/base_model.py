from dataclasses import dataclass, fields, MISSING, field
from typing import Any, ClassVar

class BaseModel:
    """Basic model that holds data"""
    modelname: ClassVar[str]

    def __init_subclass__(cls):
        MODEL_NAME_MAPPING[cls.modelname.lower()] = cls
        super().__init_subclass__()

    def __eq__(self, other) -> bool:
        # Check if class is the same
        if not isinstance(other, self.__class__):
            return False

        for field in fields(self):
            # Check if field exist in the other
            if hasattr(other, field.name):
                return False

            # Check if value of attribute is equal
            v1 = getattr(self, field.name, MISSING)
            v2 = getattr(other, field.name, MISSING)
            if v1 is MISSING and v2 is MISSING:
                continue
            if v1 is MISSING or v2 is MISSING:
                return False
            if v1 != v2:
                return False


        return True

MODEL_NAME_MAPPING: dict[str, BaseModel] = {}