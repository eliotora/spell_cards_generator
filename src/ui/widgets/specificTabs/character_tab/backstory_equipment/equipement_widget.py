from PySide6.QtWidgets import QLabel, QCheckBox, QLineEdit, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

from src.ui.widgets.specificTabs.character_tab.combat_capacities.text_boxes import SimpleTextBox

class EquipementWidget(SimpleTextBox):
    def __init__(self):
        super().__init__("Equipment".upper())
        # self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def create_layout(self, text):
        layout = super().create_layout(text)

        # self.text_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        attunement_label = QLabel("Magic Item Attunement", alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(attunement_label)
        for i in range(3):
            h_layout = QHBoxLayout()
            attunement_checkbox = QCheckBox()
            item_name = QLineEdit()

            h_layout.addWidget(attunement_checkbox)
            h_layout.addWidget(item_name)
            layout.addLayout(h_layout)

        return layout
