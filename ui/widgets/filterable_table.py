from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QAbstractItemView, QTableWidgetItem
from ui.spell_detail_window import SpellDetailWindow
from ui.widgets.SpellList import SpellTable
from model.spell_model import SpellModels
from PyQt6.QtCore import Qt

class FilterableTable(QWidget):
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

        self.table = SpellTable()
        self.table.verticalHeader().setVisible(False)
        self.table.setDragEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.table_spell_double_click)
        layout.addWidget(self.table)

    def apply_filters(self, classes, sources, schools, min_lvl, max_lvl):
        self.table.setSortingEnabled(False)
        spells = SpellModels().get_spells()

        self.filtered_spells = [
            spell
            for spell in spells
            if (
                any(cls in classes for cls in spell.get("classes", []))
                and spell.get("source") in sources
                and spell.get("école") in schools
                and min_lvl <= spell.get("niveau", 0) <= max_lvl
            )
        ]

    def display_spells(self, headers, options):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(self.filtered_spells))
        for row, spell, in enumerate(self.filtered_spells):
            for col, key in enumerate(options):
                if key == "checkbox":
                    item = QTableWidgetItem()
                    item.setFlags(
                        Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
                    )
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.table.setItem(row, col, item)
                    continue
                value = spell.get(key, "")
                if isinstance(value, list):
                    values = [v.split("(")[0].strip() for v in value if v]
                    value = ", ".join(values)
                elif isinstance(value, bool):
                    value = "Oui" if value else "Non"
                elif key == "temps_d'incantation":
                    value = spell.get("temps_d'incantation", "").split(",")[0].strip()
                if value is None:
                    value = ""
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def live_filter(self):
        name_filter = self.name_filter.text().strip().lower()
        description_filter = self.description_filter.text().strip().lower()

        for row in range(self.table.rowCount()):
            spell = self.filtered_spells[row]
            matches_name = name_filter in spell.get("nom", "").lower() or (
                spell.get("nom_VF", "") is not None
                and name_filter in spell.get("nom_VF", "").lower()
            )
            matches_description = (
                description_filter in spell.get("description_short", "").lower()
            )

            if matches_name and (
                not self.description_filter.isVisible() or matches_description
            ):
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def toggle_description_filtering(self, state):
        if state == Qt.CheckState.Checked:
            self.description_filter.setVisible(True)
        else:
            self.description_filter.setVisible(False)
            self.description_filter.clear()

    def get_selected_spell_count(self, item):
        selected_count = 0
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        return selected_count, selected_count == self.table.rowCount()

    def get_selected_spells(self):
        selected_spells = []
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.CheckState.Checked:
                selected_spells.append(self.filtered_spells[row])
        return selected_spells

    def toggle_select_all(self, state):
        for row in range(self.table.rowCount()): self.table.item(row, 0).setCheckState(state)

    def table_spell_double_click(self, row, column):
        spell_name = self.table.item(row, 1).text()
        spell = SpellModels().get_spell(spell_name)
        self.show_spell_details(spell)

    def show_spell_details(self, spell):
        window = SpellDetailWindow(spell)
        self.details_windows[spell["nom"]] = window
        window.main_controler = self
        window.show()