import pytest, json

from src.models.item_model import ItemModel, ItemType, Rarity, WeaponDetails, ArmorDetails, VehicleDetails
from src.models.base import BaseModel
from src.models.mixins import JsonMixin, ExplorableMixin, PopupMixin, ExportableMixin

# === TestItemModel ===
class TestItemModel:
    def setup_method(self):
        self.item_model = ItemModel(
            name="Matériel d'alchimiste",
            item_type=ItemType.TOOL,
            rarity=Rarity.NONE,
            weight=4,
            value_cp=5000,
            entries=["<strong>Caractéristique :</strong> Intelligence",
                     "<strong>Utilisation :</strong> identifier une substance (DD 15), allumer un feu (DD 15)",
                     "<strong>Artisanat :</strong> acide, feu grégeois, huile, papier, parfum, sacoche à composantes"
            ],
            source="PHB"
        )

        self.weapon_model = ItemModel(
            name="Bâton de combat",
            item_type=ItemType.MELEE_WEAPON,
            rarity=Rarity.NONE,
            weight=2,
            value_cp=20,
            entries=[],
            weapon=WeaponDetails(
                damage_dice="1d6",
                damage_type="contondants",
                weapon_category="courante",
                properties=[
                    "P"
                ],
                range="1,5 m",
                damage_dice_2h="1d8"
            ),
            source="PHB"
        )

        self.armor_model = ItemModel(
            name="Cotte de mailles",
            item_type=ItemType.HEAVY_ARMOR,
            rarity=Rarity.NONE,
            weight=27.5,
            value_cp=7500,
            entries=[],
            armor=ArmorDetails(
                ac_base=16,
                stealth_disadvantage=True,
                min_strength=13,
                dex_ac_mod_cap=0
            ),
            source="PHB"
        )

        self.vehicle_model = ItemModel(
            name="Cheval de selle",
            item_type=ItemType.MOUNT,
            weight=0,
            value_cp=7500,
            entries=[],
            vehicle=VehicleDetails(
                speed=18,
                cap_passengers=1,
                cap_cargo_tons=0.24,
                hp=13,
                ac=11,
                min_damage_cap=0
            ),
            source="PHB"
        )

        self.instances = [self.item_model, self.weapon_model, self.armor_model, self.vehicle_model]

    # Test: superclasses
    def test_is_subclass_of_BaseModel(self):
        assert issubclass(ItemModel, BaseModel)

    def test_is_subclass_of_JsonMixin(self):
        assert issubclass(ItemModel, JsonMixin)

    def test_is_subclass_of_ExplorableMixin(self):
        assert issubclass(ItemModel, ExplorableMixin)

    def test_is_subclass_of_PopupMixin(self):
        assert issubclass(ItemModel, PopupMixin)

    def test_is_subclass_of_ExportableMixin(self):
        assert issubclass(ItemModel, ExportableMixin)

    # Test: JsonMixin
    def test_json_mixin_to_json_returns_a_string(self):
        """Test: to_json should return a string"""
        for item in self.instances:
            json_result = item.to_json()
            assert isinstance(json_result, str)
            assert len(json_result) > 0

    def test_json_mixin_from_json_creates_instance(self):
        """Test: from_json should create a correct instance"""
        for item in self.instances:
            # Arrange
            json_str = item.to_json()

            # Act
            restored_instance = ItemModel.from_json(json_str)

            # Assert
            assert restored_instance.name == item.name
            assert restored_instance.item_type == item.item_type
            assert restored_instance.source == item.source

    def test_json_mixin_roundtrip(self):
        """Test: to_json -> from_json create a identical double"""
        for item in self.instances:
            # Act
            json_str = item.to_json()
            restored = ItemModel.from_json(json_str)
            json_str_2 = restored.to_json()

            # Assert
            assert json_str == json_str_2

    # ExplorableMixin
    def test_explorable_mixin_metadata(self):
        """Test: ExplorableMixin gives metadata"""
        # Arrange
        fields = ItemModel.__dataclass_fields__

        # Assert : check that all fields have metadata
        assert "explorer" in fields["name"].metadata or "popup" in fields["name"].metadata

    # PopupMixin
    def test_popup_mixin_has_popup_window_class(self):
        """Test: PopupMixin defines popup_window_class"""
        # Assert
        assert hasattr(ItemModel, "popup_window_class")
        assert ItemModel.popup_window_class is not None

    def test_popup_mixin_get_popup_window_class(self):
        """Test: get_popup_window_class returns a popup_window_class"""
        # Act
        window_class = ItemModel.get_popup_window_class()

        # Assert
        from src.ui.details_windows.generic_detail_window import GenericDetailWindow
        assert window_class == GenericDetailWindow

    # SourcedModel
    def test_sourced_model_has_source_attribute(self):
        """Test: SourcedModel add the source attribute"""
        # Assert
        assert hasattr(self.item_model, "source")
        assert self.item_model.source == "PHB"

    def test_sourced_model_source_persists_in_json(self):
        """Test: the source attribute is serialized in the json ouput"""
        # Arrange
        json_str = self.item_model.to_json()

        # Assert
        assert "PHB" in json_str
        assert '"source"' in json_str

    # === Tests: Attributes metadata ===
    def test_field_metadata_has_labels(self):
        """Test: all fields have labels"""
        fields = ItemModel.__dataclass_fields__
        for field_name, field in fields.items():
            if field_name != "source":
                assert ExplorableMixin.METADATA_NAMESPACE in field.metadata, f"Champ {field_name} n'a pas de label"

    def test_field_metadata_visibility(self):
        """Test: all attributes have visibility properties"""
        # Arrange
        fields = ItemModel.__dataclass_fields__
        name_field = fields["name"]

        # Assert
        assert hasattr(name_field.metadata[ExplorableMixin.METADATA_NAMESPACE], "visibility")