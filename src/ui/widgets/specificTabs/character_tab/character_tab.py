from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QBoxLayout,
    QScrollArea,
    QSizePolicy
)

from .general_info.general_info import CharacterGeneralInfo
from .skills.skills_section import SkillsSection, CaracteristicName
from .combat_capacities.combat_capacities import CombatCapacities
class CharacterTab(QWidget):
    """A tab to hold a character sheet"""

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self) -> QBoxLayout:
        """Creates the layout for the tab."""
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        general_info_widget = CharacterGeneralInfo()
        general_info_widget.setSizePolicy(general_info_widget.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)

        skills_section = SkillsSection()
        combat_capacities = CombatCapacities()

        combat_capacities.add_info("INITIATIVE")
        skills_section.carac_widgets[CaracteristicName.DEXTERITY].modifier.line_edit.textChanged.connect(lambda txt: combat_capacities.infos["INITIATIVE"].update_value(txt))
        combat_capacities.add_info("SPEED")
        combat_capacities.add_info("SIZE")
        combat_capacities.add_info("PASSIVE PERCEPTION")
        skills_section.carac_widgets[CaracteristicName.WISDOM].skills["Perception"][2].textChanged.connect(lambda txt: combat_capacities.infos["PASSIVE PERCEPTION"].update_value(str(10 + int(txt))))

        layout.addWidget(general_info_widget)

        bottom_layout = QHBoxLayout()
        skills_scroll = QScrollArea()
        skills_scroll.setWidgetResizable(True)
        skills_scroll.setWidget(skills_section)
        bottom_layout.addWidget(skills_scroll, stretch=1)
        combat_scroll = QScrollArea()
        combat_scroll.setWidgetResizable(True)
        combat_scroll.setWidget(combat_capacities)
        bottom_layout.addWidget(combat_scroll, stretch=3)

        layout.addLayout(bottom_layout)


        return layout
