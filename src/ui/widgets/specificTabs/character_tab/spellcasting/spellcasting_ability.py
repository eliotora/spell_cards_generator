from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from src.ui.widgets.specificTabs.character_tab.underlabeled_edits import UnderlabeledLineEdit

class SpellcastingAbilityWidget(QWidget):
    profiency: int = 2
    modifier: int = 0

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        self.ability = UnderlabeledLineEdit("SPELLCASTING ABILITY")

        layout.addWidget(self.ability)

        h_layout_1 = QHBoxLayout()
        self.modifier_edit = QLineEdit(alignment=Qt.AlignmentFlag.AlignRight)
        fm = QFontMetrics(self.modifier_edit.font())
        self.modifier_edit.setFixedSize(fm.horizontalAdvance("M")*3,fm.height()+6)
        self.modifier_label = QLabel("SPELLCASTING MODIFIER")
        h_layout_1.addWidget(self.modifier_edit, alignment=Qt.AlignmentFlag.AlignRight)
        h_layout_1.addWidget(self.modifier_label, alignment=Qt.AlignmentFlag.AlignLeft)
        h_layout_1.addStretch()
        layout.addLayout(h_layout_1)

        h_layout_2 = QHBoxLayout()
        self.save_dc = QLineEdit(alignment=Qt.AlignmentFlag.AlignRight)
        fm = QFontMetrics(self.save_dc.font())
        self.save_dc.setFixedSize(fm.horizontalAdvance("M")*3,fm.height()+6)
        self.save_dc_label = QLabel("SPELL SAVE DC")
        h_layout_2.addWidget(self.save_dc, alignment=Qt.AlignmentFlag.AlignRight)
        h_layout_2.addWidget(self.save_dc_label, alignment=Qt.AlignmentFlag.AlignLeft)
        h_layout_2.addStretch()
        layout.addLayout(h_layout_2)

        h_layout_3 = QHBoxLayout()
        self.attack_bonus = QLineEdit(alignment=Qt.AlignmentFlag.AlignRight)
        fm = QFontMetrics(self.attack_bonus.font())
        self.attack_bonus.setFixedSize(fm.horizontalAdvance("M")*3,fm.height()+6)
        self.attack_bonus_label = QLabel("SPELL ATTACK BONUS")
        h_layout_3.addWidget(self.attack_bonus, alignment=Qt.AlignmentFlag.AlignRight)
        h_layout_3.addWidget(self.attack_bonus_label, alignment=Qt.AlignmentFlag.AlignLeft)
        h_layout_3.addStretch()
        layout.addLayout(h_layout_3)

        return layout

    def update_display(self):
        self.modifier_edit.setText(f"+{self.modifier}" if self.modifier >= 0 else f"{self.modifier}")
        self.save_dc.setText(f"{8 + self.modifier + self.profiency}")
        self.modifier_edit.setText(f"+{self.modifier + self.profiency}" if self.modifier + self.profiency >= 0 else f"{self.modifier + self.profiency}")

    def update_modifier(self, value:int):
        self.modifier = value
        self.update_display()

    def update_proficency(self, value:int):
        self.profiency = value
        self.update_display()
