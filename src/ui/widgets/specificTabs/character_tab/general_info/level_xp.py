from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from src.ui.widgets.specificTabs.character_tab.underlabeled_edits import UnderlabeledSpinBox
from src.models.character_model import Character

class LevelXpWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.level.spinbox.valueChanged.connect(character.setLvl)
        self.xp.spinbox.valueChanged.connect(character.setXp)
        character.lvl.changed.connect(self.level.setValue)
        character.xp.changed.connect(self.xp.setValue)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.level = UnderlabeledSpinBox("Level".upper(), min=1, max=20, value=1, label_alignment=Qt.AlignmentFlag.AlignCenter)
        self.xp = UnderlabeledSpinBox("XP".upper(), min=0, max=355000, label_alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.level, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.xp, Qt.AlignmentFlag.AlignTop)

        return layout

