from dataclasses import dataclass
import pytest

from src.models.collections.base_collection import BaseCollection
from src.models.base.base_model import BaseModel


# === Fixtures ===
@dataclass
class TestModel(BaseModel):
    name: str
    level: int

# === TestBaseCollection ===

class TestBaseCollection:
    def setup_method(self):
        m1 = TestModel("Aragorn", 5)
        m2 = TestModel("Bilbo", 1)
        m3 = TestModel("Gandalf", 10)
        self.list = [m1, m2, m3]
        self.col = BaseCollection([m1, m2, m3])

    def test_len(self):
        assert len(self.col) == 3

    def test_iter(self):
        for item_col, item_list in zip(self.col, self.list):
            assert item_col == item_list

    def test_contains(self):
        assert self.list[0] in self.col

    def test_get_item(self):
        assert self.list[1] == self.col.__getitem__(1)

    def test_set_item(self):
        self.col.__setitem__(0, self.list[2])
        assert self.col.get(0) == self.list[2]

    def test_del_item(self):
        second = self.col.get(1)
        old_len = len(self.col)
        self.col.__delitem__(0)
        assert self.col.get(0) == second
        assert len(self.col) == old_len - 1

    def test_repr(self):
        assert repr(self.col) == f"{self.col.__class__.__name__}({len(self.col)})"

    def test_str(self):
        assert self.col.__str__() == repr(self.col)

    def test_items(self):
        cp = self.col.items()
        assert isinstance(cp, list) is True
        assert len(cp) == len(self.col)
        for c, o in zip(cp, self.col):
            assert c==o
        assert cp is not self.col._items

    def test_add(self):
        old_len = len(self.col)
        self.col.add(self.list[0])
        assert len(self.col) == old_len + 1
        assert self.col.get(-1) == self.list[0]

    def test_get(self):
        for i in range(len(self.col)):
            assert self.col.get(i) == self.list[i]

    def test_find_one(self):
        f = lambda i: i.name == "Bilbo"
        r = self.col.find(f)
        assert r == self.list[1]

    def test_find_none(self):
        f = lambda i: i.name == "arararar"
        r = self.col.find(f)
        assert r is None

    def test_filter_one(self):
        f = lambda i: i.name == "Bilbo"
        r = self.col.filter(f)
        assert r._items == [self.list[1]]

    def test_filter_multiple(self):
        f = lambda i: "a" in i.name
        r = self.col.filter(f)
        assert r._items == [self.list[0], self.list[2]]

    def test_filter_empty(self):
        f = lambda i: i.name == "arararar"
        r = self.col.filter(f)
        assert r._items == []


