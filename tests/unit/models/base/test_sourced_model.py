import pytest

from src.models.base.sourced_model import SourcedModel
from src.models.mixins.json_mixin import JsonMixin

# ===== SourcedModel =====

def test_sourced_model_init_no_value():
    """Source has init=False, so the attribute shouldn't exist if not given"""
    model = SourcedModel()

    assert hasattr(model, "source") is False

    # Should be ok when defined later
    model.source = "test"
    assert hasattr(model, "source") is True
    assert model.source == "test"


def test_sourced_model_has_json_metadata():
    """The source attribute should have a JsonMetadata namespace, and value in_file to False"""
    metadata = SourcedModel.__dataclass_fields__['source'].metadata

    assert metadata[JsonMixin.METADATA_NAMESPACE].in_file == False