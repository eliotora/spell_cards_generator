from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QAbstractItemView, QTableWidgetItem
from ui.feat_detail_window import FeatDetailWindow
from ui.widgets.SpellList import SpellTable
from model.feat_model import FeatModels
from PyQt6.QtCore import Qt

class FeatTable(QWidget):
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
        self.table.cellDoubleClicked.connect(self.table_feat_double_click)
        layout.addWidget(self.table)

    def apply_filters(self, sources):
        self.table.setSortingEnabled(False)
        feats = FeatModels().get_feats()

        self.filtered_feats = [
            feat
            for feat in feats
            if (
                feat.get("source") in sources
            )
        ]

    def display_feats(self, headers, options):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(self.filtered_feats))
        for row, feat in enumerate(self.filtered_feats):
            for col, key in enumerate(options):
                if key == "checkbox":
                    item = QTableWidgetItem()
                    item.setFlags(
                        Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
                    )
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.table.setItem(row, col, item)
                    continue
                value = feat.get(key, "")
                if isinstance(value, list):
                    values = [v.split("(")[0].strip() for v in value if v]
                    value = ", ".join(values)
                elif isinstance(value, bool):
                    value = "Oui" if value else "Non"
                if value is None:
                    value = ""
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def live_filter(self):
        name_filter = self.name_filter.text().strip().lower()
        description_filter = self.description_filter.text().strip().lower()

        for row in range(self.table.rowCount()):
            feat = self.filtered_feats[row]
            matches_name = name_filter in feat.get("nom", "").lower() or (
                feat.get("nom_VF", "") is not None
                and name_filter in feat.get("nom_VF", "").lower()
            )
            matches_description = (
                description_filter in feat.get("description_short", "").lower()
            )

            if matches_name and (
                not self.description_filter.isVisible() or matches_description
            ):
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

    def get_selected_feats(self):
        selected_feats = []
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.CheckState.Checked:
                selected_feats.append(self.filtered_feats[row])
        return selected_feats

    def toggle_select_all(self, state):
        for row in range(self.table.rowCount()): self.table.item(row, 0).setCheckState(state)

    def table_feat_double_click(self, row, column):
        feat_name = self.table.item(row, 1).text()
        feat = FeatModels().get_feat(feat_name)
        self.show_spell_details(feat)

    def show_spell_details(self, feat):
        window = FeatDetailWindow(feat, self.details_windows)
        self.details_windows[feat["nom"]] = window
        window.main_controler = self
        window.show()

    def get_selected_feat_count(self, item):
        selected_count = 0
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        return selected_count, selected_count == self.table.rowCount()