from dataclasses import dataclass, field
import pytest

from src.models.base.base_model import BaseModel

# === Fixture ===

@dataclass
class ModelOK(BaseModel):
    name: str
    level: int = field(init=False)

@dataclass
class ModelNoLvl(BaseModel):
    name: str

# === TestBaseModel ===
class TestBaseModel:
    def test_eq_ok(self):
        model1 = ModelOK(name="Eliot")
        model1.level =  1
        model2 = ModelOK(name="Eliot")
        model2.level =  1

        assert model1.name == model2.name
        assert model1.level == model2.level
        assert model1 == model2

    def test_eq_nok_different_class(self):
        model1 = ModelOK(name="Eliot")
        model1.level =  1
        model2 = ModelNoLvl(name="Eliot")

        assert model1 != model2

    def test_eq_nok_different_values(self):
        model1 = ModelOK(name="Eliot")
        model1.level = 5
        model2 = ModelOK(name="Alexandre")
        model2.level = 5

        assert model1 != model2
