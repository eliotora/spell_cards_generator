from dataclasses import dataclass
from typing import Optional
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from model.detailable_model import DetailableModel, MODEL_EXPORT_MODE_HTML_FILES
from ui.details_windows.spell_detail_window import SpellDetailWindow
import locale, os, json

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

def load_combat_feats_from_folder(folder_path: str) -> list:
    combat_feats = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load combat feats ---
        combat_feats_folder = os.path.join(full_source_path, "combat_feats")
        if os.path.exists(combat_feats_folder) and os.path.isdir(combat_feats_folder):
            for filename in os.listdir(combat_feats_folder):
                if filename.endswith(".json"):
                    file_path = os.path.join(combat_feats_folder, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            feat_data = json.load(file)
                            feat = CombatFeat(
                                name=feat_data.get("nom"),
                                vf_name=feat_data.get("nom_VF"),
                                vo_name=feat_data.get("nom_VO"),
                                description=feat_data.get("description"),
                                short_description=feat_data.get("description_short"),
                                classes=feat_data.get("classes", []),
                                source=source_folder
                            )
                            combat_feats.append(feat)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Erreur lors du chargement de {filename}: {e}")

    return combat_feats

class CombatFeatModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]
    load_items_method = load_combat_feats_from_folder


@dataclass
class CombatFeat(DetailableModel):
    name: str = field_metadata(
        label="Nom",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.ALWAYS_VISIBLE,
    )
    vf_name: Optional[str] = field_metadata(
        label="Nom VF",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[2]
    )
    vo_name: Optional[str] = field_metadata(
        label="Nom VO",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[3]
    )
    description: str = field_metadata(
        label="Description",
        visibility=VisibilityOption.ALWAYS_HIDDEN,
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        cols_to_hide=[4]
    )
    source: str = field_metadata(
        label="Source",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[5]
    )
    classes: list[str] = field_metadata(
        label="Classes",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    collection = CombatFeatModels
    color = "#e00909"

    export_mode = MODEL_EXPORT_MODE_HTML_FILES

    def __str__(self):
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    def to_html_dict(self):
        result = {}
        result["title"] = self.name
        result["subtitle"] = ""
        if self.vo_name:
            result["subtitle"] += f"{self.vo_name}"
            if self.vf_name:
                result["subtitle"] += f" - {self.vf_name}"
        result["italics"] = []
        result["bold"] = []
        result["main_text"] = self.description
        result["source"] = self.source
        return result