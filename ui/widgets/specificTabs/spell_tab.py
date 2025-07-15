from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QMessageBox
from ui.widgets.generic_tab import GenericTab
from ui.widgets.specificTabs.spell_grimoire_widget import SpellGrimoireWidget
from model.spell_model import Spell

class SpellTab(GenericTab):
    def __init__(self, details_windows):
        super().__init__(Spell, details_windows)

    def create_layout(self):
        layout = QHBoxLayout()
        left_layout = super().create_layout()
        layout.addLayout(left_layout)

        ##### Right part #####
        self.spell_grimoire = SpellGrimoireWidget(self.details_windows, self)
        layout.addWidget(self.spell_grimoire)
        self.spell_grimoire.html_export_btn.clicked.connect(self.export_spell_list_html)
        self.spell_grimoire.hide()

        ##### Side grimoire button #####
        spell_list_hide_btn = QPushButton()
        spell_list_hide_btn.clicked.connect(
            lambda: self.spell_grimoire.setHidden(
                bool(
                    spell_list_hide_btn.setText(
                        "<" if self.spell_grimoire.isHidden() else ">"
                    )
                    or not (self.spell_grimoire.isHidden())
                )
            )
        )
        spell_list_hide_btn.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding
        )
        spell_list_hide_btn.setFixedWidth(20)
        spell_list_hide_btn.setText(">")
        layout.addWidget(spell_list_hide_btn)

        return layout

    def export_spell_list_html(self):
        spell_list = self.spell_grimoire.get_spells()

        if not spell_list:
            QMessageBox.warning(
                self,
                "Aucun sort dans la liste",
                "Veuillez ajouter au moins un sort dans la liste pour exporter.",
            )
            return

        self.export_html(spell_list)
