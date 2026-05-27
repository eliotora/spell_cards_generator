from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from src.ui.widgets.specificTabs.character_tab.spellcasting.spellcasting_ability import SpellcastingAbilityWidget
from src.ui.widgets.specificTabs.character_tab.spellcasting.spell_slots import SpellSlotWidget
from src.ui.widgets.specificTabs.character_tab.spellcasting.spell_table import SpellTableWidget, SpellRow

from src.models import SpellModel

class SpellcastingSectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0,0,0,0)

        self.spell_ability_widget = SpellcastingAbilityWidget()
        self.spell_slot_widget = SpellSlotWidget()
        self.spell_table = SpellTableWidget()

        spells = SpellModel.collection.items()
        for spell in spells[0:10]:
            self.spell_table.add_spell(spell)

        top_layout.addWidget(self.spell_ability_widget, stretch=1)
        top_layout.addWidget(self.spell_slot_widget, stretch=2)

        layout.addLayout(top_layout)
        layout.addWidget(self.spell_table, stretch=2)

        return layout