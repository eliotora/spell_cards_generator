from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QAbstractItemView, QTableWidgetItem
from ui.maneuvers_detail_window import ManeuverDetailWindow
from ui.widgets.SpellList import DDTable
from model.maneuvers_model import ManeuversModel
from PyQt6.QtCore import Qt

class ManeuverTable(QWidget):
    details_windows = None

    def __init__(self, details_windows):
        super().__init__()
        self.details_windows = details_windows

        layout = QVBoxLayout()
        self.setLayout(layout)

        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("nom")
        self.name_filter.textChanged.connect(self.live_filter)
        self.name_filter.setClearButtonEnabled(True)
        self.name_filter.setAcceptDrops(False)
        filter_layout.addWidget(self.name_filter)

        self.description_filter = QLineEdit()
        self.description_filter.setPlaceholderText("description")
        self.description_filter.textChanged.connect(self.live_filter)
        self.description_filter.setClearButtonEnabled(True)
        self.description_filter.setAcceptDrops(False)
        self.description_filter.setVisible(False)  # Initially hidden
        filter_layout.addWidget(self.description_filter)

        self.table = DDTable()
        self.table.verticalHeader().setVisible(False)
        self.table.setDragEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.table_maneuver_double_click)
        layout.addWidget(self.table)

    def apply_filters(self, sources):
        self.table.setSortingEnabled(False)
        maneuvers = ManeuversModel().get_maneuvers()

        self.filtered_maneuvers = [
            maneuver for maneuver in maneuvers if (maneuver.get("source") in sources)
        ]

    def display_maneuvers(self, headers, cols):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.filtered_maneuvers))

        for row, maneuver in enumerate(self.filtered_maneuvers):
            for col, col_name in enumerate(cols):
                if col_name == "checkbox":
                    item = QTableWidgetItem()
                    item.setCheckState(Qt.CheckState.Unchecked)
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    self.table.setItem(row, col, item)
                    continue
                value = maneuver.get(col_name, "")
                if isinstance(value, list):
                    values = [v.split("(")[0].strip() for v in value if v]
                    value = ", ".join(values)
                elif isinstance(value, bool):
                    value = "Oui" if value else "Non"
                if value is None:
                    value = ""
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)

    def live_filter(self):
        name_filter = self.name_filter.text().lower()
        description_filter = self.description_filter.text().lower()

        for row in range(self.table.rowCount()):
            maneuver = self.filtered_maneuvers[row]
            matches_name = name_filter in maneuver.get("nom", "").lower() or (
                name_filter in maneuver.get("nom_VF", "").lower() or
                name_filter in maneuver.get("nom_VO", "").lower()
            )
            matches_description = description_filter in maneuver.get("description_short", "").lower()

            if matches_name and (not self.description_filter.isVisible() or matches_description):
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def toggle_description_filtering(self, state):
        self.description_filter.setVisible(state == Qt.CheckState.Checked)
        self.description_filter.clear()
        self.toggle_column_display(5, state == Qt.CheckState.Unchecked)

    def toggle_column_display(self, index, hide):
        self.table.setColumnHidden(index, hide)

    def get_selected_spell_count(self, item):
        selected_count = 0
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        return selected_count, selected_count == self.table.rowCount()

    def get_selected_maneuvers(self):
        selected_maneuvers = []
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                maneuver = self.filtered_maneuvers[row]
                selected_maneuvers.append(maneuver)
        return selected_maneuvers

    def toggle_select_all(self, state):
        for row in range(self.table.rowCount()):
            self.table.item(row, 0).setCheckState(state)

    def table_maneuver_double_click(self, row, column):
        maneuver_name = self.table.item(row, 1).text()
        maneuver = ManeuversModel().get_maneuver(maneuver_name)
        self.show_maneuver_details(maneuver)

    def show_maneuver_details(self, maneuver):
        window = ManeuverDetailWindow(maneuver)
        self.details_windows[maneuver["nom"]] = window
        window.main_controler = self
        window.show()

    def get_selected_maneuver_count(self, item):
        selected_count = 0
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        return selected_count, selected_count == self.table.rowCount()