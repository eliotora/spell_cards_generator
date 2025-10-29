from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox
from PySide6.QtCore import Qt

class ArmorClassWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.label = QLabel("ARMOR CLASS")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.armor_class = QLineEdit()
        self.shield_label = QLabel("SHIELD")
        self.shield_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shield_checkbox = QCheckBox()


        layout.addWidget(self.label)
        layout.addWidget(self.armor_class)
        layout.addWidget(self.shield_label)
        layout.addWidget(self.shield_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

