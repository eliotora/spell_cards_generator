from PyQt6.QtCore import QAbstractTableModel, Qt
from model.loaders.spell_loader import load_spells_from_folder
from copy import deepcopy
import locale

locale.setlocale(locale.LC_COLLATE, 'French_France.1252')

class SpellModels:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.spells = load_spells_from_folder("data")
            cls.spells.sort(key=lambda i: locale.strxfrm(i["nom"]))
            cls.instance = super(SpellModels, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_spell(cls, name:str):
        for spell in cls.spells:
            if spell["nom"].lower() == name.lower():
                return deepcopy(spell)
        return None

    @classmethod
    def get_spells(cls):
        return deepcopy(cls.spells)


class JSONTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data_list = data
        self.keys = list(data[0].keys()) if data else []

    def rowCount(self, parent=None):
        return len(self.data_list)

    def columnCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self.data_list[index.row()]
            key = self.keys[index.column()]
            return str(row.get(key, ""))

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.keys[section]
            else:
                return str(section + 1)
