from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QCheckBox
from PySide6.QtCore import Qt
import enum

class ArmorTypes(enum.StrEnum):
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    HEAVY = "HEAVY"
    SHIELDS = "SHIELDS"

class EquipmentTrainingWidget(QWidget):
    armor_trainings = {}

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 0)

        label = QLabel("EQUIPMENT TRAINING & PROFICIENCES")

        armor_layout = QHBoxLayout()
        armor_layout.setSpacing(0)
        armor_layout.setContentsMargins(0, 0, 0, 0)

        armor_label = QLabel("ARMOR TRAINING")
        armor_layout.addWidget(armor_label)
        for armor_type in [a for a in ArmorTypes]:
            checkbox = QCheckBox()
            l = QLabel(armor_type.capitalize())
            self.armor_trainings[armor_type] = checkbox

            armor_layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignRight)
            armor_layout.addWidget(l)

        weapons_label = QLabel("WEAPONS")
        self.weapons_text = QTextEdit()

        tools_label = QLabel("TOOLS")
        self.tools_text = QTextEdit()

        layout.addWidget(label)
        layout.addLayout(armor_layout)
        layout.addWidget(weapons_label)
        layout.addWidget(self.weapons_text)
        layout.addWidget(tools_label)
        layout.addWidget(self.tools_text)

        return layout


