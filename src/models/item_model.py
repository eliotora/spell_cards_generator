from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Optional, get_type_hints, get_origin, get_args
import locale, os, json
from enum import Enum
from src.models.base import BaseModel
from src.models.collections.base_collection import BaseCollection
from src.models.metadata import (
    ExplorerMetadata,
    FilterOption,
    VisibilityOption,
    JsonMetadata,
)
from src.models.mixins import ExplorableMixin, ExportableMixin, PopupMixin, JsonMixin
from src.models.mixins.exportable_mixin import ExportOption
from src.models.repositories.data_repository import DataRepository

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

# ─────────────────────────────────────────────
# Properties and others
# ─────────────────────────────────────────────
@dataclass
class WeaponMastery(BaseModel, PopupMixin, JsonMixin, ExplorableMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        }
    )
    entries: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default_factory=list
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,)
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(in_file=False),
        },
        default=None,
    )

    DATA_FOLDER = Path("masteries")
    modelname = "Weapon Mastery"

    def __str__(self) -> str:
        return f"{self.name}\n{"\n".join(self.entries)}\n{self.source}".replace("<br>", "\n")


# ─────────────────────────────────────────────
# Details : Additional capacities by type
# ─────────────────────────────────────────────


@dataclass
class ItemData:
    def __str__(self) -> str:
        pass


@dataclass
class GearData(ItemData):
    text: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )

    def __str__(self) -> str:
        return self.text


@dataclass
class WeaponData(ItemData):
    damage_dice: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Dé de dégâts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    damage_type: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Type de dégâts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    category: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Catégorie",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    ranged: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="À distance",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=False,
    )
    properties: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Propriétés",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )
    mastery: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Botte d'arme",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    text: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )

    def __str__(self) -> str:
        type = f"<em>{self.category.capitalize()} {"à distance" if self.ranged else "de corps à corps"}</em>"
        damage = f"{self.damage_dice} {self.damage_type.lower()}{"s" if self.damage_dice != "1" else ""}"
        properties = ", ".join([p.capitalize() for p in self.properties])
        mastery = f"Botte d'arme: {self.mastery}"
        return "<br>".join([type, damage, properties, mastery])


@dataclass
class ArmorData(ItemData):
    ac_base: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Classe d'armure",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    category: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Catégorie",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    stealth_disadvantage: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Désavantage à la Discrétion",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=False,
    )
    min_strength: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Force minimum",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    dex_ac_mod_cap: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Maximum au bonus de DEX à la CA",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )

    def __str__(self) -> str:
        category = self.category
        ac = f"{self.ac_base}{f' + Dex{f" (max {self.dex_ac_mod_cap})" if self.dex_ac_mod_cap is not None else ""}' if self.dex_ac_mod_cap > 0 else ""}"
        stealth = (
            "Le porteur subit le Désavantage à ses tests de Dextérité (Discrétion)"
            if self.stealth_disadvantage
            else ""
        )
        strength = (
            f"Si le porteur n'est pas doté d'une valeur de Force au moins égale à {self.min_strength}, sa vitesse est réduite de 3 m."
            if self.min_strength
            else ""
        )
        return "<br>".join([i for i in [category, ac, stealth, strength] if i != ""])


@dataclass
class ToolData(ItemData):
    stat: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Caractéristiques",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    usage: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Utilisation",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    craft: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Artisanat",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default="",
    )

    def __str__(self) -> str:
        ability = f"<strong>Caractéristique :</strong> {self.stat}"
        usage = f"<strong>Utilisation :</strong> {self.usage}"
        craft = f"<strong>Artisanat :</strong> {self.craft}" if self.craft else ""
        return "<br>".join([i for i in [ability, usage, craft] if i != ""])


@dataclass
class MountData(ItemData):
    carrying_capacity_tons: float = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Capacité de charge (kg)",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0,
    )
    profile_name: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Profile",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )

    def __str__(self) -> str:
        return f"Capacité de charge : {self.carrying_capacity_tons*1000} kg"


@dataclass
class VehicleData(ItemData):
    speed_km_h: float = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Vitesse",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    crew_min: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Équipage minimum",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0,
    )
    cap_passengers: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Capacité de passagers",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0,
    )
    cap_cargo_tons: Optional[float] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Capacité de charge (tonnes)",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0,
    )
    hp: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="pv",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    ac: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="CA",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    min_damage_cap: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Seuil de dégâts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )

    def __str__(self) -> str:
        speed = f"Vitesse : {self.speed_km_h} km/h"
        capacity = (
            f"Capacité : {self.cap_cargo_tons} tonnes, {self.cap_passengers} passagers"
        )
        stats = f"Équipage : {self.crew_min}, CA : {self.ac}, pv : {self.hp}, Seuil de dégâts : {self.min_damage_cap}"
        return "<br>".join([speed, capacity, stats])

@dataclass
class AmmunitionData(ItemData):
    quantity: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Quantité",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=1,
    )
    storage: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Rangement",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    text: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
# ─────────────────────────────────────────────
# Enums / shared types
# ─────────────────────────────────────────────


class ItemType(Enum):
    WEAPON = (WeaponData, "arme")
    ARMOR = (ArmorData, "armure")
    SHIELD = (ArmorData, "bouclier")
    POTION = (GearData, "potion")
    SCROLL = (GearData, "parchemin")
    WAND = (GearData, "baguette")
    ROD = (GearData, "sceptre")
    RING = (GearData, "bague")
    WONDEROUS = (GearData, "merveilleux")
    GEAR = (GearData, "équipement")
    ARTISAN_TOOL = (ToolData, "outils d'artisan")
    TOOL = (ToolData, "outil")
    VEHICLE_LAND = (VehicleData, "véhicule terrestre")
    VEHICLE_WATER = (VehicleData, "véhicule aquatique")
    VEHICLE_AIR = (VehicleData, "véhicule volant")
    MOUNT = (MountData, "monture")
    AMMUNITION = (AmmunitionData, "munition")

    @property
    def data_class(self):
        return self.value[0]

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if isinstance(other, ItemType):
            return self.name < other.name
        elif isinstance(other, str):
            return self.name < other
        else:
            raise ValueError(f"Cannot compare ItemType with {other.__class__.__name__}")


class Rarity(Enum):
    MUNDANE = "mundane"
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    VERY_RARE = "very_rare"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"
    VARIES = "varies"  # group of generic items (ex: +1 weapon)

    def __str__(self):
        return self.name


# ---------------------------------------------------
# ItemModel (base)
# ---------------------------------------------------


@dataclass
class ItemModel(BaseModel, ExplorableMixin, ExportableMixin, PopupMixin, JsonMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    item_type: ItemType = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Type",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.ALWAYS_VISIBLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    rarity: Rarity = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Rareté",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=Rarity.MUNDANE,
    )
    weight: float = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Poids",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0.0,
    )
    value_cp: int = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Prix (en cuivre)",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=0,
    )
    entries: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )
    requires_attunement: bool | str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Lien",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=False,
    )
    wondrous: bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Magique",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=False,
    )
    data: Optional[ItemData] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Données",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default=None,
    )
    tags: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Tags",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(12,),
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata(in_file=False),
        },
        default=None,
    )

    DATA_FOLDER = Path("items")
    modelname = "Item"
    export_options = [ExportOption.RULES]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, text: str) -> "ItemModel":
        """Désérialise un ItemModel depuis JSON en instanciant le bon type de ItemData."""
        try:
            data = json.loads(text)

            # Traiter les champs énumérés
            hints = get_type_hints(cls)

            for field_name, value in data.items():
                if value is None:
                    continue

                if field_name in hints:
                    field_type = hints[field_name]

                    # Gérer Optional[T] et Union
                    origin = get_origin(field_type)
                    if origin is not None:
                        args = get_args(field_type)
                        # Pour Optional et Union, prendre le premier type non-None
                        field_type = next(
                            (t for t in args if t is not type(None)), args[0]
                        )

                    # Traiter les enums (ItemType, Rarity)
                    if isinstance(field_type, type) and issubclass(field_type, Enum):
                        data[field_name] = field_type[value]  # Accès par nom d'enum

            # Gérer le polymorphisme du champ 'data'
            if "data" in data and data["data"] is not None and "item_type" in data:
                item_type_enum = data["item_type"]
                data_dict = data["data"]

                # Obtenir la classe ItemData depuis l'enum
                data_class = item_type_enum.data_class

                # Instancier le bon type de données
                if data_class and data_class != ItemData:
                    data["data"] = data_class(**data_dict)

            return cls(**data)
        except Exception as e:
            print(f"Erreur lors de la désérialisation {cls.__name__}: {text}")
            raise e


WeaponMastery.collection = BaseCollection(DataRepository.load_all(WeaponMastery))
ItemModel.collection = BaseCollection(DataRepository.load_all(ItemModel))