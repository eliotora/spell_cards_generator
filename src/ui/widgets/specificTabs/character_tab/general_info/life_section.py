from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox
from PySide6.QtCore import Qt

from ..underlabeled_line_edit import UnderlabeledLineEdit

class HitPointsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.label = QLabel("HIT POINTS")
        self.current_hp = UnderlabeledLineEdit("CURRENT")
        self.temp_hp = UnderlabeledLineEdit("TEMP")
        self.max_hp = UnderlabeledLineEdit("MAX")


        layout.addWidget(self.label, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_hp, 1, 0, 2, 1)
        layout.addWidget(self.temp_hp, 1, 1, 1, 1)
        layout.addWidget(self.max_hp, 2, 1, 1, 1)

        return layout


class HitDicesWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.label = QLabel("HIT DICE")
        self.spent_dices = UnderlabeledLineEdit("SPENT")
        self.max_dices = UnderlabeledLineEdit("MAX")

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.spent_dices)
        layout.addWidget(self.max_dices)

        return layout

class DeathSavesWidget(QWidget):
    def __init__(self):
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
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20,0,20,0)

        self.hp = HitPointsWidget()
        self.hit_dices = HitDicesWidget()
        self.death_saves = DeathSavesWidget()

        layout.addWidget(self.hp, stretch=2)
        layout.addWidget(self.hit_dices, stretch=1)
        layout.addWidget(self.death_saves, stretch=1)

        return layout
