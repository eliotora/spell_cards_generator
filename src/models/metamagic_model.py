from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import locale

from src.models.base import BaseModel
from src.models.mixins import ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin, MODEL_EXPORT_MODE_HTML_FILES, ExportOption
from src.models.metadata import ExplorerMetadata, JsonMetadata, FilterOption, VisibilityOption

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

@dataclass
class MetamagicModel(BaseModel, ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    point_cost: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Coût en points",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    description: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    vf_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom VF",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(3,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=""
    )
    vo_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom VO",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(4,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=""
    )
    cumulable: Optional[bool] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Cumulable",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(5,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=False
    )
    short_description: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
                cols_to_hide=(6,),
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(7,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(
                in_file=False
            )
        },
        default=None
    )

    color = "#992E2E"
    DATA_FOLDER = Path("metamagics")
    modelname = "Metamagic"
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
            for field in ["point_cost"]
        ]
        result['bolds'] = []
        result['main_text'] = self.description
        result['source'] = self.source
        return result