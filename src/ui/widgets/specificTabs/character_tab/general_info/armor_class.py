from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QCheckBox
from PySide6.QtCore import Qt
from src.models.character_model import Character

class ArmorClassWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.armor_class.valueChanged.connect(character.setArmorClass)
        self.shield_checkbox.checkStateChanged.connect(lambda state: character.setShield(state==Qt.CheckState.Checked))
        character.armor_class.changed.connect(self.armor_class.setValue)
        character.shield.changed.connect(self.shield_checkbox.setChecked)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.label = QLabel("ARMOR CLASS")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.armor_class = QSpinBox(minimum=0, maximum=50, value=10)
        self.shield_label = QLabel("SHIELD")
        self.shield_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shield_checkbox = QCheckBox()


        layout.addWidget(self.label)
        layout.addWidget(self.armor_class)
        layout.addWidget(self.shield_label)
        layout.addWidget(self.shield_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

