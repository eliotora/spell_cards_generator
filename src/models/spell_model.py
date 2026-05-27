from dataclasses import dataclass, field, fields
from typing import Optional
import locale
from pathlib import Path

from src.models.base import BaseModel
from src.models.mixins import ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin, MODEL_EXPORT_MODE_HTML_FILES, ExportOption
from src.models.metadata import ExplorerMetadata, JsonMetadata, FilterOption, VisibilityOption

from src.ui.details_windows.spell_detail_window import SpellDetailWindow

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

@dataclass
class SpellModel(BaseModel, ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin):
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
    vf_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom VF",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    vo_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom VO",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(3,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    classes: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Classes",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    schools: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="École",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(4,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    level: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Niveau",
                filter_type=FilterOption.INT_RANGE,
                visibility=VisibilityOption.ALWAYS_VISIBLE
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    casting_time: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Temps d'incantation",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(6,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    range: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Portée",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(7,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    components: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Composantes",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(8,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    duration: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Durée",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    concentration: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Concentration",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(9,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    ritual: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Rituel",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(10,)
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
    short_description: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
                cols_to_hide=(11,),
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
                cols_to_hide=(12,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(
                in_file=False
            )
        },
        default=None
    )
    at_higher_levels: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Aux niveaux supérieurs",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )

    DATA_FOLDER = Path("spells")
    popup_window_class = SpellDetailWindow
    color = "#6D0000"
    modelname = "Spell"
    export_options = [ExportOption.RULES, ExportOption.CARDS, ExportOption.GRIMOIRE]

    def to_html_dict(self):
        result = {}
        result['title'] = self.name
        if self.vo_name:
            result['subtitle'] = self.vo_name
            if self.vf_name:
                result["subtitle"] += " + " + self.vf_name
        result['italics'] = [f"niveau {self.level} - {self.schools[0] if len(self.schools) < 2 else f"{self.schools[0]} ({", ".join(self.schools[1:])})" }{f" (rituel)" if self.ritual else ""}"]
        result['bolds'] = [f"<strong>{self.__class__.__dataclass_fields__[field].metadata.get(ExplorableMixin.METADATA_NAMESPACE).label}</strong> : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}"
                           for field in ["casting_time", "range", "components", "duration"]]
        result['main_text'] = f"{self.description}{f"<br><strong>Aux niveaux supérieurs. </strong>{self.at_higher_levels}" if self.at_higher_levels else ""}"
        result["footer"] = [f"<div class='classe'>{classe}</div>" for classe in self.classes]
        result["source"] = self.source
        result["level"] = self.level
        result["name"] = self.name
        return result

MODEL_EXPORT_MODE_HTML_FILES[(SpellModel.__name__.lower(), ExportOption.GRIMOIRE.value)] = "spell_grimoire.html"