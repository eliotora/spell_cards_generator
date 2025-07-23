from dataclasses import dataclass
from typing import Optional
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from model.detailable_model import DetailableModel
import locale, os, json

from ui.details_windows.generic_detail_window import GenericDetailWindow

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

def load_metamagics_from_folder(folder_path: str):
    metamagics = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        metamagics_folder = os.path.join(full_source_path, "metamagics")
        if not os.path.exists(metamagics_folder):
            continue
        for filename in os.listdir(metamagics_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(metamagics_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        metamagic_data = json.load(file)
                        metamagic = Metamagic(
                            name=metamagic_data.get("nom", ""),
                            vo_name=metamagic_data.get("nom_vo", ""),
                            vf_name=metamagic_data.get("nom_vf", ""),
                            point_cost=metamagic_data.get("cout_en_points", ""),
                            cumulable=metamagic_data.get("cumulable", ""),
                            description=metamagic_data.get("description", ""),
                            short_description=metamagic_data.get("description_short", ""),
                            source=source_folder
                        )
                        metamagics.append(metamagic)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return metamagics

class MetamagicModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.GRIMOIRE,
        ExportOption.CARDS
    ]
    load_items_method = load_metamagics_from_folder

@dataclass
class Metamagic(DetailableModel):
    name: str = field_metadata(
        label="Nom",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.ALWAYS_VISIBLE
    )
    vf_name: Optional[str] = field_metadata(
        label="Nom VF", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[2]
    )
    vo_name: Optional[str] = field_metadata(
        label="Nom VO", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[3]
    )
    point_cost: str = field_metadata(
        label="Coût en points", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[4]
    )
    cumulable: Optional[bool] = field_metadata(
        label="Cumulable avec une autre", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[5]
    )
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description", visibility=VisibilityOption.HIDDABLE_WITH_FILTER, cols_to_hide=[6], filter_type=FilterOption.LINE_EDIT
    )
    source: str = field_metadata(
        label="Source", visibility=VisibilityOption.HIDDABLE, filter_type=FilterOption.LIST, cols_to_hide=[7]
    )
    collection = MetamagicModels

    def __str__(self):
        """String representation of the Metamagic."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."
