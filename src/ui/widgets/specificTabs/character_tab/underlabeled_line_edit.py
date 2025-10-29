from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics


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

        layout.addWidget(self.line_edit, alignment=label_alignement)
        layout.addWidget(self.label, alignment=label_alignement)

        layout.addStretch()

        return layout

    def set_label(self, text:str):
        self.label.setText(text)

    def set_value(self, text:str):
        self.line_edit.setText(text)

    def setFixedSize(self, w:int, h:int):
        label_size = self.label.minimumSizeHint()

        w = w if w >= label_size.width() else label_size.width()
        h = h if h >= label_size.height() else label_size.height()

        self.line_edit.setFixedSize(w, h)

    def setFixedCharSize(self, char_nbr:int):
        fm = QFontMetrics(self.line_edit.font())

        font_h = fm.height()
        font_w = fm.maxWidth()

        self.setFixedSize(font_w*char_nbr, font_h+6)

    def get_value(self):
        return self.line_edit.text()
