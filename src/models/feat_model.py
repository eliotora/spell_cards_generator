from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import locale

from src.models.base import BaseModel
from src.models.mixins import ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin, ExportOption
from src.models.metadata import ExplorerMetadata, JsonMetadata, FilterOption, VisibilityOption


locale.setlocale(locale.LC_COLLATE, "French_France.1252")

@dataclass
class FeatModel(BaseModel, ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                visibility=VisibilityOption.ALWAYS_VISIBLE,
                filter_type=FilterOption.LINE_EDIT
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    vf_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Nom VF",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,)
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    vo_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Nom VO",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(3,)
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    category: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Catégorie",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(4,)
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    prerequisite: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Prérequis",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(5,)
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    repetable: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Répétable",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(6,)
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    description: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Description",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    short_description: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Description",
                visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
                cols_to_hide=(7,),
                filter_type=FilterOption.LINE_EDIT
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata()
        }
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Source",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(8,),
                filter_type=FilterOption.LIST
            ),
            JsonMixin.METADATA_NAMESPACE:
            JsonMetadata(in_file=False)
        },
        default=None
    )

    color = "#C93C0C"
    DATA_FOLDER = Path("feats")
    modelname = "Feat"
    export_options = [ExportOption.RULES, ExportOption.CARDS]

    def to_html_dict(self):
        result = {}
        result['title'] = self.name
        result["subtitle"] = ""
        if self.vo_name:
            result['subtitle'] = f"{self.vo_name}"
            if self.vf_name:
                result["subtitle"] += f" - {self.vf_name}"
        result['italics'] = [
            f"<em>{self.__class__.__dataclass_fields__[field].metadata.get(ExplorableMixin.METADATA_NAMESPACE).label} : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}</em>"
            for field in ["category","prerequisite"] if self.__getattribute__(field) != ""
        ]
        result['bolds'] = []
        result['main_text'] = self.description
        result['source'] = self.source
        return result