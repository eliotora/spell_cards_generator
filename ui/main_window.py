from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QLabel,
    QSpinBox,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from export.html_export import html_export
from model.spell_model import SpellModels
from profile_loader import load_profiles_from_folder
from ui.spell_detail_window import SpellDetailWindow
from ui.widgets.spell_grimoire_widget import SpellGrimoireWidget
from ui.widgets.multi_selection_list import MultiSelectionListWidget
from ui.widgets.SpellList import SpellTable
from ui.widgets.spell_filters import SpellFilters
from ui.widgets.filterable_table import FilterableTable
from utils.paths import get_export_dir
import os
import json


class MainWindow(QMainWindow):
    details_windows = {}
    default_export_dir = os.path.join(os.getcwd(), "output")

    def __init__(self):
        super().__init__()
        self.spell_models = SpellModels()
        self.setWindowTitle("Liste des Sorts")

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        ##### Left part #####
        self.left_col = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_col.setLayout(self.left_layout)
        self.layout.addWidget(self.left_col)
        self.filters_and_table = FilterableTable(self.details_windows)
        self.filters_widget = SpellFilters(self.apply_filters, self.description_checkbox_event)
        self.left_layout.addWidget(self.filters_widget)
        self.left_layout.addWidget(self.filters_and_table)

        self.load_spells()
        self.load_profiles()

        # ==== Export section ====
        export_options_layout = QHBoxLayout()
        select_data_layout = QHBoxLayout()
        select_data_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.select_everything_checkbox = QCheckBox("Tout sélectionner")
        self.select_everything_checkbox.setChecked(False)
        self.select_everything_checkbox.checkStateChanged.connect(
            self.filters_and_table.toggle_select_all
        )
        self.print_vo_name_checkbox = QCheckBox("Imprimer le nom en VO")
        self.print_source_checkbox = QCheckBox("Imprimer la source")
        select_data_layout.addWidget(self.select_everything_checkbox)
        select_data_layout.addWidget(self.print_vo_name_checkbox)
        select_data_layout.addWidget(self.print_source_checkbox)

        export_mode_layout = QHBoxLayout()
        export_mode_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.export_mode_label = QLabel("Format:")
        self.radio_rules = QRadioButton("Règles")
        self.radio_grimoire = QRadioButton("Grimoire")
        self.radio_cards = QRadioButton("Cartes")
        self.radio_rules.setChecked(True)

        self.format_group = QButtonGroup()
        self.format_group.addButton(self.radio_rules, id=0)
        self.format_group.addButton(self.radio_grimoire, id=1)
        self.format_group.addButton(self.radio_cards, id=2)
        export_mode_layout.addWidget(self.export_mode_label)
        export_mode_layout.addWidget(self.radio_rules)
        export_mode_layout.addWidget(self.radio_grimoire)
        export_mode_layout.addWidget(self.radio_cards)

        export_options_layout.addLayout(select_data_layout)
        export_options_layout.addLayout(export_mode_layout)
        self.filters_and_table.table.itemChanged.connect(self.update_selected_spell_count)

        self.left_layout.addLayout(export_options_layout)

        # Adding export buttons
        export_buttons_layout = QHBoxLayout()
        self.selected_spell_count_label = QLabel("Sorts sélectionnés: 0")

        # Boutons d'export
        export_pdf_btn = QPushButton("Exporter en PDF")
        # export_pdf_btn.clicked.connect(self.export_pdf)
        export_pdf_btn.setDisabled(True)

        export_html_btn = QPushButton("Exporter en HTML")
        export_html_btn.clicked.connect(self.export_selected_html)

        export_buttons_layout.addWidget(self.selected_spell_count_label)
        export_buttons_layout.addWidget(export_pdf_btn)
        export_buttons_layout.addWidget(export_html_btn)
        self.left_layout.addLayout(export_buttons_layout)

        ##### Right part #####
        self.spell_grimoire = SpellGrimoireWidget(self.details_windows, self)
        self.layout.addWidget(self.spell_grimoire)
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

        self.layout.addWidget(spell_list_hide_btn)

        self.filters_widget.load_filters()

        self.showMaximized()

    def load_profiles(self):
        self.profiles = load_profiles_from_folder("data")

    def get_profile(self, profile_name):
        for p in self.profiles:
            if p["nom"] == profile_name:
                return p
        return None

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

    def spell_list_double_click(self, item):
        spell_name = item.text()
        self.show_spell_details(self.spell_models.get_spell(spell_name))

    def description_checkbox_event(self, state):
        self.filters_and_table.toggle_description_filtering(state)
        self.apply_filters()

    def update_selected_spell_count(self, item):
        if item.column() != 0:
            return

        # Update the count of selected spells
        selected_count = self.filters_and_table.get_selected_spell_count(item)

        self.selected_spell_count_label.setText(f"Sorts sélectionnés: {selected_count}")
        self.select_everything_checkbox.blockSignals(True)
        self.select_everything_checkbox.setChecked(
            selected_count == self.filters_and_table.table.rowCount()
        )
        self.select_everything_checkbox.blockSignals(False)

    def export_html(self, spells):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer HTML",
            str(get_export_dir()),
            "Fichier HTML (*.html)",
        )
        if not path:
            return  # L'utilisateur a annulé

        if self.radio_rules.isChecked():
            mode = "rules"
        elif self.radio_grimoire.isChecked():
            mode = "grimoire"
        elif self.radio_cards.isChecked():
            mode = "cards"

        show_VO_name = self.print_vo_name_checkbox.isChecked()
        show_source = self.print_source_checkbox.isChecked()

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

    def closeEvent(self, event):
        for k, w in self.details_windows.items():
            w.close()
