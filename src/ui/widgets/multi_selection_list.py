from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QCheckBox,
    QVBoxLayout,
    QAbstractItemView,
    QSizePolicy
)
from PySide6.QtCore import Qt

class MultiSelectionListWidget(QWidget):
    def __init__(self, label: str = ""):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.checkbox = QCheckBox(label+":", self)
        self.checkbox.setChecked(True)
        self.checkbox.checkStateChanged.connect(self.toggle_selection)

        self.list = QListWidget()
        self.list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.list.clicked.connect(self.update_checkbox_state)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.list)

    def toggle_selection(self, state):
        checked = state == Qt.CheckState.Checked

        for i in range(self.list.count()):
            self.list.item(i).setSelected(checked)

    def update_checkbox_state(self):
        total = self.list.count()
        selected = len(self.list.selectedItems())

        all_selected = selected == total

        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(all_selected)
        self.checkbox.blockSignals(False)

    def get_selected_item_texts(self) -> list[str]:
        return [item.text() for item in self.list.selectedItems()]

    def clear(self):
        self.list.clear()

    def addItem(self, item): self.list.addItem(item)

    def addItems(self, items): self.list.addItems(items)

    def adjustSize(self):
        self.list.adjustSize()
        super().adjustSize()

    def checkItems(self, items):
        for i in range(self.list.count()):
            checked = self.list.item(i).text() in items
            self.list.item(i).setSelected(checked)