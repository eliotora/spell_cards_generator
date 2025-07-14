from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog
from ui.widgets.maneuversTab import maneuvers_filters, maneuvers_table, maneuvers_export
from model.maneuvers_model import ManeuversModel
import os
from utils.paths import get_export_dir
from export.html_export import html_export, MANEUVER

class ManeuversTabContent(QWidget):
    details_windows = {}
    default_export_dir = os.path.join(os.getcwd(), "output")

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.maneuvers_model = ManeuversModel()

        # === Filters ===
        self.filters_and_table = maneuvers_table.ManeuverTable(self.details_windows)
        self.filters_widget = maneuvers_filters.ManeuverFilters(self.apply_filters, self.description_checkbox_event, self.filters_and_table.toggle_column_display)
        layout.addWidget(self.filters_widget)
        layout.addWidget(self.filters_and_table)

        self.load_maneuvers()
        self.update_display()

        # === Export ===
        self.export_section = maneuvers_export.ManeuverExport()
        self.export_section.select_everything_checkbox.checkStateChanged.connect(self.filters_and_table.toggle_select_all)
        self.export_section.export_html_btn.clicked.connect(self.export_selected_html)
        layout.addWidget(self.export_section)
        self.filters_and_table.table.itemChanged.connect(self.update_selected_maneuver_count)

    def apply_filters(self):
        # Filters
        selected_sources = self.filters_widget.get_filters()
        self.filters_and_table.apply_filters(selected_sources)

        # Update table
        headers = [
            "✔",
            "Manoeuvre",
            "VF",
            "VO",
            "Description",
            "Source"
        ]
        headers = [header for header in headers if header is not None]
        cols = [
            "checkbox",
            "nom",
            "nom_VF",
            "nom_VO",
            "description_short",
            "source"
        ]
        cols = [col for col in cols if col is not None]
        self.filters_and_table.display_maneuvers(headers, cols)

    def description_checkbox_event(self, state):
        self.filters_and_table.toggle_description_filtering(state)
        self.apply_filters()

    def load_maneuvers(self):
        maneuvers = self.maneuvers_model.get_maneuvers()

        self.sources = sorted(set(maneuver.get("source", "") for maneuver in maneuvers))
        self.filters_widget.load_filter_options(self.sources)

        self.apply_filters()

    def update_display(self):
        self.filters_widget.fire_checked_signals()

    def update_selected_maneuver_count(self, item):
        if item.column() != 0:
            return
        selected_count, all = self.filters_and_table.get_selected_maneuver_count(item)
        self.export_section.update_selected_count(selected_count, all)

    def export_selected_html(self):
        selected_maneuvers = self.filters_and_table.get_selected_maneuvers()
        if not selected_maneuvers:
            QMessageBox.warning(self, "Aucun résultat", "Veuillez sélectionner au moins une manoeuvre à exporter.")
            return

        self.export_html(selected_maneuvers)

    def export_html(self, maneuvers):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer HTML",
            get_export_dir(self.default_export_dir),
            "HTML Files (*.html);;All Files (*)"
        )

        mode, show_VO_name, show_source = self.export_section.get_export_options()

        if maneuvers and path:
            html_export(
                maneuvers, path, mode, show_VO_name=show_VO_name, show_source=show_source, data_type=MANEUVER
            )
            QMessageBox.information(
                self,
                "Exportation réussie",
                f"{len(maneuvers)} manoeuvres ont été exportées avec succès en HTML."
            )