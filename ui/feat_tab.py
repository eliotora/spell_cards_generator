from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog
from ui.widgets.featsTab import feat_filters, feat_table, feat_export
from model.feat_model import FeatModels
import os
from utils.paths import get_export_dir
from export.html_export import html_export, FEAT


class FeatTabContent(QWidget):
    details_windows = {}
    default_export_dir = os.path.join(os.getcwd(), "output")

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.feat_models = FeatModels()

        # === Filters ===
        self.filters_and_table = feat_table.FeatTable(self.details_windows)
        self.filters_widget = feat_filters.FeatFilters(self.apply_filters, self.description_checkbox_event, self.filters_and_table.toggle_column_display)
        layout.addWidget(self.filters_widget)
        layout.addWidget(self.filters_and_table)

        self.load_feats()
        self.update_display()


        # === Table ===

        # === Export ===
        self.export_section = feat_export.FeatExport()
        self.export_section.select_everything_checkbox.checkStateChanged.connect(self.filters_and_table.toggle_select_all)
        self.export_section.export_html_btn.clicked.connect(self.export_selected_html)
        layout.addWidget(self.export_section)
        self.filters_and_table.table.itemChanged.connect(self.update_selected_feat_count)


    def apply_filters(self):
        # Filters
        selected_sources = self.filters_widget.get_filters()
        self.filters_and_table.apply_filters(selected_sources)

        # Update table
        headers = [
            "✔",
            "Don",
            "VF",
            "VO",
            "Prérequis",
            "Description",
            "Source"
        ]
        headers = [header for header in headers if header is not None]
        cols = [
            "checkbox",
            "nom",
            "nom_VF",
            "nom_VO",
            "prérequis",
            "description_short",
            "source"
        ]
        cols = [col for col in cols if col is not None]
        self.filters_and_table.display_feats(headers, cols)

    def description_checkbox_event(self, state):
        self.filters_and_table.toggle_description_filtering(state)
        self.apply_filters()

    def load_feats(self):
        feats = self.feat_models.get_feats()

        self.sources = sorted(set(feat.get("source", "") for feat in feats))
        self.filters_widget.load_filter_options(self.sources)

        self.apply_filters()

    def update_display(self):
        self.filters_widget.fire_checked_signals()

    def update_selected_feat_count(self, item):
        if item.column() != 0:
            return

        # Update the count of selected feats
        selected_count, all = self.filters_and_table.get_selected_feat_count(item)
        self.export_section.change_selected_feat_count_label(selected_count, all)

    def export_selected_html(self):
        selected_spells = self.filters_and_table.get_selected_feats()
        if not selected_spells:
            QMessageBox.warning(
                self,
                "Aucun sort sélectionné",
                "Veuillez sélectionner au moins un sort à exporter.",
            )
            return

        self.export_html(selected_spells)

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
                spells, path, mode, show_VO_name=show_VO_name, show_source=show_source, data_type=FEAT
            )
            QMessageBox.information(
                self,
                "Exportation réussie",
                f"{len(spells)} sorts ont été exportés avec succès en HTML.",
            )
