from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QSizePolicy
from PySide6.QtCore import Qt

class Inspiration(QWidget):
    def __init__(self, value:int=2):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 10)
        label = QLabel("HEROIC INSPIRATION")
        mod = QCheckBox()

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mod, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return layout
