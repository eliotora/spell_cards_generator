from dataclasses import dataclass, field
from typing import Type
import enum


class ExportOption(enum.IntEnum):
    """Enum for export options."""
    RULES = 1
    GRIMOIRE = 2
    CARDS = 3

    @classmethod
    def from_string(cls, value: str) -> 'ExportOption':
        """Convert a string to an ExportOption enum."""
        return cls[value.upper()]

    def __str__(self) -> str:
        """String representation of the enum."""
        return self.name.lower()

class FilterOption(enum.IntEnum):
    """Enum for filter options."""
    LIST = 1
    INT_RANGE = 2
    LINE_EDIT = 3

    @classmethod
    def from_string(cls, value: str) -> 'FilterOption':
        """Convert a string to a FilterOption enum."""
        return cls[value.upper()]

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
            if isinstance(value, str):
                if all([filter.lower() == "" for filter in filters]):
                    return True
                return filters.lower() in value.lower()
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

def field_metadata(label=None, filter_type: FilterOption = None, visibility: VisibilityOption = VisibilityOption.ALWAYS_VISIBLE, cols_to_hide: list[int] = None):
    """Helper function to create field metadata."""
    return field(metadata={"label": label, "filter_type": filter_type, "visibility": visibility, "cols_to_hide": cols_to_hide})

@dataclass
class ExplorableModel:
    """Model that can have a tab and should be explorable by users"""
    def to_dict(self) -> dict[str, str|bool|int]:
        return {fname: getattr(self, fname) for fname in self.__dataclass_fields__}

    def __init_subclass__(cls):
        super().__init_subclass__()
        MODEL_NAME_MAPPING[cls.__name__] = cls

    @classmethod
    def get_collection(cls) -> Type:
        pass

    @classmethod
    def get_detail_windowclass(cls):
        pass


MODEL_NAME_MAPPING: dict[str, ExplorableModel] = {}