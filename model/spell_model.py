from dataclasses import dataclass
from typing import Optional, Type
from PyQt6.QtCore import QAbstractTableModel, Qt
from model.loaders.spell_loader import load_spells_from_folder
from copy import deepcopy
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ExplorableModel,
)
from ui.spell_detail_window import SpellDetailWindow
import locale, os, json

locale.setlocale(locale.LC_COLLATE, "French_France.1252")


class SpellModels:
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.GRIMOIRE,
        ExportOption.CARDS,
    ]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.spells = load_spells_from_folder("data")
            cls.spells.sort(key=lambda i: locale.strxfrm(i.name))
            cls.instance = super(SpellModels, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_item(cls, name: str):
        for spell in cls.spells:
            if spell.name.lower() == name.lower():
                return deepcopy(spell)
        return None

    @classmethod
    def get_items(cls):
        return deepcopy(cls.spells)


@dataclass
class Spell(ExplorableModel):
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
    classes: list[str] = field_metadata(
        label="Classes",
        visibility=VisibilityOption.ALWAYS_HIDDEN,
        filter_type=FilterOption.LIST,
    )
    school: str = field_metadata(
        label="École",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[5],
        filter_type=FilterOption.LIST,
    )
    level: int = field_metadata(
        label="Niveau",
        filter_type=FilterOption.INT_RANGE,
        visibility=VisibilityOption.ALWAYS_VISIBLE,
    )

    casting_time: str = field_metadata(
        label="Temps d'incantation",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[6],
    )
    range: str = field_metadata(
        label="Portée", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[7]
    )
    components: list[str] = field_metadata(
        label="Composantes", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[8]
    )
    duration: str = field_metadata(
        label="Durée", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    concentration: bool = field_metadata(
        label="Concentration", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[9]
    )
    ritual: bool = field_metadata(
        label="Rituel", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[10]
    )
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        filter_type=FilterOption.LINE_EDIT,
        cols_to_hide=[11],
    )
    at_higher_levels: Optional[str] = field_metadata(
        label="Aux niveaux supérieurs", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    source: str = field_metadata(
        label="Sources",
        visibility=VisibilityOption.HIDDABLE,
        filter_type=FilterOption.LIST,
        cols_to_hide=[12],
    )


    def __str__(self):
        """String representation of the Spell."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    @classmethod
    def get_collection(cls):
        return SpellModels

    @classmethod
    def get_detail_windowclass(cls):
        return SpellDetailWindow


def load_spells_from_folder(folder_path: str):
    spells = []
    class_lookup = {}

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load class spell lists ---
        class_folder = os.path.join(full_source_path, "spell_lists")
        if os.path.exists(class_folder) and os.path.isdir(class_folder):
            for class_file in os.listdir(class_folder):
                if class_file.endswith(".json"):
                    file_path = os.path.join(class_folder, class_file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            class_data = json.load(file)
                            for spell_name in class_data.get("sorts", []):
                                class_lookup.setdefault(spell_name, set()).add(
                                    class_data.get("classe", "")
                                )
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Erreur lors du chargement de {class_file}: {e}")

        # --- Load spells ---
        spell_folder = os.path.join(full_source_path, "spells")
        if os.path.exists(spell_folder) and os.path.isdir(spell_folder):
            for filename in os.listdir(spell_folder):
                if filename.endswith(".json"):
                    file_path = os.path.join(spell_folder, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            spell_data = json.load(file)
                            spell = Spell(
                                name=spell_data.get("nom"),
                                vf_name=spell_data.get("nom_VF"),
                                vo_name=spell_data.get("nom_VO"),
                                level=spell_data.get("niveau"),
                                school=spell_data.get("école"),
                                casting_time=spell_data.get("temps_d'incantation"),
                                range=spell_data.get("portée"),
                                components=spell_data.get("composantes"),
                                duration=spell_data.get("durée"),
                                concentration=spell_data.get("concentration"),
                                ritual=spell_data.get("rituel"),
                                description=spell_data.get("description"),
                                at_higher_levels=spell_data.get("à_niveau_supérieur"),
                                short_description=spell_data.get("description_short"),
                                source=source_folder,
                                classes=sorted(
                                    class_lookup.get(spell_data.get("nom", ""), [])
                                ),
                            )

                            spells.append(spell)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Erreur lors du chargement de {filename}: {e}")

    return spells
