from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt
from src.models.character_model import Character

class Inspiration(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.inspiration_box.checkStateChanged.connect(lambda state: character.setInspiration(state == Qt.CheckState.Checked))
        character.inspiration.changed.connect(lambda val: self.inspiration_box.setCheckState(Qt.CheckState.Checked if val else Qt.CheckState.Unchecked))


    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 10)
        label = QLabel("HEROIC INSPIRATION")
        self.inspiration_box = QCheckBox()

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.inspiration_box, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return layout
