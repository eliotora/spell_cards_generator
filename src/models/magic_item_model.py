from src.models.item_model import *
from src.models.conceptual_models import *

from typing import Union
from copy import deepcopy
from dataclasses import asdict


class MagicItemType(Enum):
    RING = ("anneau", [])
    WAND = ("baguette", [])
    STAFF = ("bâton", [])
    WONDEROUS_ITEM = ("Objet merveilleux", [])
    SCROLL = ("parchemin", [])
    POTION = ("potion", [])
    ROD = ("sceptre", [])
    GENERIC_VARIANT = ("variant générique", [])

    def __str__(self) -> str:
        return self.value[0]

    def __lt__(self, other):
        if isinstance(other, Enum):
            return self.name < other.name
        elif isinstance(other, str):
            return self.name < other
        else:
            raise ValueError(
                f"Cannot compare MagicItemType with {other.__class__.__name__}"
            )

    def get_entries(self):
        return self.value[1]


@dataclass(kw_only=True)
class MagicItemModel(ItemModel):
    item_type: list[MagicItemType | ItemType] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Type",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=list[MagicItemType|ItemType]),
        }
    )
    rarity: Rarity = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Rareté",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(form_type=list[Rarity]),
        },
        default=Rarity.COMMON,
    )
    requires_attunement: str | bool = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Lien",
                filter_type=FilterOption.LIST,
                visibility=VisibilityOption.HIDDABLE,
                sorting_key=SortingKeys.STR_BOOL
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=bool
            ),
        },
        default=False,
    )
    requires_attunement_tags: Optional[list[dict[str, str]]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Tags lien",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            ),
        },
        default_factory=list,
    )
    bonusWeaponDamage: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus aux dégâts de l'arme",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    bonusWeaponAttack: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à l'attaque avec l'arme",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    bonusMagicAttack: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à l'attaque des sorts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    bonusMagicDC: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus au DD avec des sorts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    bonusAC: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à la CA",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    bonusSaves: Optional[list[dict]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus aux jets de sauvegarde",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default_factory=list,
    )
    bonusAbilityCheck: Optional[list[dict]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus aux jets de tests de compétence",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default_factory=list,
    )
    resists: Optional[list[str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Résistances octroyées",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=list
            ),
        },
        default=list,
    )
    immunities: Optional[list[str]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Immunités octroyées",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=list
            ),
        },
        default=list,
    )
    charges: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nombre de charge (max)",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=int
            ),
        },
        default=None,
    )
    recharge: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Moment de la recharge",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            ),
        },
        default=None,
    )
    rechargeAmount: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Quantité de recharge",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            ),
        },
        default=None,
    )
    light: Optional[list[dict[str, int]]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Lumière",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            ),
        },
        default=None,
    )
    variants: Optional[
        dict[str, Union[str, "MagicItemModel"]]
        | set[Union[str, "MagicItemModel"]]
    ] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Variations",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN,
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            ),
        },
        default_factory=dict,
    )
    applies_to: Optional[list[dict]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="S'applique à",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            )
        },
        default_factory=list
    )
    requires_mastery: Optional[dict] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="S'applique à",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMetadata.METADATA_NAMESPACE: JsonMetadata(
                form_type=str
            )
        },
        default_factory=list
    )

    modelname = "MagicItem"
    DATA_FOLDER = Path("items") / Path("magic")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MagicItemModel":
        base = data.pop("base", None)
        if base:
            item_base: ItemModel = ItemModel.collection.get_by_field("name", base)
            if not item_base:
                raise ValueError(f"A base ({base}) was given but no item with that name where found")

            for field in fields(ItemModel):
                if field.name not in data:
                    if field.name == "value_cp":
                        if "value_cp" in data:
                            new_val = item_base.value_cp + data["value_cp"]
                        else:
                            new_val = item_base.value_cp + Rarity[data["rarity"]].price_modifier
                    else:
                         new_val = deepcopy(getattr(item_base, field.name))
                    data[field.name] = new_val

        variants = data.pop("variants", None)
        if isinstance(variants, list):
            data["variants"] = set(variants)
        elif isinstance(variants, dict):
            data["variants"] = variants

        if "value_cp" not in data and "rarity" in data:
            # Put default value from rarity
            data["value_cp"] = Rarity[data["rarity"]].price_modifier

        i_type = data.pop("item_type")
        if isinstance(i_type, str):
            i_type = [i_type]
        for i, t in enumerate(i_type):
            if isinstance(t, MagicItemType) or isinstance(t, ItemType): continue
            if t in MagicItemType._member_names_:
                i_type[i] = MagicItemType[t]
            elif t in ItemType._member_names_:
                i_type[i] = ItemType[t]
        data["item_type"] = i_type
        item: MagicItemModel = super().from_dict(data)
        generated_variants = item._create_variants()
        if generated_variants: item.variants = generated_variants
        return item

    def get_entries(self):
        res = []
        if self.bonusAC:
            res.append(
                (
                    None,
                    f"Lorsque vous portez cette armure, vous gagnez un vonus de {self.bonusAC} à la CA.",
                )
            )
        # if self.bonusWeaponAttack: res.append()
        res += super().get_entries()
        if self.variants:
            if isinstance(self.variants, set):
                variant_list = [f"<a href='MagicItem/{v}'>{v}</a>" for v in sorted(list(self.variants))]
            elif isinstance(self.variants, dict):
                variant_list = [f"<a href=\"item/{k}\">{k}</a>: <a href=\"MagicItem/{v}\">{v}</a>" for k, v in self.variants.items()]
            res.append(
                (
                    None,
                    f"Plusieurs variantes de cet objet existent, comme listées ci-après:<br>{"<br>".join(variant_list)}",
                )
            )
        return res

    def _create_variants(self):
        if not (MagicItemType.GENERIC_VARIANT in self.item_type and self.applies_to):
            return

        qual_items: dict[str, ItemModel] = {}
        for grp in self.applies_to:
            if "model_name" and grp["model_name"] == "Item":
                filtered = ItemModel.collection.filter(grp["filter"])
                for item in filtered.items():
                    qual_items[item.name] = item

        for name, item in qual_items.items():
            qual_items[name] = self.__class__.from_generic(self, item)

        return qual_items

    @classmethod
    def from_generic(cls, generic_variant: 'MagicItemModel', base: ItemModel) -> 'MagicItemModel':
        base_dict = asdict(base)
        base_dict = {}
        for f in fields(base):
            base_dict[f.name] = base.__getattribute__(f.name)
        base_dict["name"] = f"{base.name} ({generic_variant.name})"
        base_dict["entries"] += generic_variant.entries
        for f in fields(cls):
            if f.name == "value_cp":
                # Add item price and magic rarity price modifier
                base_dict["value_cp"] = base.value_cp + generic_variant.value_cp
                continue

            if f.name in base_dict or f.name in ["variants", "applies_to"]: continue

            base_dict[f.name] = deepcopy(generic_variant.__getattribute__(f.name))

        res = cls(**base_dict)
        return res



magic_item_collection = BaseCollection(DataRepository.load_all(MagicItemModel))
for magic_item in magic_item_collection.items():
    if MagicItemType.GENERIC_VARIANT in magic_item.item_type and magic_item.variants:
        if isinstance(magic_item.variants, dict):
            for name, item in magic_item.variants.items():
                if isinstance(item, MagicItemModel):
                    magic_item_collection.add(item)

MagicItemModel.collection = magic_item_collection