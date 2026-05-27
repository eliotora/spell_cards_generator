from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .proficiency_bonus import ProficiencyBonus
from .carac_skills import CaracSkillswidget
from .inspiration import Inspiration
from .equipment_training import EquipmentTrainingWidget
from src.models.character_model import Character, Ability, Caracteristic

class SkillsSection(QWidget):
    carac_widgets: dict[Caracteristic.Caracteristics, CaracSkillswidget] = {}

    def __init__(self, character: Character):
        super().__init__()
        layout = self.create_layout(character)
        self.setLayout(layout)

    def create_layout(self, character: Character) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20, 0, 0, 20)

        carac_skills_layout = QHBoxLayout()
        carac_skills_layout.setSpacing(0)
        carac_skills_layout.setContentsMargins(0, 0, 0, 0)

        left_carac_skills = QVBoxLayout()
        left_carac_skills.setSpacing(0)
        left_carac_skills.setContentsMargins(0, 0, 5, 0)
        right_carac_skills = QVBoxLayout()
        left_carac_skills.setSpacing(0)
        left_carac_skills.setContentsMargins(5, 0, 5, 0)

        self.proficiency_widget = ProficiencyBonus(character)
        self.inspiration = Inspiration(character)

        for k,c in character.caracs.value.items():
            widget = CaracSkillswidget(c, [character.saving_throws.value[k]] + [character.abilities.value[ability] for ability in Ability.Abilities.abilities_by_carac(k)], character.proficiency_bonus)
            self.carac_widgets[k] = widget
            self.proficiency_widget.mod.valueChanged.connect(widget.changeProfiency)

        left_carac_skills.addWidget(self.proficiency_widget)
        left_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.STRENGTH])
        left_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.DEXTERITY])
        left_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.CONSTITUTION])
        left_carac_skills.addWidget(self.inspiration)

        right_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.INTELLIGENCE])
        right_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.WISDOM])
        right_carac_skills.addWidget(self.carac_widgets[Caracteristic.Caracteristics.CHARISMA])

        carac_skills_layout.addLayout(left_carac_skills)
        carac_skills_layout.addLayout(right_carac_skills)


        equipment_training_widget = EquipmentTrainingWidget()

        layout.addLayout(carac_skills_layout)
        layout.addWidget(equipment_training_widget)

        return layout


