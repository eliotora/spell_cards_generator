from dataclasses import dataclass, field, fields, MISSING
import itertools
from pathlib import Path
from typing import Any, Optional, get_type_hints, get_origin
import locale
from enum import Enum
from src.models.base import BaseModel
from src.models.collections.base_collection import BaseCollection
from src.models.metadata import (
    ExplorerMetadata,
    FilterOption,
    VisibilityOption,
    SortingKeys,
    JsonMetadata,
)
from src.models.metadata.popup_metadata import PopupMetadata
from src.models.mixins import ExplorableMixin, ExportableMixin, PopupMixin, JsonMixin
from src.models.mixins.exportable_mixin import ExportOption
from src.models.repositories.data_repository import DataRepository
from src.models.conceptual_models import MoneyQuantity
from src.ui.details_windows.generic_popup_window import GenericPopupWindow
from src.ui.rich_text_editor import RichTextEditor

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
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    entries: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,),
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(in_file=False),
        },
        default=None,
    )
    name_format: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Format de nom",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        },
        default="{name}",
    )
    extra_fields: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Champs supplémentaires",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )

    DATA_FOLDER = Path("masteries")
    modelname = "Weapon Mastery"

    def __str__(self) -> str:
        return f"{self.name}"


@dataclass
class MasteryData:
    mastery: WeaponMastery
    extras: dict[str, Any]

    def __str__(self) -> str:
        extras = {}
        for f in self.mastery.extra_fields:
            if f in self.extras:
                extras[f] = self.extras[f]
            else:
                extras[f] = ""
        return self.mastery.name_format.format(name=self.mastery.name, **extras)

    @property
    def name(self) -> str:
        return self.mastery.name

    @property
    def entries(self) -> str:
        return self.mastery.entries


@dataclass
class WeaponProperty(BaseModel, PopupMixin, JsonMixin, ExplorableMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    description: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Description",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        }
    )
    name_format: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Format de nom",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        },
        default="{name}",
    )
    extra_fields: list[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Champs supplémentaires",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(),
        },
        default_factory=list,
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(2,),
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(in_file=False),
        },
        default=None,
    )

    DATA_FOLDER = Path("weaponproperties")
    modelname = "Weapon Properties"

    def __str__(self) -> str:
        return f"{self.name}\n{self.description}"


@dataclass
class PropertyData:
    property: WeaponProperty
    extras: dict[str, Any]

    def __str__(self) -> str:
        extras = {}
        for f in self.property.extra_fields:
            if f in self.extras:
                extras[f] = self.extras[f]
            else:
                extras[f] = ""
        return self.property.name_format.format(name=self.property.name, **extras)


# ─────────────────────────────────────────────
# Enums / shared types
# ─────────────────────────────────────────────
class ItemType(Enum):
    WEAPON = ("arme", [])
    ARMOR = ("armure", [])
    SHIELD = ("bouclier", [])
    GEAR = ("équipement", [])
    ARTISAN_TOOL = (
        "outils d'artisan",
        [
            (
                "Outils d'artisan",
                "Les outils d'artisan sont tous axés sur la fabrication d'objets et l'exercice d'un métier. Chacun nécessite une maîtrise distincte.",
            )
        ],
    )
    TOOL = (
        "outil",
        [("Outil", "Ces outils sont utiles à l'aventure et à d'autres activités")],
    )
    VEHICLE_LAND = ("véhicule terrestre", [])
    VEHICLE_WATER = ("véhicule aquatique", [])
    VEHICLE_AIR = ("véhicule volant", [])
    MOUNT = ("monture", [])
    AMMUNITION = ("munition", [])

    def __str__(self):
        return self.value[0]

    def get_entries(self):
        return self.value[1]

    def __lt__(self, other):
        if isinstance(other, Enum):
            return self.name < other.name
        elif isinstance(other, str):
            return self.name < other
        else:
            raise ValueError(f"Cannot compare ItemType with {other.__class__.__name__}")

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            raise ValueError(f"Cannot compare ItemType with {other.__class__.__name__}")


class Rarity(Enum):
    MUNDANE = ("mundane", 0)
    COMMON = ("commun", 10000)
    UNCOMMON = ("peu courant", 40000)
    RARE = ("rare", 400000)
    VERY_RARE = ("très rare", 4000000)
    LEGENDARY = ("légendaire", 20000000)
    ARTIFACT = ("artéfact", None)
    VARIES = ("variable", 0)  # group of generic items (ex: +1 weapon)

    def __str__(self):
        return self.value[0]

    @property
    def price_modifier(self):
        return MoneyQuantity(self.value[1])

    def __lt__(self, other):
        if isinstance(other, Enum):
            return self.name < other.name
        elif isinstance(other, str):
            return self.name < other
        else:
            raise ValueError(f"Cannot compare Rarity with {other.__class__.__name__}")


# ─────────────────────────────────────────────
# ItemTypes
# ─────────────────────────────────────────────
@dataclass
class BaseData:
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BaseData":
        mendatory_fields = [
            f
            for f in fields(cls)
            if f.default is MISSING and f.default_factory is MISSING
        ]

        if any([f.name not in data for f in mendatory_fields]):
            raise ValueError(
                f"Field missing for item {data} in initialization of {cls.__name__}"
            )

        return cls(**data)

    def add_tags(self, tags: set[str]):
        pass


@dataclass
class WeaponData(BaseData):
    damage_dice: str
    damage_type: str
    category: str
    ranged: bool
    properties: list[PropertyData] = field(default_factory=list)
    mastery: Optional[MasteryData] = None
    entries: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        damage = f"{self.damage_dice} {self.damage_type}"
        type = self.weapontype
        p = ", ".join(str(prop) for prop in self.properties)
        m = f"Botte d'arme: {str(self.mastery)}"
        e = "\n".join(self.entries) if self.entries else None

        return "\n".join(i for i in [type, damage, p, m, e] if i)

    @property
    def weapontype(self) -> str:
        return f"{self.category.capitalize()} {"à distance" if self.ranged else "de corps à corps"}"

    def get_entries(self) -> list[tuple[str, str]]:
        res = []
        if self.entries:
            for e in self.entries:
                res.append(("", e))
        for p in self.properties:
            res.append((p.property.name, p.property.description))
        if self.mastery:
            res.append(
                (f"Botte d'arme: {self.mastery.name}", "\n".join(self.mastery.entries))
            )
        return res

    def get_data_text(self):
        res = f"{self.damage_dice} {self.damage_type}"
        if self.properties:
            res += f"\n{", ".join(str(p) for p in self.properties)}"
        if self.mastery:
            res += f"\nBotte d'arme: {self.mastery}"
        return res

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WeaponData":
        # Link mastery instance
        mastery_name = data.pop("mastery")
        if mastery_name:
            if isinstance(mastery_name, str):
                mastery_name = {"name": mastery_name}
            mastery_item = WeaponMastery.collection.get_by_field(
                "name", mastery_name.pop("name")
            )
            mastery_data = MasteryData(mastery_item, mastery_name)
            data["mastery"] = mastery_data
        else:
            data["mastery"] = None

        properties = data.pop("properties", [])
        # Link properties and make data
        for i, p in enumerate(properties):
            property_name = p.pop("name")
            property_type = WeaponProperty.collection.get_by_field(
                "name", property_name
            )
            if not property_type:
                print(property_name)
            property_data = PropertyData(property_type, p)
            properties[i] = property_data
        data["properties"] = properties

        return super().from_dict(data)

    def add_tags(self, tags):
        tags = tags | {
            self.category,
            "Arme à distance" if self.ranged else "Arme de corps à corps",
        }


@dataclass
class ArmorData(BaseData):
    ac_base: int
    category: str
    stealth_disadvantage: bool = False
    min_strength: Optional[int] = None
    dex_ac_mod_cap: Optional[int] = None

    def get_entries(self) -> list[tuple[str | None, str]]:
        res = []
        if self.stealth_disadvantage:
            res.append(
                (
                    None,
                    "Le porteur subit le Désavantage à ses tests de Dextérité (Discrétion)",
                )
            )
        if self.min_strength:
            res.append(
                (
                    None,
                    "L'armure réduit la Vitesse du porteur de 3 m si celui-ci n'est pas doté d'une valeur de Force au moins égale au nombre indiqué",
                )
            )
        return res

    def get_data_text(self) -> str:
        res = f"CA {"{0:+}".format(self.ac_base) if self.category.lower() == "bouclier" else self.ac_base}"
        if self.category.lower() != "bouclier":
            if self.dex_ac_mod_cap is None:
                res += " + Dex"
            elif self.dex_ac_mod_cap > 0:
                res += f" + Dex (max {self.dex_ac_mod_cap})"
        return res

    def add_tags(self, tags):
        tags.add(self.category)


@dataclass
class ToolData(BaseData):
    stat: str
    usage: str
    craft: Optional[str] = None

    def get_entries(self) -> list[tuple[str, str]]:
        res = [
            ("Caractéristique", f"{self.stat}"),
            ("Utilisation", f"{self.usage}"),
        ]
        if self.craft:
            res += [("Artisanat", f"{self.craft}")]
        res += [
            (
                None,
                "Si vous avez la maîtrise d'un outil, ajoutez votre bonus de maîtrise aux tests de caractéristique correspondants. Si vous avez la maîtrise d'une compétence associée à ce test, vous avez en outre l'Avantage au test.",
            )
        ]
        return res


@dataclass
class MountData(BaseData):
    carrying_capacity_kg: float = 0
    speed: float = 0
    profile_name: str = None

    def get_entries(self) -> list[tuple[str, str]]:
        return []

    def get_data_text(self) -> str:
        res = f"{int(self.carrying_capacity_kg)} kg, {self.speed} m"
        return res


@dataclass
class VehicleData(BaseData):
    speed_km_h: float
    crew_min: int = 0
    cap_passengers: Optional[int] = 0
    cap_cargo_tons: Optional[float] = 0
    hp: Optional[int] = None
    ac: Optional[int] = None
    min_damage_cap: Optional[int] = None

    def get_entries(self) -> list[tuple[str, str]]:
        if self.crew_min > 0:
            return [
                (
                    "Vitesse",
                    "Un navire qui fait voile contre un vent fort se déplace à la moitié de sa Vitesse. En cas de calme plat (absence de vent), les bateaux ne peuvent pas naviguer à la voile et laa propulsion doit se faire à la rame. Barges et barques sont utilisées sur les lacs et les rivières. Si vous naviguez vers l'aval, ajoutez la Vitesse du courant (généralement 4,5 km par heure) à celle du véhicule. Il est impossible de naviguer à contre-courant à la seule force des rames, mais de tels véhicules peuvent être halés vers l'amont par des animaux de trait depuis la berge. Une barque peut être portée et pèse 50 kg.",
                ),
                (
                    "Équipage",
                    "Tout navire de plus fort gaberit qu'une marge ou une barque à besoin d'un équipage d'employés qualifiés (voir à \"Services\") pour fonctionner. L'effectif minimum d'employés qualifiés nécessaires à l'équipage d'un navire dépend de son type.",
                ),
                (
                    "Passagers",
                    "La table indique le nombre de passagers de taille P ou M qu'un bateau peut héberger dans les hamacs. Un bateau doté de cabines privées peut transporter cinq fois moins de passagers. Un passager paie généralement 5 pa par jour pour dormir dans un hamac, mais les prix sont susceptible de varier d'un navire à l'autre. Une petite cabine privée coûte généralement 2 po par jour.",
                ),
                (
                    "Seuil de dégâts",
                    "Si un véhicule présente un seuil de dégâts (cf. glossaire de règles), celui-ci figure sur la table",
                ),
                (
                    "Réparation de navire",
                    "Les réparations d'un navire endommagé s'effectuent lorsque la bateau est à quai. Réparer 1 point de vie nécessite 1 jour et coûte 20 po (matériaux et main-d'oeuvre). Si les réparations sont effectuées dans un endroit où matériaux et main-d'oeuvre qualifiée abondent, comme le chantier naval d'une grande ville, la durée et le coût des réparations sont réduits de moitié.",
                ),
            ]
        else:
            return []

    def get_data_text(self) -> str:
        res = f"Vitesse: {self.speed_km_h} km/h"
        if self.cap_cargo_tons or self.cap_passengers:
            res += f"\nCapacité: {", ".join([f"{int(self.cap_cargo_tons*1000)} kg", f"{self.cap_passengers} passagers"])}"
        caracs = [f"Équipage {self.crew_min}", f"CA {self.ac}", f"HP {self.hp}"]
        if self.min_damage_cap:
            caracs += [f"Seuil de dégâts {self.min_damage_cap}"]
        res += f"\n{", ".join(caracs)}"
        return res


@dataclass
class AmmunitionData(BaseData):
    quantity: int = 1
    storage: Optional[str] = None

    def get_entries(self) -> list[tuple[str, str]]:
        return []


# ─────────────────────────────────────────────
# ItemModel (base)
# ─────────────────────────────────────────────
@dataclass(unsafe_hash=True)
class ItemModel(BaseModel, ExplorableMixin, ExportableMixin, PopupMixin, JsonMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom",
                filter_type=FilterOption.LINE_EDIT,
                visibility=VisibilityOption.ALWAYS_VISIBLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=str),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Nom"),
        }
    )
    item_type: list[ItemType] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Type",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=list[ItemType]),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Type"),
        }
    )
    weight: float = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Poids",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=float),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Poids"),
        },
        default=0.0,
    )
    value_cp: MoneyQuantity = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Prix",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=int),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Prix"),
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
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=RichTextEditor),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Description"),
        },
        default_factory=list,
    )
    tags: set[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Tags",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=str),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Tags", hidden=True),
        },
        default_factory=set,
    )
    source: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Source",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                cols_to_hide=(12,),
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(in_file=False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Source"),
        },
        default=None,
    )

    weapon_data: Optional[WeaponData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="WeaponData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données arme"),
        },
    )
    armor_data: Optional[ArmorData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="ArmorData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données armure"),
        },
    )
    tool_data: Optional[ToolData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="ToolData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données outil"),
        },
    )
    mount_data: Optional[MountData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="MountData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données monture"),
        },
    )
    vehicle_data: Optional[VehicleData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="VehicleData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données véhicule"),
        },
    )
    ammunition_data: Optional[AmmunitionData] = field(
        default=None,
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="AmmunitionData",
                visibility=VisibilityOption.ALWAYS_HIDDEN,
                filter_type=FilterOption.NONE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(False),
            PopupMixin.METADATA_NAMESPACE: PopupMetadata(label="Données munition"),
        },
    )

    DATA_FOLDER = Path("items")
    modelname = "Item"
    export_options = [ExportOption.RULES]
    popup_window_class = GenericPopupWindow

    def __post_init__(self):
        for data in [
            self.weapon_data,
            self.armor_data,
            self.tool_data,
            self.mount_data,
            self.vehicle_data,
            self.ammunition_data,
        ]:
            data: BaseData
            if data:
                data.add_tags(self.tags)
        if len(self.tags) == 0:
            self.tags = self.tags | {*[str(t).capitalize() for t in self.item_type]}

    def __str__(self) -> str:
        header = [self.name, self.source]
        types = [f"*{str(self.item_type).capitalize()}*"]
        infos = [self.value_cp, self.weight]
        entries = [*self.entries]
        return self.name

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ItemModel":
        """Désérialise un ItemModel depuis JSON en instanciant le bon type de ItemData."""
        # Traiter les champs énumérés
        hints = get_type_hints(cls)

        for field_name, value in data.items():
            if value is None:
                continue

            if field_name in hints:
                try:
                    field_type = hints[field_name]

                    try:
                        alt_compute = cls.data_to_field(value, field_type)
                    except Exception as e:
                        print(
                            f"Field was {field_name}; expected type: {field_type}; value: {value}"
                        )
                        raise e
                    data[field_name] = alt_compute
                except Exception as e:
                    print(field_name, value)
                    raise e

        return cls(**data)

    @classmethod
    def data_to_field(cls, data, expected_type):
        origin = get_origin(expected_type)
        if (
            origin is None
            and issubclass(expected_type, BaseData)
            and isinstance(data, dict)
        ):
            return expected_type.from_dict(data)
        return super().data_to_field(data, expected_type)

    def get_entries(self) -> list[tuple[str, str]]:
        res = []
        if self.entries and len(self.entries) > 0:
            res.append((None, f"<p>{self.entries[0]}</p>"))
            for e in self.entries[1:]:
                res.append((None, f"<p style='text-indent: 15px;'>   {e}</p>"))
        for t in self.item_type:
            res += t.get_entries()
        for data in [
            self.weapon_data,
            self.armor_data,
            self.tool_data,
            self.ammunition_data,
            self.mount_data,
            self.vehicle_data,
        ]:
            if data:
                res = res + data.get_entries()
        return res


@dataclass(kw_only=True, unsafe_hash=True)
class WeaponModel(ItemModel):
    """Wrapper to create weapon easily"""

    modelname = "Weapon"
    DATA_FOLDER = Path("items") / Path("weapons")

    def __post_init__(self):
        self.tags.add(self.weapon_data.category.capitalize())
        self.tags.add(
            f"Arme {"à distance" if self.weapon_data.ranged else "de corps à corps"}"
        )
        super().__post_init__()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WeaponModel":
        # Link mastery instance
        mastery_name = data.pop("mastery")
        if isinstance(mastery_name, str):
            mastery_name = {"name": mastery_name}
        mastery_item = WeaponMastery.collection.get_by_field(
            "name", mastery_name.pop("name")
        )
        mastery_data = MasteryData(mastery_item, mastery_name)

        properties = data.pop("properties", [])
        # Link properties and make data
        for i, p in enumerate(properties):
            property_name = p.pop("name")
            property_type = WeaponProperty.collection.get_by_field(
                "name", property_name
            )
            if not property_type:
                print(property_name)
            property_data = PropertyData(property_type, p)
            properties[i] = property_data

        weapon_data = WeaponData(
            damage_dice=data.pop("damage_dice"),
            damage_type=data.pop("damage_type"),
            category=data.pop("category"),
            ranged=data.pop("ranged", False),
            properties=properties,
            mastery=mastery_data,
            entries=data.pop("entries", None),
        )

        data["weapon_data"] = weapon_data
        return super().from_dict(data)


@dataclass(kw_only=True, unsafe_hash=True)
class GearModel(ItemModel):
    modelname = "Adventurer's Gear"
    DATA_FOLDER = Path("items") / Path("gear")


@dataclass(kw_only=True, unsafe_hash=True)
class ArmorModel(ItemModel):
    modelname = "Armor"
    DATA_FOLDER = Path("items") / Path("armors")

    def __post_init__(self):
        self.tags.add(self.armor_data.category.capitalize())
        super().__post_init__()

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        armor_data = ArmorData(
            ac_base=data.pop("ac_base"),
            category=data.pop("category"),
            stealth_disadvantage=data.pop("stealth_disadvantage", False),
            min_strength=data.pop("min_strength", None),
            dex_ac_mod_cap=data.pop("dex_ac_mod_cap", None),
        )
        data["armor_data"] = armor_data
        return super().from_dict(data)


@dataclass(kw_only=True, unsafe_hash=True)
class ToolModel(ItemModel):
    modelname = "Tool"
    DATA_FOLDER = Path("items") / Path("tools")

    def __post_init__(self):
        if len(self.tags) == 0:
            self.tags.add(*[str(t).capitalize() for t in self.item_type])
        super().__post_init__()

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        tool_data = ToolData(
            stat=data.pop("stat"),
            usage=data.pop("usage"),
            craft=data.pop("craft", None),
        )
        data["tool_data"] = tool_data
        return super().from_dict(data)


@dataclass(kw_only=True, unsafe_hash=True)
class MountModel(ItemModel):
    modelname = "Mount"
    DATA_FOLDER = Path("items") / Path("mounts")

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        mount_data = MountData(
            carrying_capacity_kg=data.pop("carrying_capacity_tons", 0),
            speed=data.pop("speed", 0),
            profile_name=data.pop("profile_name", None),
        )
        data["mount_data"] = mount_data
        return super().from_dict(data)


@dataclass(kw_only=True, unsafe_hash=True)
class VehicleModel(ItemModel):
    modelname = "Vehicle"
    DATA_FOLDER = Path("items") / Path("vehicles")

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        vehicle_data = VehicleData(
            speed_km_h=data.pop("speed_km_h"),
            crew_min=data.pop("crew_min"),
            cap_passengers=data.pop("cap_passengers", 0),
            cap_cargo_tons=data.pop("cap_cargo_tons", 0),
            hp=data.pop("hp", None),
            ac=data.pop("ac", None),
            min_damage_cap=data.pop("min_damage_cap", None),
        )
        data["vehicle_data"] = vehicle_data
        return super().from_dict(data)


@dataclass(kw_only=True, unsafe_hash=True)
class AmmunitionModel(ItemModel):
    modelname = "Ammunitions"
    DATA_FOLDER = Path("items") / Path("ammunitions")

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        ammunition_data = AmmunitionData(
            quantity=data.pop("quantity", 1),
            storage=data.pop("storage", None),
        )
        data["ammunition_data"] = ammunition_data
        return super().from_dict(data)


import time

start = time.time()
print(f"Start loading weapon metadata")
WeaponProperty.collection = BaseCollection(DataRepository.load_all(WeaponProperty))
WeaponMastery.collection = BaseCollection(DataRepository.load_all(WeaponMastery))
print(f"Weapon metadata loaded in {time.time() - start} seconds")

# Items
start = time.time()
print(f"Start loading items")
WeaponModel.collection = BaseCollection(DataRepository.load_all(WeaponModel))
GearModel.collection = BaseCollection(DataRepository.load_all(GearModel))
ArmorModel.collection = BaseCollection(DataRepository.load_all(ArmorModel))
ToolModel.collection = BaseCollection(DataRepository.load_all(ToolModel))
MountModel.collection = BaseCollection(DataRepository.load_all(MountModel))
VehicleModel.collection = BaseCollection(DataRepository.load_all(VehicleModel))
AmmunitionModel.collection = BaseCollection(DataRepository.load_all(AmmunitionModel))

other_item_collection = BaseCollection(DataRepository.load_all(ItemModel))

ItemModel.collection = BaseCollection(
    list(
        itertools.chain.from_iterable(
            [sc.collection for sc in ItemModel.__subclasses__()]
        )
    )
    + other_item_collection.items()
)
print(f"Items loaded in {time.time() - start} seconds")

# ItemModel.collection = BaseCollection(DataRepository.load_all(ItemModel))
