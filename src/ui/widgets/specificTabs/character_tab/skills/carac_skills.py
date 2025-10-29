from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from ..underlabeled_line_edit import UnderlabeledLineEdit
import enum
from copy import copy

class CaracteristicName(enum.StrEnum):
    """Enum for the caracteristics of the character"""
    STRENGTH = "STRENGTH"
    DEXTERITY = "DEXTERITY"
    CONSITUTION = "CONSTITUTION"
    INTELLIGENCE = "INTELLIGENCE"
    WISDOM = "WISDOM"
    CHARISMA = "CHARISMA"

    @classmethod
    def from_string(cls, value: str) -> 'CaracteristicName':
        """Convert a string to an CaracteristicName enum."""
        return cls[value.upper()]

class CaracSkillswidget(QWidget):
    def __init__(self, carac:CaracteristicName, saving_throw:bool = True, skills: list[str] = [], profiency_bonus:int = 2):
        super().__init__()
        self.skills: dict[str, tuple[QHBoxLayout, QCheckBox, QLineEdit, QLabel]] = {}
        layout = self.create_layout(carac, saving_throw, skills)
        self.setLayout(layout)
        self.profiency_bonus = profiency_bonus

    def create_layout(self, carac:CaracteristicName, saving_throw:bool, skills: list[str]):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        carac_label = QLabel(carac.value)

        self.modifier = UnderlabeledLineEdit("MODIFIER", "0", Qt.AlignmentFlag.AlignCenter)
        self.modifier.setFixedCharSize(2)
        self.score = UnderlabeledLineEdit("SCORE", "10", Qt.AlignmentFlag.AlignCenter)
        self.score.setFixedCharSize(2)
        self.score.line_edit.textChanged.connect(self.on_value_changed)

        carac_layout = QHBoxLayout()
        carac_layout.setSpacing(0)
        carac_layout.setContentsMargins(0, 0, 0, 0)

        carac_layout.addWidget(self.modifier)
        carac_layout.addWidget(self.score)

        lines = copy(skills)
        if saving_throw: lines.insert(0, "Saving Throw")


        for line in lines:
            line_layout = QHBoxLayout()
            line_layout.setSpacing(0)
            line_layout.setContentsMargins(0, 0, 0, 0)

            check_box = QCheckBox()
            bonus = QLineEdit(alignment=Qt.AlignmentFlag.AlignRight)
            fm = QFontMetrics(bonus.font())
            bonus.setFixedSize(fm.horizontalAdvance("M") * 3, fm.height()+6)
            label = QLabel(line)

            line_layout.addWidget(check_box, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addWidget(bonus, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addStretch()

            self.skills[line] = (line_layout, check_box, bonus, label)
            check_box.checkStateChanged.connect(self.checkbox_update_factory(bonus, check_box))

        layout.addWidget(carac_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(carac_layout)
        for line in lines:
            layout.addLayout(self.skills[line][0])

        layout.addStretch()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return layout

    def checkbox_update_factory(self, line_edit:QLineEdit, checkbox:QCheckBox):
        return lambda state: self.update_bonus(line_edit, checkbox, int(self.modifier.get_value() if self.modifier.get_value() else 0))

    def on_value_changed(self):
        new_value = self.score.get_value()

        try:
            new_value = int(new_value)
        except:
            return

        new_modifier = (new_value - 10) // 2

        self.modifier.set_value(f"+{new_modifier}" if new_modifier >= 0 else f"{new_modifier}")

        for key, item in self.skills.items():
            self.update_bonus(item[2], item[1], new_modifier)

    def update_bonus(self, line_edit:QLineEdit, checkbox:QCheckBox, modifier:int):
        final_score = modifier
        if checkbox.isChecked(): final_score += self.profiency_bonus
        line_edit.setText(f"+{final_score}" if final_score >= 0 else f"{final_score}")

    def changeProfiency(self, value:int=2):
        try:
            value = int(value)
        except:
            return
        self.profiency_bonus = value
        for key, item in self.skills.items():
            self.update_bonus(item[2], item[1], int(self.modifier.get_value() if self.modifier.get_value() else 0))


