from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class UnderlabeledLineEdit(QWidget):
    def __init__(self, label_text:str, placeholder_text:str="", label_alignement:Qt.AlignmentFlag=Qt.AlignmentFlag.AlignLeft):
        super().__init__()
        layout = self.create_layout(label_alignement)
        self.setLayout(layout)
        self.line_edit.setPlaceholderText(placeholder_text)
        self.label.setText(label_text)

    def create_layout(self, label_alignement:Qt.AlignmentFlag):
        layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.label = QLabel("")

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.label, alignment=label_alignement)

        layout.addStretch()

        return layout

    def set_label(self, text:str):
        self.label.setText(text)

    def set_value(self, text:str):
        self.line_edit.setText(text)