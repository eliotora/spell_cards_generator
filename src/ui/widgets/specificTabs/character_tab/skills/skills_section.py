from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .proficiency_bonus import ProficiencyBonus
from .carac_skills import CaracSkillswidget, CaracteristicName
from .inspiration import Inspiration
from .equipment_training import EquipmentTrainingWidget

skills = {
    CaracteristicName.STRENGTH: ["Athletics"],
    CaracteristicName.DEXTERITY: ["Acrobatics", "Sleight of Hand", "Stealth"],
    CaracteristicName.CONSITUTION: [],
    CaracteristicName.INTELLIGENCE: ["Arcana", "History", "Investigation", "Nature", "Religion"],
    CaracteristicName.WISDOM: ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
    CaracteristicName.CHARISMA: ["Deception", "Intimidation", "Performance", "Persuasion"]
}

class SkillsSection(QWidget):
    carac_widgets: dict[CaracteristicName, CaracSkillswidget] = {}

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
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

        self.proficiency_widget = ProficiencyBonus()
        self.inspiration = Inspiration()

        for carac in [c for c in CaracteristicName]:
            widget = CaracSkillswidget(carac, True, skills[carac])
            self.carac_widgets[carac] = widget
            self.proficiency_widget.mod.textChanged.connect(widget.changeProfiency)

        left_carac_skills.addWidget(self.proficiency_widget)
        left_carac_skills.addWidget(self.carac_widgets[CaracteristicName.STRENGTH])
        left_carac_skills.addWidget(self.carac_widgets[CaracteristicName.DEXTERITY])
        left_carac_skills.addWidget(self.carac_widgets[CaracteristicName.CONSITUTION])
        left_carac_skills.addWidget(self.inspiration)

        right_carac_skills.addWidget(self.carac_widgets[CaracteristicName.INTELLIGENCE])
        right_carac_skills.addWidget(self.carac_widgets[CaracteristicName.WISDOM])
        right_carac_skills.addWidget(self.carac_widgets[CaracteristicName.CHARISMA])

        carac_skills_layout.addLayout(left_carac_skills)
        carac_skills_layout.addLayout(right_carac_skills)


        equipment_training_widget = EquipmentTrainingWidget()

        layout.addLayout(carac_skills_layout)
        layout.addWidget(equipment_training_widget)

        return layout


