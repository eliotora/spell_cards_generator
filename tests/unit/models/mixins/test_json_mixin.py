from dataclasses import dataclass
import pytest, json

from src.models.mixins.json_mixin import JsonMixin

# ===== Fixtures =====

@dataclass
class FakeModel(JsonMixin):
    name: str
    level: int

# ===== JsonMixin =====

class TestJsonMixin:
    def setup_method(self):
        self.raw_data = {
            "name": "Aragorn",
            "level": 5
        }
        self.json_data = json.dumps(self.raw_data)

        self.model = FakeModel(
            name=self.raw_data["name"],
            level=self.raw_data["level"]
        )

    def test_from_json(self):
        model = FakeModel.from_json(self.json_data)

        assert model.name == self.raw_data['name']
        assert model.level == self.raw_data['level']


    def test_to_json(self):
        json_data = self.model.to_json()

        assert self.json_data == json_data