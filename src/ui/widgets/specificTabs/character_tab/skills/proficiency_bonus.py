from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics

class ProficiencyBonus(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 10)
        label = QLabel("PROFICIENCY BONUS")
        self.mod = QLineEdit()
        fm = QFontMetrics(self.mod.font())
        char_width = fm.horizontalAdvance("M")
        char_height = fm.height()

        self.mod.setFixedSize(char_width*2, char_height+6)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mod, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout
