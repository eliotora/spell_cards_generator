from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QBoxLayout,
    QScrollArea,
    QSizePolicy,
    QTabWidget
)

from src.ui.widgets.specificTabs.character_tab.general_info.general_info import CharacterGeneralInfo
from src.ui.widgets.specificTabs.character_tab.skills.skills_section import SkillsSection
from src.ui.widgets.specificTabs.character_tab.combat_capacities.combat_capacities import CombatCapacities
from src.ui.widgets.specificTabs.character_tab.spellcasting.spellcasting_section import SpellcastingSectionWidget
from src.ui.widgets.specificTabs.character_tab.backstory_equipment.backstory_equipment_widget import BackstoryEquipementWidget
from src.models.character_model import Character
from src.models.character_class_model import *
class CharacterTab(QWidget):
    """A tab to hold a character sheet"""

    def __init__(self):
        super().__init__()
        self.character = Character()
        layout = self.create_layout()
        self.setLayout(layout)

        char_class = CharacterClass(
            name="Magicien",
            health_dice=Dice.D6,
            profiencies=["dague", "fléchette", "fronde", "bâton", "arbalète légère"],
            saving_throws_profiencies= [Caracteristic.Caracteristics.INTELLIGENCE, Caracteristic.Caracteristics.WISDOM],
            skills_profiencies_choice=[2, [
                Ability.Abilities.Arcana,
                Ability.Abilities.History,
                Ability.Abilities.Insight,
                Ability.Abilities.Investigation,
                Ability.Abilities.Medicine,
                Ability.Abilities.Religion
                ]],
            starting_equipement=[[]],
            class_features={}
        )

        spellcasting_feat = SpellCastingFeature(
            spell_slot_evolution=SpellSlotEvolution.FULLCASTER,
            max_minor_spells= {
                1:3,2:3,3:3,4:4,5:4,6:4,7:4,8:4,9:4,10:5,11:5,12:5,13:5,14:5,15:5,16:5,17:5,18:5,19:5,20:5,
            },
            spellcasting_carac=Caracteristic.Caracteristics.INTELLIGENCE,
            spellcasting_focus_type="Focaliseur arcanique",
            max_spell_nbr=MaxSpellNbr.LevelPlusMod,
            spell_filter=spell_filter_factory(
                {
                    "type": "compare",
                    "compare_type": "EQ",
                    "key": "level",
                    "value": 1
                }
            )
        )

    def create_layout(self) -> QBoxLayout:
        """Creates the layout for the tab."""
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        tab_char1 = QWidget()
        tab_widget.addTab(tab_char1, "Front")

        tab1_layout = QVBoxLayout()
        tab1_layout.setSpacing(0)
        tab1_layout.setContentsMargins(0, 0, 0, 0)
        tab_char1.setLayout(tab1_layout)

        general_info_widget = CharacterGeneralInfo(self.character)
        general_info_widget.setSizePolicy(general_info_widget.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)

        skills_section = SkillsSection(self.character)
        combat_capacities = CombatCapacities(self.character)

        combat_capacities.add_info("INITIATIVE")
        # skills_section.carac_widgets[Caracteristic.Caracteristics.DEXTERITY].modifier.spinbox.valueChanged.connect(lambda txt: combat_capacities.infos["INITIATIVE"].update_value(txt))
        combat_capacities.add_info("SPEED")
        combat_capacities.add_info("SIZE")
        combat_capacities.add_info("PASSIVE PERCEPTION")
        # skills_section.carac_widgets[Caracteristic.Caracteristics.WISDOM].skills[Ability.Abilities.Perception][2].textChanged.connect(lambda txt: combat_capacities.infos["PASSIVE PERCEPTION"].update_value(str(10 + int(txt))))

        tab1_layout.addWidget(general_info_widget)

        bottom_layout = QHBoxLayout()
        skills_scroll = QScrollArea()
        skills_scroll.setWidgetResizable(True)
        skills_scroll.setWidget(skills_section)
        bottom_layout.addWidget(skills_scroll, stretch=1)
        combat_scroll = QScrollArea()
        combat_scroll.setWidgetResizable(True)
        combat_scroll.setWidget(combat_capacities)
        bottom_layout.addWidget(combat_scroll, stretch=3)

        tab1_layout.addLayout(bottom_layout)

        spell_section_widget = SpellcastingSectionWidget()
        backstory_equipment = BackstoryEquipementWidget()

        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(spell_section_widget, stretch=2)
        backstory_scroll = QScrollArea()
        backstory_scroll.setWidgetResizable(True)
        backstory_scroll.setWidget(backstory_equipment)
        tab2_layout.addWidget(backstory_scroll, stretch=1)

        tab_char2 = QWidget()
        tab_char2.setLayout(tab2_layout)

        tab_widget.addTab(tab_char2, "Back")

        return layout
