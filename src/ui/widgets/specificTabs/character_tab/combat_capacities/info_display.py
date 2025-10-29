from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics


class InfoDisplay(QWidget):
    value = ""
    def __init__(self, name:str, value=None):
        super().__init__()
        layout = self.create_layout(name, value)
        self.setLayout(layout)
        self.value = value

    def create_layout(self, name, value):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5,5,5,5)
        label = QLabel(name)
        self.value_display = QLineEdit(alignment=Qt.AlignmentFlag.AlignCenter)
        self.value_display.setText(value)
        fm = QFontMetrics(self.value_display.font())
        self.value_display.setFixedSize(fm.horizontalAdvance("M") * 3, fm.height() + 6)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_display, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

    def update_value(self, value):
        self.value = value
        self.value_display.setText(value)

