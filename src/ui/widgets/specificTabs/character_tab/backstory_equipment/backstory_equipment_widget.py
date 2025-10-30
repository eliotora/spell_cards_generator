from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from .backstory_widget import BackstoryWidget
from .coins_widget import CoinWidget
from .equipement_widget import EquipementWidget
from ..combat_capacities.text_boxes import SimpleTextBox

class BackstoryEquipementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        self.appearance_box = SimpleTextBox("APPEARANCE")
        self.backstory_box = BackstoryWidget()
        self.language_box = SimpleTextBox("Language")
        self.equipement_box = EquipementWidget()
        self.coin_widget = CoinWidget()

        # for widget in [self.appearance_box, self.backstory_box, self.language_box, self.equipement_box, self.coin_widget]:
        #     widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        # for widget in [self.appearance_box, self.backstory_box, self.language_box, self.equipement_box]:
        #     widget.text_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        layout.addWidget(self.appearance_box, stretch=4)
        layout.addWidget(self.backstory_box, stretch=8)
        layout.addWidget(self.language_box, stretch=2)
        layout.addWidget(self.equipement_box, stretch=10)
        layout.addWidget(self.coin_widget, stretch=3)

        return layout