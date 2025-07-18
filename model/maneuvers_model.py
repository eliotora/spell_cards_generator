from dataclasses import dataclass
from typing import Optional, Type
from model.generic_model import (
    ExplorableModel,
    ExportOption,
    FilterOption,
    VisibilityOption,
    field_metadata,
)
from ui.details_windows.generic_detail_window import GenericDetailWindow
from copy import deepcopy
import locale, os, json

locale.setlocale(locale.LC_COLLATE, "French_France.1252")


class ManeuversModels:
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.maneuvers = load_maneuvers_from_folder("data")
            cls.maneuvers.sort(key=lambda i: locale.strxfrm(i.name))
            cls.instance = super(ManeuversModels, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_item(cls, name: str):
        for maneuver in cls.maneuvers:
            if maneuver.name.lower() == name.lower():
                return deepcopy(maneuver)
        return None

    @classmethod
    def get_items(cls):
        return deepcopy(cls.maneuvers)


@dataclass
class Maneuver(ExplorableModel):
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
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        cols_to_hide=[4],
    )
    source: str = field_metadata(
        label="Source",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[5],
    )

    def __str__(self):
        """String representation of the Maneuver."""
        return f"{self.name} ({self.source}) - {self.description[:50]}"

    @classmethod
    def from_dict(cls, data: dict) -> "Maneuver":
        """Create a Maneuver instance from a dictionary."""
        return cls(
            name=data.get("nom", ""),
            vo_name=data.get("nom_vo"),
            vf_name=data.get("nom_vf"),
            prerequisite=data.get("prérequis", ""),
            description=data.get("description", ""),
            short_description=data.get("description_short"),
            source=data.get("source", ""),
        )

    @classmethod
    def get_collection(cls) -> Type:
        return ManeuversModels



def load_maneuvers_from_folder(folder_path: str):
    maneuvers = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        maneuvers_folder = os.path.join(full_source_path, "maneuvers")
        if not os.path.exists(maneuvers_folder):
            continue
        for filename in os.listdir(maneuvers_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(maneuvers_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        maneuver_data = json.load(file)
                        maneuver = Maneuver(
                            name=maneuver_data.get("nom", ""),
                            vo_name=maneuver_data.get("nom_vo", ""),
                            vf_name=maneuver_data.get("nom_vf", ""),
                            description=maneuver_data.get("description", ""),
                            short_description=maneuver_data.get("description_short", ""),
                            source=source_folder
                        )
                        maneuvers.append(maneuver)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return maneuvers
