import pytest
from unittest.mock import MagicMock, patch
from copy import deepcopy
from dataclasses import dataclass

from src.models.generic_model import (
    ExportOption, FilterOption, VisibilityOption, ModelCollection, ExplorableModel
)

# -- Fixtures -------------------------------------------------------------------------------------

@dataclass
class FakeItem(ExplorableModel):
    name:str
    level: int = 1
    tags: list = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

def make_collection(items: list) -> type:
    """Crée une sous-classe de ModelCollection pré-chargée, sans toucher au FS."""
    class FakeCollection(ModelCollection):
        load_items_method = staticmethod(lambda path: deepcopy(items))
    # Reset le singleton entre chaque test
    if hasattr(FakeCollection, "instance"):
        del FakeCollection.instance
    FakeCollection() # déclenche __new__ et charge items
    return FakeCollection

# -- Generic item loading -------------------------------------------------------------------------

class TestLoadModelFromFolder:
    def setup_method(self):
        self.item = FakeItem(
            name="Aragorn", level=5
        )
        self.item


# -- ExportOption ---------------------------------------------------------------------------------

class TestExportOption:
    def test_from_string_minuscule(self):
        assert ExportOption.from_string("rules") == ExportOption.RULES

    def test_from_strong_majuscule(self):
        assert ExportOption.from_string("GRIMOIRE") == ExportOption.GRIMOIRE

    def test_from_string_valeur_inconnue_leve_erreur(self):
        with pytest.raises(KeyError):
            ExportOption.from_string("inexistant")

    def test_str_retourne_nom_en_minuscule(self):
        assert str(ExportOption.CARDS) == "cards"

# -- FirlterOption.value_in_filter ----------------------------------------------------------------

class TestFilterOptionValueInFilter:
    # --- LIST ---
    def test_list_valeur_presente(self):
        assert FilterOption.LIST.value_in_filter("guerrier", ["guerrier", "mage"]) is True

    def test_list_valeur_absente(self):
        assert FilterOption.LIST.value_in_filter("voleur", ["guerrier", "mage"]) is False

    def test_list_valeur_est_une_liste_avec_intersection(self):
        # La valeur est elle-même une liste
        assert FilterOption.LIST.value_in_filter(["feu", "terre"], ["feu"]) is True

    def test_list_valeur_est_une_liste_sans_intersection(self):
        assert FilterOption.LIST.value_in_filter(["eau", "vent"], ["feu"]) is False

    # --- INT_RANGE ---
    def test_int_range_valeur_dans_intervalle(self):
        assert FilterOption.INT_RANGE.value_in_filter(5, [1, 10]) is True

    def test_int_range_valeur_sur_borne_basse(self):
        assert FilterOption.INT_RANGE.value_in_filter(1, [1, 10]) is True

    def test_int_range_valeur_sur_borne_haute(self):
        assert FilterOption.INT_RANGE.value_in_filter(10, [1, 10]) is True

    def test_int_range_valeur_hors_intervalle(self):
        assert FilterOption.INT_RANGE.value_in_filter(11, [1, 10]) is False

    def test_int_range_valeur_non_entiere_retourne_false(self):
        assert FilterOption.INT_RANGE.value_in_filter("cinq", [1, 10]) is False

    def test_int_range_filters_mal_forme_retourne_false(self):
        # filters dois avoir exactement 2 éléments
        assert FilterOption.INT_RANGE.value_in_filter(5, [1]) is False

    # --- LINE_EDIT ---
    def test_line_edit_valeur_presente_dans_texte(self):
        assert FilterOption.LINE_EDIT.value_in_filter("Boule de feu", ["boule"]) is True

    def test_line_edit_insensible_a_la_casse(self):
        assert FilterOption.LINE_EDIT.value_in_filter("Boule de feu", ["FEU"]) is True

    def test_line_edit_filtre_vide_retourne_true(self):
        # Filtre vide = pas de filtre actif -> Tout est visible
        assert FilterOption.LINE_EDIT.value_in_filter("sort", [""]) is True

    def test_line_edit_valeur_none_traitee_comme_chaine_vide(self):
        assert FilterOption.LINE_EDIT.value_in_filter(None, [""]) is True

    def test_line_edit_valeur_non_string_retourne_false(self):
        assert FilterOption.LINE_EDIT.value_in_filter(42, ["42"]) is False

# -- ModelCollection ------------------------------------------------------------------------------

class TestModelCollectionGetItem:
    def setup_method(self):
        items = [FakeItem(name="Aragorn"), FakeItem(name="Gandalf")]
        self.col = make_collection(items)

    def test_get_item_trouve_par_nom_exact(self):
        item = self.col.get_item("Aragorn")
        assert item is not None
        assert item.name == "Aragorn"

    def test_get_item_insensible_a_la_casse(self):
        item = self.col.get_item("aragorn")
        assert item is not None

    def test_get_item_retourne_none_si_inconnu(self):
        assert self.col.get_item("Frodon") is None

    def test_get_item_retourne_une_copie_profonde(self):
        item1 = self.col.get_item("Aragorn")
        item2 = self.col.get_item("Aragorn")
        item1.name = "Modifié"
        # La modification ne doit pas affecter la collection ni l'autre copie
        assert item2.name == "Aragorn"
        assert self.col.get_item("Aragorn").name == "Aragorn"


class TestModelCollectionGetItems:
    def setup_method(self):
        items = [FakeItem(name="Legolas"), FakeItem(name="Gimli")]
        self.col = make_collection(items)

    def test_get_items_retourne_tous_les_elements(self):
        assert len(self.col.get_items()) == 2

    def test_get_items_retourne_une_copie_profonde(self):
        items = self.col.get_items()
        name_save = deepcopy(items[0].name)
        items[0].name = "Modifié"
        # La collection interne ne doit pas être affectée
        assert self.col.get_items()[0].name == name_save

# -- ExplorableModel.to_dict ----------------------------------------------------------------------

class TestExplorableModelToDict:
    def test_to_dict_contient_tous_les_champs(self):
        item = FakeItem(name="Sauron", level=9, tags=["méchant"])
        d = item.to_dict()
        assert d == {"name": "Sauron", "level": 9, "tags": ["méchant"]}

    def test_to_dict_valeurs_par_defaut(self):
        item = FakeItem(name="Anonyme")
        d = item.to_dict()
        assert d["level"] == 1
        assert d["tags"] == []

