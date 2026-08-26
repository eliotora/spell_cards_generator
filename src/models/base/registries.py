from dataclasses import dataclass
from typing import Generic, TypeVar, ClassVar

from src.models.base.translated_text import TranslatedText
from src.models.mixins.json_mixin import JsonMixin


@dataclass(frozen=True)
class RegisteredModel:
    key: str
    label: TranslatedText

    _registry: ClassVar[dict[str, "RegisteredModel"]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry = {}
        REGISTERED_MODELS[cls.__name__] = cls

    def __str__(self) -> str:
        return self.label.for_lang("fr")

    @classmethod
    def register(cls, key: str, label: TranslatedText, **extra_fields) -> "RegisteredModel":
        if key in cls._registry:
            return cls._registry[key]
        instance = cls(key=key, label=label, **extra_fields)
        cls._registry[key] = instance
        return instance

    @classmethod
    def register(cls, key:str, instance: "RegisteredModel"):
        if key in cls._registry:
            return cls._registry
        cls._registry[key] = instance
        return instance

    @classmethod
    def get(cls, key: str) -> "RegisteredModel":
        try:
            return cls._registry[key]
        except KeyError:
            raise ValueError(f"{cls.__name__} unknown : {key!r}") from None

    @classmethod
    def all(cls) -> list["RegisteredModel"]:
        return list(cls._registry.values())

    @classmethod
    def __contains__(cls, key: str) -> bool:
        return key in cls._registry

REGISTERED_MODELS: dict[str, RegisteredModel|JsonMixin] = {}