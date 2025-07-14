from dataclasses import dataclass, field, fields
from typing import Optional
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

@dataclass
class Feat(ExplorableModel):
    name : str = field_metadata(label="Nom", filter_type=FilterOption.LINE_EDIT, visibility=VisibilityOption.ALWAYS_VISIBLE)
    vf_name: Optional[str] = field_metadata(label="Nom VF", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[2])
    vo_name: Optional[str] = field_metadata(label="Nom VO", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[3])
    prerequisite: str = field_metadata(label="Prérequis", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[4])
    description: str = field_metadata(label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN)
    short_description: Optional[str] = field_metadata(label="Description", filter_type=FilterOption.LINE_EDIT, visibility=VisibilityOption.HIDDABLE_WITH_FILTER, cols_to_hide=[5])
    source: str = field_metadata(label="Source", filter_type=FilterOption.LIST, visibility=VisibilityOption.HIDDABLE, cols_to_hide=[6])

    def __str__(self):
        """String representation of the Feat."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    @classmethod
    def from_dict(cls, data: dict) -> 'Feat':
        """Create a Feat instance from a dictionary."""
        return cls(
            name=data.get("nom", ""),
            vo_name=data.get("nom_vo"),
            vf_name=data.get("nom_vf"),
            prerequisite=data.get("prérequis", ""),
            description=data.get("description", ""),
            short_description=data.get("description_short"),
            source=data.get("source", "")
        )

if __name__ == "__main__":
    feat = Feat(
        name="Exemple de talent",
        vo_name="Example Feat",
        vf_name="Talent d'exemple",
        prerequisite="Aucun",
        description="Ceci est une description d'exemple pour un talent.",
        short_description="Description courte de l'exemple.",
        source="Manuel de base"
    )
    print(feat)
    print(fields(feat)[0].metadata["label"])
    for key, item in feat.__dataclass_fields__.items():
        print(f"{key}: {item.metadata.get('label', 'No label')}, Filter Type: {item.metadata.get('filter_type', 'No filter type')}, Visibility: {item.metadata.get('visibility', 'No visibility')}")