from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QMessageBox
from ui.widgets.generic_tab import GenericTab
from ui.widgets.specificTabs.spell_tab.spell_grimoire_widget import SpellGrimoireWidget
from models.spell_model import Spell

class SpellTab(GenericTab):
    def __init__(self, shared_dict):
        self._shared_dict = shared_dict
        super().__init__(Spell)

    def create_layout(self):
        layout = QHBoxLayout()
        left_layout = super().create_layout()
        layout.addLayout(left_layout)

        ##### Right part #####
        self.list_widget = SpellGrimoireWidget(self._shared_dict, self)
        layout.addWidget(self.list_widget)
        self.list_widget.html_export_btn.clicked.connect(self.export_spell_list_html)
        self.list_widget.hide()

        ##### Side grimoire button #####
        spell_list_hide_btn = QPushButton()
        spell_list_hide_btn.clicked.connect(
            lambda: self.list_widget.setHidden(
                bool(
                    spell_list_hide_btn.setText(
                        "<" if self.list_widget.isHidden() else ">"
                    )
                    or not (self.list_widget.isHidden())
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
        spell_list = self.list_widget.get_spells()

        if not spell_list:
            QMessageBox.warning(
                self,
                "Aucun sort dans la liste",
                "Veuillez ajouter au moins un sort dans la liste pour exporter.",
            )
            return

        self.export_html(spell_list)
