from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics


class UnderlabeledLineEdit(QWidget):
    def __init__(self, label_text:str, placeholder_text:str="", label_alignment:Qt.AlignmentFlag=Qt.AlignmentFlag.AlignLeft):
        super().__init__()
        layout = self.create_layout(label_alignment)
        self.setLayout(layout)
        self.line_edit.setPlaceholderText(placeholder_text)
        self.label.setText(label_text)

    def create_layout(self, label_alignment:Qt.AlignmentFlag):
        layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.label = QLabel("")

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(self.line_edit, alignment=label_alignment)
        layout.addWidget(self.label, alignment=label_alignment)

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


class UnderlabeledSpinBox(QWidget):
    def __init__(self, label:str, min:int, max:int, value:int=None, label_alignment:Qt.AlignmentFlag=Qt.AlignmentFlag.AlignLeft):
        super().__init__()
        layout = self.create_layout(label_alignment)
        self.setLayout(layout)
        self.spinbox.setMinimum(min)
        self.spinbox.setMaximum(max)
        if value: self.spinbox.setValue(value)
        self.label.setText(label)

    def create_layout(self, label_alignment:Qt.AlignmentFlag):
        layout = QVBoxLayout()

        self.spinbox = QSpinBox()
        self.label = QLabel()

        layout.addWidget(self.spinbox)
        layout.addWidget(self.label, alignment=label_alignment)

        return layout

    def setMaximum(self, max:int):
        self.spinbox.setMaximum(max)

    def setMinimum(self, min:int):
        self.spinbox.setMinimum(min)

    def setValue(self, value:int):
        self.spinbox.setValue(value)

    def setLabelText(self, text:str):
        self.label.setText(text)
