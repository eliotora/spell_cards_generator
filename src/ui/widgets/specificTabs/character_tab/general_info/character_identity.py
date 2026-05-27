from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt

from src.ui.widgets.specificTabs.character_tab.underlabeled_edits import (
    UnderlabeledLineEdit,
)
from src.models.character_model import Character


class CharacterIdentity(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.name.line_edit.textChanged.connect(character.setName)
        self.background.line_edit.textChanged.connect(character.setBackground)
        self.species.line_edit.textChanged.connect(character.setSpecies)
        self.char_class.line_edit.textChanged.connect(character.setClass)
        self.subclass.line_edit.textChanged.connect(character.setSubclass)

        character.name.changed.connect(self.name.line_edit.setText)
        character.background.changed.connect(self.background.line_edit.setText)
        character.species.changed.connect(self.species.line_edit.setText)
        character.char_class.changed.connect(self.char_class.line_edit.setText)
        character.subclass.changed.connect(self.subclass.line_edit.setText)

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
