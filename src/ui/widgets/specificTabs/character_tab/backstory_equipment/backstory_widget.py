from PySide6.QtWidgets import QLabel, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt

from ..combat_capacities.text_boxes import SimpleTextBox

class BackstoryWidget(SimpleTextBox):
    def __init__(self):
        super().__init__("Backstory & Personality".upper())
        # self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)


    def create_layout(self, text):
        layout = super().create_layout(text)
        # self.text_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        alignment_label = QLabel("Alignment", alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(alignment_label)

        alignment_edit = QLineEdit()
        layout.addWidget(alignment_edit)

        return layout
