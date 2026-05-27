import pytest, json

from src.models.spell_model import SpellModel
from src.models.base import BaseModel
from src.models.mixins import JsonMixin, ExplorableMixin, PopupMixin

# === TestSpellModel ===
class TestSpellModel:
    def setup_method(self):
        self.instance = SpellModel(
            source="PHB",
            name="Boule de feu",
            vf_name=None,
            vo_name="Fireball",
            classes=["Ensorceleur", "Magicien"],
            schools=["évocation"],
            level=3,
            casting_time="action",
            range="45 m",
            components=["V", "S", "M (une boulette de guano de chauve-souris et de soufre)"],
            duration="instantanée",
            concentration=False,
            ritual=False,
            description="Une zébrure éblouissante jaillit de vous jusqu'au point que vous choisissez à portée, produisant une déflagration au grondement sourd. Chaque créature prise dans la Sphère de 6 m de rayon centrée sur ce point d'origine effectue un jet de sauvegarde de Dextérité et subit 8d6 dégâts de feu en cas d'échec, la moitié en cas de réussite.<br>L'explosion embrase les objets inflammables de la zone qui ne sont portés par personne.",
            short_description="Les créatures dans un rayon de 6 m doivent réussir un JdS de Dex. ou subir 8d6 dégâts de feu (dégâts/niv).",
            at_higher_levels="Les dégâts augmentent de 1d6 par niveau d'emplacement au-delà du 3e."
        )

    # Test: superclasses
    def test_is_subclass_of_BaseModel(self):
        assert issubclass(SpellModel, BaseModel)

    def test_is_subclass_of_JsonMixin(self):
        assert issubclass(SpellModel, JsonMixin)

    def test_is_subclass_of_ExplorableMixin(self):
        assert issubclass(SpellModel, ExplorableMixin)

    def test_is_subclass_of_PopupMixin(self):
        assert issubclass(SpellModel, PopupMixin)

    # Test: JsonMixin
    def test_json_mixin_to_json_returns_a_string(self):
        """Test: to_json should return a string"""
        json_result = self.instance.to_json()
        assert isinstance(json_result, str)
        assert len(json_result) > 0

    def test_json_mixin_from_json_creates_instance(self):
        """Test: from_json should create a correct instance"""
        # Arrange
        json_str = self.instance.to_json()

        # Act
        restored_instance = SpellModel.from_json(json_str)

        # Assert
        assert restored_instance.name == self.instance.name
        assert restored_instance.level == self.instance.level
        assert restored_instance.source == self.instance.source

    def test_json_mixin_roundtrip(self):
        """Test: to_json -> from_json creates a identical double"""
        # Act
        json_str = self.instance.to_json()
        restored = SpellModel.from_json(json_str)
        json_str_2 = restored.to_json()

        # Assert
        assert json_str == json_str_2

    # ExplorableMixin
    def test_explorable_mixin_metadata(self):
        """Test: ExplorableMixin gives metadata"""
        # Arrange
        fields = SpellModel.__dataclass_fields__

        # Assert : check that all fields have metadata
        assert "explorer" in fields["name"].metadata or "popup" in fields["name"].metadata

    # PopupMixin
    def test_popup_mixin_has_popup_window_class(self):
        """Test: PopupMixin defines popup_window_class"""
        # Assert
        assert hasattr(SpellModel, "popup_window_class")
        assert SpellModel.popup_window_class is not None

    def test_popup_mixin_get_popup_window_class(self):
        """Test: get_popup_window_class returns a popup_window_class"""
        # Act
        window_class = SpellModel.get_popup_window_class()

        # Assert
        from src.ui.details_windows.spell_detail_window import SpellDetailWindow
        assert window_class == SpellDetailWindow

    # SourcedModel
    def test_sourced_model_has_source_attribute(self):
        """Test: SourcedModel add the source attribute"""
        # Assert
        assert hasattr(self.instance, "source")
        assert self.instance.source == "PHB"

    def test_sourced_model_source_persists_in_json(self):
        """Test: the source attribute is serialized in the json ouput"""
        # Arrange
        json_str = self.instance.to_json()

        # Assert
        assert "PHB" in json_str
        assert '"source"' in json_str

    # === Tests: Attributes metadata ===
    def test_field_metadata_has_labels(self):
        """Test: all fields have labels"""
        fields = SpellModel.__dataclass_fields__
        for field_name, field in fields.items():
            if field_name != "source":
                assert ExplorableMixin.METADATA_NAMESPACE in field.metadata, f"Champ {field_name} n'a pas de label"

    def test_field_metadata_visibility(self):
        """Test: all attributes have visibility properties"""
        # Arrange
        fields = SpellModel.__dataclass_fields__
        name_field = fields["name"]

        # Assert
        assert hasattr(name_field.metadata[ExplorableMixin.METADATA_NAMESPACE], "visibility")

    # === Tests : Special cases ===
    def test_optional_fields_can_be_none(self):
        """Test: les champs optionnels peuvent être  None"""
        spell = SpellModel(
            source="Test",
            name="Test Spell",
            vf_name=None,
            vo_name=None,
            classes=[],
            schools=[],
            level=1,
            casting_time="action",
            range="self",
            components=["V"],
            duration="1 minute",
            concentration=False,
            ritual=False,
            description="Test",
            short_description=None,
            at_higher_levels=None
        )

        assert spell.vf_name is None
        assert spell.vo_name is None
        assert spell.short_description is None
        assert spell.at_higher_levels is None