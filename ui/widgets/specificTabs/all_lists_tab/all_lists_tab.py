from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QGridLayout
from utils.shared_dict import SharedDict
from model.generic_model import MODEL_NAME_MAPPING
from ui.widgets.detailled_item_list import DetailledItemList
from math import sqrt, ceil


class AllListsTab(QWidget):
    _othersDict : SharedDict
    _spellsDict : SharedDict
    def __init__(self, details_windows, spells_dict: SharedDict, others_dict: SharedDict):
        super().__init__()
        self._othersDict = others_dict
        self._spellsDict = spells_dict
        self.details_windows = details_windows
        self.setup_layout()
        self._othersDict.categoryChanged.connect(self.on_category_changed)
        self._spellsDict.categoryChanged.connect(self.on_category_changed)

    def setup_layout(self):
        layout = QGridLayout()

        lst_nbr = len(self._othersDict.keys())
        line_nbr = ceil(sqrt(lst_nbr))

        self.setLayout(layout)
        self._lists = {}
        layout.addWidget(QLabel("Sorts"), 0, 0, 1, 2)
        left_col = QVBoxLayout()
        right_col = QVBoxLayout()
        for key, list in self._spellsDict.items():
            label = QLabel("Niveau " + key if int(key) != 0 else "Tours de magie")
            wlist = DetailledItemList(self.details_windows, MODEL_NAME_MAPPING["Spell"])
            self._lists[key] = wlist
            if int(key) < 5:
                left_col.addWidget(label)
                left_col.addWidget(wlist)
            else:
                right_col.addWidget(label)
                right_col.addWidget(wlist)
            self.on_category_changed(key, list)
        layout.addLayout(left_col, 1, 0, line_nbr, 1)
        layout.addLayout(right_col, 1, 1, line_nbr, 1)

        i = 0
        for key, list in self._othersDict.items():
            label = QLabel(key)
            wlist = DetailledItemList(self.details_windows, MODEL_NAME_MAPPING[key])
            self._lists[key] = wlist
            layout.addWidget(label, 2*(i//line_nbr), i%line_nbr+2)
            layout.addWidget(wlist, 2*(i//line_nbr)+1, i%line_nbr+2)
            self.on_category_changed(key, list)
            i+=1

    def on_category_changed(self, key, items):
        if key in self._lists:
            list = self._lists[key]
            self.update_list(list, items)

    def update_list(self, list: QListWidget, items:list):
        current = [list.item(i).text() for i in range(list.count())]
        if current != items:
            list.clear()
            list.addItems(items)

    def on_item_double_click(self, item: QListWidgetItem):
        item_name = item.text()



