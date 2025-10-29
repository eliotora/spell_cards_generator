from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class SimpleTextBox(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = self.create_layout(title)
        self.setLayout(layout)

    def create_layout(self, text:str):
        layout = QVBoxLayout()
        label = QLabel(text.upper())

        self.text_box = QTextEdit()

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_box)

        return layout

class DoubleTextBox(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = self.create_layout(title)
        self.setLayout(layout)

    def create_layout(self, text:str):
        layout = QVBoxLayout()
        label = QLabel(text.upper())

        text_box_layout = QHBoxLayout()

        self.left_text_box = QTextEdit()
        self.right_text_box = QTextEdit()

        text_box_layout.addWidget(self.left_text_box)
        text_box_layout.addWidget(self.right_text_box)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(text_box_layout)

        return layout

