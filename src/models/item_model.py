from dataclasses import dataclass
from typing import Optional
from src.models.generic_model import (
    ExportOption,
    FilterOption,
    VisibilityOption,
    field_metadata,
    ModelCollection
)
from src.models.detailable_model import DetailableModel
import locale, os, json
from enum import Enum
from src.models.conceptual_models import WeaponType, WeaponProperty, Dice

locale.setlocale(locale.LC_COLLATE, "French_France.1252")


def load_magic_items_from_folder(folder_path: str):
    items = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        items_path = os.path.join(full_source_path, "items", "magic")
        if not os.path.exists(items_path):
            continue
        for filename in os.listdir(items_path):
            if filename.endswith(".json"):
                file_path = os.path.join(items_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        item_data = json.load(file)
                        item = Item(
                            name=item_data.get("nom", ""),
                            vo_name=item_data.get("nom_vo", ""),
                            vf_name=item_data.get("nom_vf", ""),
                            description=item_data.get("description", ""),
                            short_description=item_data.get("description_short", ""),
                            source=source_folder
                        )
                        items.append(item)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return items

def load_mundate_items_from_folder(folder_path: str):
    items = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        items_path = os.path.join(full_source_path, "items", "mundane")
        if not os.path.exists(items_path):
            continue
        for filename in os.listdir(items_path):
            if filename.endswith(".json"):
                file_path = os.path.join(items_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        item_data = json.load(file)
                        item = Item(
                            name=item_data.get("nom", ""),
                            vo_name=item_data.get("nom_vo", ""),
                            vf_name=item_data.get("nom_vf", ""),
                            description=item_data.get("description", ""),
                            short_description=item_data.get("description_short", ""),
                            source=source_folder
                        )
                        items.append(item)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return items

class ItemModels(ModelCollection):
    load_items_method = lambda folder_path: MagicItemModels.get_items() + MundaneItemModels.get_items()

class MagicItemModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]
    load_items_method = load_magic_items_from_folder

class MundaneItemModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]
    load_items_method = load_mundate_items_from_folder

@dataclass
class Item(DetailableModel):
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
    type: list[str] = field_metadata(
        label="Type",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.ALWAYS_VISIBLE
    )
    source: str = field_metadata(
        label="Source",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[8],
    )

    weight: Optional[str] = field_metadata(
        label="Poids",
        visibility=VisibilityOption.HIDDABLE, cols_to_hide=[6]
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        cols_to_hide=[7],
    )

    collection = ItemModels
    color = "#7F513E"

    def __str__(self):
        """String representation of the Maneuver."""
        return f"{self.name} ({self.source}) - {self.description[:50]}"

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
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

    def to_html_dict(self):
        result = {}
        result['title'] = self.name
        result["subtitle"] = ""
        if self.vo_name:
            result['subtitle'] = f"{self.vo_name}"
            if self.vf_name:
                result["subtitle"] += f" - {self.vf_name}"
        result['italics'] = [
            f"<em>{self.__class__.__dataclass_fields__[field].metadata['label']} : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}</em>"
            for field in []
        ]
        result['bolds'] = []
        result['main_text'] = self.description
        result['source'] = self.source
        return result

@dataclass
class MagicItem(Item):
    attunement: bool = field_metadata(
        label="Lien",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[9]
    )
    rarity: Optional[str] = field_metadata(
        label="Rareté",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[10]
    )
    collection = MagicItemModels

@dataclass
class MundaneItem(Item):
    cost: Optional[str] = field_metadata(
        label="Coût",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[9]
    )
    collection = MundaneItemModels

class Units(Enum):
    PLATINIUM=({"en":"pp", "fr":"pp"},1000)
    GOLD=({"en":"gp", "fr":"po"},100)
    ELECTRUM=({"en":"ep", "fr":"pe"},50)
    SILVER=({"en":"sp", "fr":"pa"},10)
    COPPER=({"en":"cp", "fr":"pc"},1)

    def get_unit_from_text(cls, text) -> 'Units':
        for u in cls:
            if text in u[0]:
                return u
        return None

class Cost:
    def __init__(self, cost_text:str=None):
        if cost_text is None:
            self.value = None
            self.unit: Units = None
        else:
            cost_text = cost_text.strip()
            elements = cost_text.split(" ")
            self.value = float(elements[0])
            self.unit: Units = Units.get_unit_from_text(elements[1])

    def __str__(self):
        return f"{self.value} {self.unit[0]["fr"]}"

@dataclass
class Weapon(MundaneItem):
    damage_dice: tuple[int, Dice]
    damage_type: str
    properties: Optional[list[WeaponProperty]]
    weapon_type: WeaponType = WeaponType.MELEE


