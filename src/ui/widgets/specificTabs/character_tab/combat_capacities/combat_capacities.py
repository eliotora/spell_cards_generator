from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .info_display import InfoDisplay
from .attack_table import AttackTableWidget
from .text_boxes import SimpleTextBox, DoubleTextBox
from src.models.item_model import Weapon, WeaponProperty, Dice, WeaponType
from src.models.conceptual_models import WeaponPropertyType, Distance
from src.models.character_model import Character

class CombatCapacities(QWidget):
    def __init__(self, char:Character):
        super().__init__()
        self.char = char
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

        weapon = Weapon(
            name="Trident",
            vf_name="",
            vo_name="Trident",
            type=["Arme", "Arme de guerre", "Arme de corps à corps"],
            weight="2 kg",
            description="",
            short_description="",
            cost="5 po",
            damage_dice=(1, Dice.D6),
            damage_type="Perforant",
            properties=[
                WeaponProperty(WeaponPropertyType.THROWN, range_normal=Distance(6, "m"), range_max=Distance(18, "m")),
                WeaponProperty(WeaponPropertyType.VERSATILE, versatile_damage=Dice.D8)
            ],
            source="PHB",
            weapon_type=WeaponType.MELEE
        )

        self.attack_table_widget.add_attack(weapon, char=self.char)

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

