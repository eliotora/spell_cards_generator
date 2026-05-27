from dataclasses import dataclass, field
import pytest

from src.models.mixins.explorable_mixin import ExplorableMixin
from src.models.metadata.explorer_metadata import ExplorerMetadata, FilterOption, VisibilityOption


# ===== Fixtures =====

@dataclass
class FakeModel(ExplorableMixin):
    name: str = field(
        metadata={
            ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                label="Nom", filter_type=FilterOption.LINE_EDIT, visibility=VisibilityOption.ALWAYS_VISIBLE
            )
        }
    )
    level: int

# ===== ExplorableMixin =====

class TestExplorableMixin:
    def test_explorer_fields(self):
        r = FakeModel.explorer_fields()
        assert len(r) == 1
        assert r[0][0].name == "name"

    def test_validate_metadata_raises(self):
        with pytest.raises(AttributeError):
            FakeModel.validate_metadata()

    def test_validate_metadata_not_raises(self):
        @dataclass
        class OKModel(ExplorableMixin):
            name: str = field(
                metadata={
                    ExplorableMixin.METADATA_NAMESPACE: ExplorerMetadata(
                        label="Nom", filter_type=FilterOption.LINE_EDIT, visibility=VisibilityOption.ALWAYS_VISIBLE
                    )
                }
            )
        try:
            OKModel.validate_metadata()
        except AttributeError as e:
            pytest.fail(e)

