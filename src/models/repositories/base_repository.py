from typing import TypeVar, Generic
import os

from src.models.base.base_model import BaseModel
from src.models.mixins.json_mixin import JsonMixin

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    @classmethod
    def get_instance_from_file(cls, path: str, model_cls: type[T]) -> T:
        if not os.path.exists(path):
            raise ValueError(f"The path \"{path}\" doesn't exist.")
        with open(path, "r", encoding="utf-8") as file:
            return model_cls.from_json(file.read())

    @classmethod
    def write_instance_to_file(cls, instance: type[T], path: str):
        if not issubclass(type(instance), JsonMixin):
            raise TypeError(f"Instance of type {instance.__class__.__name__} is not {JsonMixin.__name__}")

        data = instance.to_json()
        if not data:
            raise ValueError(f"Instance of {instance.__class__.__name__} returns no data")

        with open(path, "w", encoding="utf-8") as file:
            file.write(data)