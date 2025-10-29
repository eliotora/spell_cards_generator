from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .info_display import InfoDisplay
from .attack_table import AttackTableWidget
from .text_boxes import SimpleTextBox, DoubleTextBox

class CombatCapacities(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.infos: dict[str, InfoDisplay] = {}

    def create_layout(self):
        layout = QVBoxLayout()

        self.info_layout = QHBoxLayout()

        # self.initiative_info_box = InfoDisplay("INITIATIVE")
        # self.speed_info_box = InfoDisplay("SPEED")
        # self.size_info_box = InfoDisplay("SIZE")
        # self.passive_perception_info_box = InfoDisplay("PASSIVE PERCEPTION")

        # for widget in [self.initiative_info_box, self.speed_info_box, self.size_info_box, self.passive_perception_info_box]: self.info_layout.addWidget(widget)

        layout.addLayout(self.info_layout)

        self.attack_table_widget = AttackTableWidget()

        layout.addWidget(self.attack_table_widget)

        self.class_features = DoubleTextBox("CLASS FEATURES")

        layout.addWidget(self.class_features)

        traits_feats_layout = QHBoxLayout()
        traits_feats_layout.setSpacing(0)
        traits_feats_layout.setContentsMargins(0,0,0,0)

        self.species_traits = SimpleTextBox("SPECIES TRAITS")
        self.feats = SimpleTextBox("FEATS")

        traits_feats_layout.addWidget(self.species_traits)
        traits_feats_layout.addWidget(self.feats)

        layout.addLayout(traits_feats_layout)

        return layout

    def add_info(self, title:str):
        info = InfoDisplay(title)
        self.info_layout.addWidget(info)
        self.infos[title] = info

