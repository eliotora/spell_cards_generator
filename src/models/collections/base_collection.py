from typing import Any, Generic, TypeVar, Iterator, Callable
from copy import deepcopy
import operator

from src.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)
Predicate = Callable[[Any], bool]

OPS: dict[str, Callable] = {
    "eq":           operator.eq,
    "neq":          operator.ne,
    "gt":           operator.gt,
    "gte":          operator.ge,
    "lt":           operator.lt,
    "lte":          operator.le,
    "in":           lambda a, b: a in b,
    "not_in":       lambda a, b: a not in b,
    "contains":     lambda a, b: b in a,
    "startswith":   lambda a, b: a.startswith(b),
}


class BaseCollection(Generic[T]):
    """Base for all collection classes"""

    def __init__(self, items:list[T] | None = None):
        self._items: list[T] = items or []

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __contains__(self, item) -> bool:
        return item in self._items

    def __getitem__(self, key) -> T:
        return self._items[key]

    def __setitem__(self, key, value) -> None:
        self._items[key] = value

    def __delitem__(self, key) -> None:
        self._items.__delitem__(key)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self)})"

    def __str__(self) -> str:
        return self.__repr__()

    def items(self) -> list[T]:
        return deepcopy(self._items)

    def add(self, item) -> None:
        self._items.append(item)

    def get(self, index) -> T:
        return self._items[index]

    def find(self, predicate: Callable) -> T:
        for item in self._items:
            if predicate(item) is True:
                return item

    def filter(self, rule: dict) -> 'BaseCollection[T]':
        predicate = self.build_predicate(rule)
        return self.__class__([i for i in self._items if predicate(i)])

    def get_by_field(self, field_name, value) -> T|None:
        if not hasattr(self._items[0], field_name):
            raise ValueError(f"Model {self._items[0].__class__.__name__} doesn't have attribute {field_name}")

        if isinstance(value, str): value = value.lower()

        for i in self._items:
            attribute = getattr(i, field_name)
            if isinstance(attribute, str): attribute = attribute.lower()
            if isinstance(attribute, list): pass

            if attribute == value:
                return i

        return None

    def _get_field(self, obj: Any, field: str) -> Any:
        for part in field.split("."):
            if isinstance(obj, dict):
                obj = obj[part]
            else:
                obj = getattr(obj, part)
        return obj

    def build_predicate(self, rule: dict) -> Predicate:
        if "and" in rule:
            subs = [self.build_predicate(r) for r in rule["and"]]
            return lambda obj: all(p(obj) for p in subs)

        if "or" in rule:
            subs = [self.build_predicate(r) for r in rule["or"]]
            return lambda obj: any(p(obj) for p in subs)

        if "not" in rule:
            sub = self.build_predicate(rule["not"])
            return lambda obj: not sub(obj)

        field = rule["field"]
        op = rule["op"]
        value = rule["value"]

        if not op in OPS:
            raise ValueError(f"Unknown operator: {op!r}")

        fn = OPS[op]
        return lambda obj: fn(self._get_field(obj, field), value)


