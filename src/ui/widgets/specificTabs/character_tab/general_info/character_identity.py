from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt

from ui.widgets.specificTabs.character_tab.underlabeled_line_edit import (
    UnderlabeledLineEdit,
)


class CharacterIdentity(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.name = UnderlabeledLineEdit("Name".upper())
        self.background = UnderlabeledLineEdit("Background".upper())
        self.species = UnderlabeledLineEdit("Species".upper())
        self.char_class = UnderlabeledLineEdit("Class".upper())
        self.subclass = UnderlabeledLineEdit("Subclass".upper())

        layout.addWidget(self.name, 0, 0, 1, 2)
        layout.addWidget(self.background, 1, 0)
        layout.addWidget(self.species, 2, 0)
        layout.addWidget(self.char_class, 1, 1)
        layout.addWidget(self.subclass, 2, 1)

        return layout
