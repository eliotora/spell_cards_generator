from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt

from ui.widgets.specificTabs.character_tab.underlabeled_line_edit import (
    UnderlabeledLineEdit,
)
from .character_identity import CharacterIdentity
from .level_xp import LevelXpWidget
from .armor_class import ArmorClassWidget
from .life_section import LifeWidget


class CharacterGeneralInfo(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 10)

        self.char_identity = CharacterIdentity()
        self.level = LevelXpWidget()
        self.armor_class = ArmorClassWidget()
        self.life = LifeWidget()

        left_layout = QHBoxLayout()
        left_layout.addWidget(self.char_identity, stretch=2)
        left_layout.addWidget(self.level, stretch=1)
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.armor_class, stretch=1)
        right_layout.addWidget(self.life, stretch=4)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        return layout
