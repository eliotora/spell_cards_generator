from dataclasses import dataclass, field
from locale import setlocale, LC_COLLATE
from enum import Enum
from datetime import date
from pathlib import Path
from typing import Any

from src.models.base import BaseModel, TranslatedText
from src.models.collections.base_collection import BaseCollection
from src.models.mixins import (
    ExplorableMixin,
    JsonMixin,
    PopupMixin
)
from src.models.metadata import (
    ExplorerMetadata,
    JsonMetadata,
    FilterOption,
    VisibilityOption
)
from src.models.repositories.data_repository import DataRepository

setlocale(LC_COLLATE, "French_France.1252")

class BookCategory(Enum):
    CORE=TranslatedText({"fr": "Base", "en": "Core"})
    SETTING=TranslatedText({"fr": "Setting de campagne", "en": "Setting"})
    SUPPLEMENT=TranslatedText({"fr": "Supplément", "en": "Supplement"})
    PLAYTEST=TranslatedText({"fr": "Phase de test", "en": "Playtest"})


@dataclass
class SourceModel(BaseModel, ExplorableMixin, JsonMixin, PopupMixin):
    editor: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Éditeur",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    abreviation: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Abréviation",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    name: TranslatedText = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata()
        },
        default_factory=TranslatedText
    )
    year: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Publication",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata()
        },
        default=date.today().year
    )
    category: BookCategory = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Publication",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata()
        },
        default=BookCategory.SUPPLEMENT
    )

    modelname = "source"
    DATA_FOLDER = Path("source")

    @classmethod
    def from_dict(cls, data:dict[str, Any]) -> "SourceModel":
        data["category"] = BookCategory[data.pop("category")]
        return super().from_dict(data)



SourceModel.collection = BaseCollection(DataRepository.load_all(SourceModel))