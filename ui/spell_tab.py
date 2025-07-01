from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QFileDialog, QMessageBox
from model.spell_model import SpellModels
from ui.widgets.spellsTab.export_section import ExportSection
from ui.widgets.spellsTab.filterable_table import FilterableTable
from ui.widgets.spellsTab.spell_filters import SpellFilters
from ui.widgets.spellsTab.spell_grimoire_widget import SpellGrimoireWidget
from export.html_export import html_export
from utils.paths import get_export_dir
import os


class SpellTabContent(QWidget):
    details_windows = {}
    default_export_dir = os.path.join(os.getcwd(), "output")

    def __init__(self):
        super().__init__()
        self.spell_models = SpellModels()
        # Main layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        ##### Left part #####
        self.left_col = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_col.setLayout(self.left_layout)
        layout.addWidget(self.left_col)
        self.filters_and_table = FilterableTable(self.details_windows)
        self.filters_widget = SpellFilters(self.apply_filters, self.description_checkbox_event, self.filters_and_table.toggle_column_display)
        self.left_layout.addWidget(self.filters_widget)
        self.left_layout.addWidget(self.filters_and_table)

        self.load_spells()
        self.update_display()

        # ==== Export section ====

        self.export_section = ExportSection()
        self.export_section.select_everything_checkbox.checkStateChanged.connect(self.filters_and_table.toggle_select_all)
        self.export_section.export_html_btn.clicked.connect(self.export_selected_html)
        self.left_layout.addWidget(self.export_section)
        self.filters_and_table.table.itemChanged.connect(self.update_selected_spell_count)

        ##### Right part #####
        self.spell_grimoire = SpellGrimoireWidget(self.details_windows, self)
        layout.addWidget(self.spell_grimoire)
        self.spell_grimoire.html_export_btn.clicked.connect(self.export_spell_list_html)
        self.spell_grimoire.hide()

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

        self.filters_widget.load_filters()

    def load_spells(self):
        spells = self.spell_models.get_spells()

        self.schools = sorted(set(spell.get("école", "") for spell in spells))
        self.sources = sorted(set(spell.get("source", "") for spell in spells))
        self.classes = sorted(
            {cls for spell in spells for cls in spell.get("classes", [])}
        )
        self.filters_widget.load_filter_options(self.schools, self.sources, self.classes)

        self.apply_filters()

    def apply_filters(self):
        # Filters
        selected_classes, selected_sources,selected_schools, min_level, max_level = self.filters_widget.get_filters()
        self.filters_and_table.apply_filters(selected_classes, selected_sources, selected_schools, min_level, max_level)

        # Update table
        headers = self.filters_widget.get_display_headers()
        headers = [header for header in headers if header is not None]
        cols = self.filters_widget.get_display_options()
        cols = [col for col in cols if col is not None]
        self.filters_and_table.display_spells(headers, cols)

    def update_display(self):
        self.filters_widget.fire_checked_signals()

    def description_checkbox_event(self, state):
        self.filters_and_table.toggle_description_filtering(state)
        self.apply_filters()

    def update_selected_spell_count(self, item):
        if item.column() != 0:
            return

        # Update the count of selected spells
        selected_count, all = self.filters_and_table.get_selected_spell_count(item)
        self.export_section.change_selected_spell_count_label(selected_count, all)

    def export_html(self, spells):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer HTML",
            str(get_export_dir()),
            "Fichier HTML (*.html)",
        )
        if not path:
            return  # L'utilisateur a annulé

        mode, show_VO_name, show_source = self.export_section.get_export_options()

        if spells and path:
            html_export(
                spells, path, mode, show_VO_name=show_VO_name, show_source=show_source
            )
            QMessageBox.information(
                self,
                "Exportation réussie",
                f"{len(spells)} sorts ont été exportés avec succès en HTML.",
            )

    def export_selected_html(self):
        selected_spells = self.filters_and_table.get_selected_spells()
        if not selected_spells:
            QMessageBox.warning(
                self,
                "Aucun sort sélectionné",
                "Veuillez sélectionner au moins un sort à exporter.",
            )
            return

        self.export_html(selected_spells)

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
