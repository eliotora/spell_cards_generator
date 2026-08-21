from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TranslatedText:
    by_lang: dict[str, str] = field(default_factory=dict)

    def for_lang(self, lang:str, fallback: str = "fr") -> str:
        return (
            self.by_lang.get(lang)
            or self.by_lang.get(fallback)
            or next(iter(self.by_lang.values()), "")
        )

    @classmethod
    def from_dict(cls, data: dict[str, str]):
        if not isinstance(data, dict):
            if isinstance(data, str):
                res = {
                    "fr": data,
                    "en": data
                }
                return cls(res)

        keys = data.keys()
        if any([not isinstance(k ,str) for k in keys]):
            raise ValueError(
                f"One of the keys of {data} is not a string"
            )
        values = data.values()
        if any([not isinstance(k ,str) for k in values]):
            raise ValueError(
                f"One of the values of {data} is not a string"
            )

        for k in data.keys():
            if len(k) > 2:
                data[k[0:2]] = data.pop(k)


        if len(data.keys()) == 0:
            data["fr"] = ""
            data["en"] = ""

        return cls(data)

    def __str__(self, lang:str="fr") -> str:
        return self.for_lang(lang)