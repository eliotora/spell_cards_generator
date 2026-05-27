from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit, QSizePolicy, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from ..underlabeled_edits import UnderlabeledSpinBox
from src.models.character_model import Caracteristic, signaledProperty, Ability

class CaracSkillswidget(QWidget):
    def __init__(self, carac:Caracteristic, skills: list[Ability] = [], profiency_bonus:signaledProperty[int] = 2):
        super().__init__()
        self.skills: dict[Ability, tuple[QHBoxLayout, QCheckBox, QLineEdit, QLabel]] = {}
        layout = self.create_layout(carac, skills)
        self.setLayout(layout)
        self.profiency_bonus: int = profiency_bonus.value

    def create_layout(self, carac:Caracteristic, skills: list[Ability]):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        carac_label = QLabel(carac.name)

        self.modifier = UnderlabeledSpinBox("MODIFIER", -5, 10, label_alignment=Qt.AlignmentFlag.AlignCenter)
        self.score = UnderlabeledSpinBox("SCORE", 0, 30, 10, label_alignment=Qt.AlignmentFlag.AlignCenter)

        self.score.spinbox.valueChanged.connect(carac.setValue)
        carac.valueChanged.connect(lambda: (
            self.score.spinbox.setValue(carac.getValue()),
            self.modifier.spinbox.setValue(carac.getMod())
        ))
        self.modifier.spinbox.setReadOnly(True)
        self.modifier.spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.score.spinbox.wheelEvent = lambda event: event.ignore()


        carac_layout = QHBoxLayout()
        carac_layout.setSpacing(0)
        carac_layout.setContentsMargins(0, 0, 0, 0)

        carac_layout.addWidget(self.modifier)
        carac_layout.addWidget(self.score)

        def spinbox_update_factory(spinbox:QSpinBox, ability:Ability):
            return lambda: spinbox.setValue(ability.get_mod(self.profiency_bonus))

        def checkbox_update_factory(ability:Ability):
            return lambda state: ability.setProficient(state == Qt.CheckState.Checked)

        for line in skills:
            line_layout = QHBoxLayout()
            line_layout.setSpacing(0)
            line_layout.setContentsMargins(0, 0, 0, 0)

            check_box = QCheckBox()
            bonus = QSpinBox(minimum=-10, maximum=30, alignment=Qt.AlignmentFlag.AlignRight)
            fm = QFontMetrics(bonus.font())
            bonus.setFixedSize(fm.horizontalAdvance("M") * 3, fm.height()+6)
            label = QLabel(line.name)

            check_box.checkStateChanged.connect(checkbox_update_factory(line))
            bonus.setReadOnly(True)
            bonus.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            line.onModifierChanged.connect(spinbox_update_factory(bonus, line))


            line_layout.addWidget(check_box, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addWidget(bonus, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
            line_layout.addStretch()

            self.skills[line] = (line_layout, check_box, bonus, label)

        layout.addWidget(carac_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(carac_layout)
        for line in skills:
            layout.addLayout(self.skills[line][0])

        layout.addStretch()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return layout

    def changeProfiency(self, value:int=2):
        self.profiency_bonus = value
        for key, item in self.skills.items():
            key.onModifierChanged.emit()


