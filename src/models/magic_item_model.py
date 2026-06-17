from src.models.item_model import *
from src.models.conceptual_models import *

class MagicItemType(Enum):
    WONDEROUS_ITEM="Objet merveilleux"
    GENERIC_VARIANT="variant générique"

@dataclass(kw_only=True)
class MagicItemModel(ItemModel):
    item_type: ItemType|MagicItemType = field(
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
        default=Rarity.COMMON,
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
    bonusWeaponDamage: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus aux dégâts de l'arme",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    bonusWeaponAttack: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à l'attaque avec l'arme",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    bonusMagicAttack: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à l'attaque des sorts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    bonusMagicDC: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus au DD avec des sorts",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    bonusAC: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Bonus à la CA",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    charges: Optional[int] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nombre de charge (max)",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    recharge: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Moment de la recharge",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    rechargeAmount: Optional[str] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Quantité de recharge",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    light: Optional[list[dict[str, int]]] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Lumière",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default=None
    )
    variants: Optional[dict[ItemModel, 'MagicItemModel']] = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Variations",
                filter_type=FilterOption.NONE,
                visibility=VisibilityOption.ALWAYS_HIDDEN
            ),
            JsonMixin.METADATA_NAMESPACE: JsonMetadata()
        },
        default_factory=list
    )

