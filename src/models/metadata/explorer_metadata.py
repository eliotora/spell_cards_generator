from dataclasses import dataclass
from src.utils import normalize_text
import enum

class FilterOption(enum.IntEnum):
    """Enum for filter options."""
    LIST = 1
    INT_RANGE = 2
    LINE_EDIT = 3
    NONE = 0

    @classmethod
    def from_string(cls, value: str) -> 'FilterOption':
        """Convert a string to a FilterOption enum."""
        try:
            return cls[value.upper()]
        except Exception as e:
            raise ValueError(f"No such value in {cls.__class__.__name__}")

    def __str__(self) -> str:
        """String representation of the enum."""
        return self.name.lower()

    def value_in_filter(self, value: str|int, filters: list[str|int]) -> bool:
        """Check if a value is in the filter options"""
        if self == FilterOption.LIST:
            if type(value) == list:
                return any(v in filters for v in value)

            return value in filters
        elif self == FilterOption.INT_RANGE:
            if isinstance(value, int) and len(filters) == 2:
                return filters[0] <= value <= filters[1]

            return False
        elif self == FilterOption.LINE_EDIT:
            if value == None:
                value = ""
            if isinstance(value, str):
                if all([filter.lower() == "" for filter in filters]):
                    return True
                flag = any(normalize_text.normalize_text(filter.lower()) in normalize_text.normalize_text(value.lower()) for filter in filters)
                return flag
            return False

class VisibilityOption(enum.IntEnum):
    """Enum for visibility options."""
    ALWAYS_VISIBLE = 1
    HIDDABLE = 2
    HIDDABLE_WITH_FILTER = 3
    ALWAYS_HIDDEN = 4

    @classmethod
    def from_string(cls, value: str) -> 'VisibilityOption':
        """Convert a string to a VisibilityOption enum."""
        return cls[value.upper()]

    def __str__(self) -> str:
        """String representation of the enum."""
        return self.name.lower()


@dataclass(frozen=True)
class ExplorerMetadata:
    label:str
    visibility: VisibilityOption
    filter_type: FilterOption = FilterOption.NONE
    cols_to_hide: tuple[int] = ()