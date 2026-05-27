from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import locale

from src.models.base import BaseModel
from src.models.mixins import ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin
from src.models.metadata import ExplorerMetadata, JsonMetadata, FilterOption, VisibilityOption

from src.ui.details_windows.profile_detail_window import ProfileDetailWindow

locale.setlocale(locale.LC_COLLATE, "French_France.1252")
@dataclass
class ProfileModel(BaseModel, ExplorableMixin, JsonMixin, PopupMixin, ExportableMixin):
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
    cr: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="FP",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(4,),
                filter_type=FilterOption.LIST
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    type: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Type",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(5,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    size: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Taille",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(6,),
                filter_type=FilterOption.LIST
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    ac: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Classe d'armure",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(7,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    hp: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="points de vie",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(8,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    speed: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Vitesse",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(9,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    alignment: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Alignement",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(10,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    stats: dict[str, int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Caractéristiques",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    legendary: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Légendaire",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(11,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    pb: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Bonus de maîtrise",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default="+0"
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Source",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(12,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(in_file=False)
        },
        default=None
    )
    proficiencies: dict[str, str] = field( # "proficiencies": {"Arcane": "P", "JS_FOR": "E", "Initiative": "P"} -> P pour proficiency (+BM) ; E pour expertise (+2xBM)
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Compétences",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=dict
    )
    details: dict[str, str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Détails",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    traits: Optional[dict[str, str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Traits",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    actions: Optional[dict[str, str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Actions",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    bonus_actions: Optional[dict[str, str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Actions bonus",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    reactions: Optional[dict[str, str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Réactions",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    legendary_actions: Optional[dict[str, str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Actions légendaires",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    legendary_text: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Texte légendaire",
                visibility=VisibilityOption.ALWAYS_HIDDEN
            )
        },
        default=None
    )
    description: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE:
            ExplorerMetadata(
                label="Description",
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(13,)
            )
        },
        default=""
    )

    popup_window_class = ProfileDetailWindow
    color = "#e69a28"
    DATA_FOLDER = Path("profiles")
    modelname = "Profile"

    def get_stat_mod(self, value:int) -> int:
        return (value - 10) // 2

    def get_proficiency_mod(self, value:int, name:str) -> int:
        if name not in self.proficiencies.keys():
            return self.get_stat_mod(value)

        # Profiency fixed?
        try:
            pb = int(self.pb)
            if self.proficiencies.get(name) == "P":
                return self.get_stat_mod(value) + pb
            elif self.proficiencies.get(name) == "E":
                return self.get_stat_mod(value) + 2 * pb
        except ValueError:
            return self.get_stat_mod(value)


    def get_html_dict(self):
        init_bonus = self.get_proficiency_mod(self.stats["dextérité"], "Initiative")
        try:
            int(self.pb)
            bm_text = ""
        except:
            pro = self.proficiencies.get("Initiative", None)
            if pro == "P":
                bm_text = " + BM "
            elif pro == "E":
                bm_text = " + 2xBM "
        init_text = f"{"0:+".format(init_bonus)}{bm_text if bm_text else ""} ({10+init_bonus}{bm_text if bm_text else ""})"

        res = {
            "name": self.name,
            "type": f"{self.type.capitalize()} de taille {self.size}, {self.alignment}",
            "init": init_text,
            "ac": self.ac,
            "hp": self.hp,
            "speed": self.speed,
            "car": [
                {
                    "name": key,
                    "value": stat,
                    "mod": self.get_stat_mod(stat),
                    "save": self.get_proficiency_mod(stat, key)
                } for key, stat in self.stats.items()
            ],
            "details": [
                {"name": key,"value": value} for key, value in self.details.items()
            ],
            "traits": [
                {"name": key, "value": value} for key, value in self.traits.items()
            ],
            "actions": [
                {"name": key, "value": value} for key, value in self.actions.items()
            ],
            "bonus_actions": [
                {"name": key, "value": value} for key, value in self.bonus_actions.items()
            ],
            "reactions": [
                {"name": key, "value": value} for key, value in self.reactions.items()
            ],
            "legendary": self.legendary,
            "legendary_text": self.legendary_text,
            "legendary_actions": [
                {"name": key, "value": value} for key, value in self.legendary_actions.items()
            ],
            "description": self.description,
            "source": self.source
        }