import pytest

from src.models.metadata.explorer_metadata import ExplorerMetadata, FilterOption, VisibilityOption

# ===== FilterOption =====
class TestFilterOption():
    def test_filter_option_from_string_valid(self):
        filter_option = FilterOption.from_string("list")
        assert filter_option == FilterOption.LIST

    def test_filter_option_from_string_invalid(self):
        with pytest.raises(ValueError):
            FilterOption.from_string("1234")

    def test_value_in_filter_list_to_list_true(self):
        assert FilterOption.LIST.value_in_filter(
            value=["d", "a"],
            filters=["a", "b", "c"]
        ) is True

    def test_value_in_filter_list_to_list_false(self):
        assert FilterOption.LIST.value_in_filter(
            value=["d"],
            filters=["a", "b", "c"]
        ) is False

    def test_value_in_filter_list_to_value_true(self):
        assert FilterOption.LIST.value_in_filter(
            value="a",
            filters=["a", "b", "c"]
        ) is True

    def test_value_in_filter_list_to_value_false(self):
        assert FilterOption.LIST.value_in_filter(
            value="d",
            filters=["a", "b", "c"]
        ) is False

    def test_value_in_filter_int_range_true(self):
        assert FilterOption.INT_RANGE.value_in_filter(
            value=5,
            filters=[1, 9]
        ) is True

    def test_value_in_filter_int_range_false(self):
        assert FilterOption.INT_RANGE.value_in_filter(
            value=0,
            filters=[1, 9]
        ) is False

    def test_value_in_filter_int_range_edge_case(self):
        assert FilterOption.INT_RANGE.value_in_filter(
            value=1,
            filters=[1, 9]
        ) is True
        assert FilterOption.INT_RANGE.value_in_filter(
            value=9,
            filters=[1, 9]
        ) is True

    def test_value_in_filter_line_edit_true(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="Boule de feu",
            filters=["feu"]
        ) is True

    def test_value_in_filter_line_edit_false(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="Boule de feu",
            filters=["Trait"]
        ) is False

    def test_value_in_filter_line_edit_caps(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="Boule de feu",
            filters=["FEU"]
        ) is True
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="Boule de feu",
            filters=["boule"]
        ) is True

    def test_value_in_filter_line_edit_non_ascii_char(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="À terre",
            filters=["À"]
        ) is True
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="À terre",
            filters=["à"]
        ) is True
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="À terre",
            filters=["a"]
        ) is True

    def test_value_in_filter_line_edit_none(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="À terre",
            filters=[""]
        ) is True

    def test_value_in_filter_line_edit_multiple(self):
        assert FilterOption.LINE_EDIT.value_in_filter(
            value="À terre",
            filters=["Boule", "terre"]
        ) is True

# ===== VisibilityOption =====
class TestVisibilityOption():
    def test_filter_option_from_string_valid(self):
        filter_option = FilterOption.from_string("list")
        assert filter_option == FilterOption.LIST

    def test_filter_option_from_string_invalid(self):
        with pytest.raises(ValueError):
            FilterOption.from_string("1234")


# ===== ExplorerMetadata =====
def test_explorer_metadata_cols_to_hide_init_value():
    meta = ExplorerMetadata(
        label = "nom",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.ALWAYS_VISIBLE
    )
    assert meta.cols_to_hide == ()