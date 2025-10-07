from dataclasses import dataclass
from typing import Optional
from models.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from models.detailable_model import DetailableModel
from ui.details_windows.profile_detail_window import ProfileDetailWindow
import locale, os, json

locale.setlocale(locale.LC_COLLATE, "French_France.1252")


def load_profiles_from_folder(folder_path: str):
    profiles = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load profiles ---
        profiles_folder = os.path.join(full_source_path, "profiles")
        if not os.path.exists(profiles_folder):
            continue
        for filename in os.listdir(profiles_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(profiles_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        profile_data = json.load(file)
                        profile = Profile(
                            name=profile_data.get("nom"),
                            vf_name=profile_data.get("nom_VF"),
                            vo_name=profile_data.get("nom_VO"),
                            cr=profile_data.get("cr"),
                            type=profile_data.get("type"),
                            size=profile_data.get("taille"),
                            ac=profile_data.get("classe d'armure"),
                            hp=profile_data.get("points de vie"),
                            speed=profile_data.get("vitesse"),
                            alignment=profile_data.get("alignement"),
                            legendary=profile_data.get("legendary"),
                            stats=profile_data.get("stats"),
                            details=profile_data.get("détails"),
                            traits=profile_data.get("traits"),
                            actions=profile_data.get("actions"),
                            bonus_actions=profile_data.get("actions bonus"),
                            reactions=profile_data.get("réactions"),
                            legendary_actions=profile_data.get("actions_leg"),
                            legendary_text=profile_data.get("actions_leg_texte"),
                            source=source_folder
                        )
                        profiles.append(profile)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return profiles

class ProfileModels(ModelCollection):
    export_options: list[ExportOption] = [ExportOption.RULES, ExportOption.CARDS]
    load_items_method = load_profiles_from_folder

@dataclass
class Profile(DetailableModel):
    name: str = field_metadata(
        label="Nom",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.ALWAYS_VISIBLE,
    )
    vf_name: Optional[str] = field_metadata(
        label="Nom VF", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[2]
    )
    vo_name: Optional[str] = field_metadata(
        label="Nom VO", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[3]
    )
    cr: Optional[str] = field_metadata(
        label="FP",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[4],
        filter_type=FilterOption.INT_RANGE,
    )
    type: str = field_metadata(
        label="Type",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[5],
    )
    size: str = field_metadata(
        label="Taille",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[6],
        filter_type=FilterOption.LIST,
    )
    ac: str = field_metadata(
        label="Classe d'armure", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[7]
    )
    hp: str = field_metadata(
        label="points de vie", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[8]
    )
    speed: str = field_metadata(
        label="Vitesse", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[9]
    )
    alignment: str = field_metadata(
        label="Alignement", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[10]
    )
    legendary: bool = field_metadata(
        label="Légendaire", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[11]
    )
    source: str = field_metadata(
        label="Source",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[12],
        filter_type=FilterOption.LIST,
    )
    stats: dict[str, int]
    details: dict[str, list[str]]
    traits: Optional[dict[str, str]]
    actions: Optional[dict[str, str]]
    bonus_actions: Optional[dict[str, str]]
    reactions: Optional[dict[str, str]]
    legendary_actions: Optional[dict[str, str]]
    legendary_text: Optional[str]
    collection = ProfileModels
    details_window_class = ProfileDetailWindow
    color = "#e69a28"

    def __str__(self):
        """String representation of the Profile"""
        return f"{self.name} ({self.source}) - {self.type}, {self.alignment}"

