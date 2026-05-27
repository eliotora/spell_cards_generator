from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt

from ..underlabeled_edits import UnderlabeledSpinBox
from src.models.character_model import Character

class HitPointsWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.current_hp.spinbox.valueChanged.connect(character.setCurrentHitPoints)
        self.temp_hp.spinbox.valueChanged.connect(character.setTempHitPoints)
        self.max_hp.spinbox.valueChanged.connect(character.setMaxHitPoints)
        character.current_hit_points.changed.connect(self.current_hp.setValue)
        character.temp_hit_points.changed.connect(self.temp_hp.setValue)
        character.max_hit_points.changed.connect(self.max_hp.setValue)

    def create_layout(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.label = QLabel("HIT POINTS")
        self.current_hp = UnderlabeledSpinBox("CURRENT", -200, 200, 1)
        self.temp_hp = UnderlabeledSpinBox("TEMP", min=0, max=100, value=0)
        self.max_hp = UnderlabeledSpinBox("MAX", min=1, max=200, value=6)


        layout.addWidget(self.label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_hp, 1, 0, 2, 1)
        layout.addWidget(self.temp_hp, 1, 1, 1, 1)
        layout.addWidget(self.max_hp, 2, 1, 1, 1)

        return layout


class HitDicesWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)
        self.spent_dices.spinbox.valueChanged.connect(character.setSpentHitDice)
        self.max_dices.spinbox.valueChanged.connect(character.setMaxHitDice)
        character.spent_hit_dice.changed.connect(self.spent_dices.setValue)
        character.max_hit_dice.changed.connect(self.max_dices.setValue)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.label = QLabel("HIT DICE")
        self.spent_dices = UnderlabeledSpinBox("SPENT", 0, 1, 0)
        self.max_dices = UnderlabeledSpinBox("MAX", 1, 20, 1)

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.spent_dices)
        layout.addWidget(self.max_dices)

        return layout

class DeathSavesWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.label = QLabel("DEATH SAVES")
        success_layout = QHBoxLayout()
        self.successes = [QCheckBox() for _ in range(3)]
        [success_layout.addWidget(box, alignment=Qt.AlignmentFlag.AlignCenter) for box in self.successes]
        self.successes_label = QLabel("SUCCESSES")
        failure_layout = QHBoxLayout()
        self.failures = [QCheckBox() for _ in range(3)]
        [failure_layout.addWidget(box, alignment=Qt.AlignmentFlag.AlignCenter) for box in self.failures]
        self.failures_label = QLabel("FAILURES")

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(success_layout)
        layout.addWidget(self.successes_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(failure_layout)
        layout.addWidget(self.failures_label, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

class LifeWidget(QWidget):
    def __init__(self, character:Character):
        super().__init__()
        layout = self.create_layout(character)
        self.setLayout(layout)

    def create_layout(self, character: Character):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.hp = HitPointsWidget(character)
        self.hit_dices = HitDicesWidget(character)
        self.death_saves = DeathSavesWidget(character)

        layout.addWidget(self.hp, stretch=2)
        layout.addWidget(self.hit_dices, stretch=1)
        layout.addWidget(self.death_saves, stretch=1)

        return layout
