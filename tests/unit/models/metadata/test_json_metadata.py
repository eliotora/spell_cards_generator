import pytest

from src.models.metadata.json_metadata import JsonMetadata

# ===== JsonMetadata =====
def test_json_metadata_in_file_default_value():
    meta = JsonMetadata()
    assert meta.in_file is True