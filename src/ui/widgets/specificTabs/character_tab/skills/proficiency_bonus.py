from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from src.models.character_model import Character

class ProficiencyBonus(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

        character.proficiency_bonus.changed.connect(self.mod.setValue)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 10)
        label = QLabel("PROFICIENCY BONUS")
        self.mod = QSpinBox(minimum=2, maximum=10, alignment=Qt.AlignmentFlag.AlignRight)
        self.mod.setReadOnly(True)
        self.mod.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        fm = QFontMetrics(self.mod.font())
        char_width = fm.horizontalAdvance("M")
        char_height = fm.height()

        self.mod.setFixedSize(char_width*2, char_height+6)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mod, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout
