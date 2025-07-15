from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QAbstractItemView,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt

from model.generic_model import ExplorableModel, FilterOption
from ui.feat_detail_window import FeatDetailWindow
from ui.widgets.SpellList import DDTable


class GenericTable(QWidget):
    """A generic table class that can be used to display a model with a list."""

    def __init__(self, model: ExplorableModel, details_windows):
        super().__init__()
        self.model = model
        self.details_windows = details_windows

        layout = QVBoxLayout()
        self.setLayout(layout)

        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        self.line_filters: dict[str, QLineEdit] = {}
        for fname, field in model.__dataclass_fields__.items():
            if field.metadata.get("filter_type") == FilterOption.LINE_EDIT:
                line_filter = QLineEdit()
                line_filter.setPlaceholderText(field.metadata.get("label", fname))
                line_filter.textChanged.connect(self.live_filter)
                line_filter.setClearButtonEnabled(True)
                line_filter.setAcceptDrops(False)
                self.line_filters[fname] = line_filter
        for line_filter in self.line_filters.values():
            filter_layout.addWidget(line_filter)

        self.table = DDTable()
        self.table.verticalHeader().setVisible(False)
        self.table.setDragEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.table_double_click)
        layout.addWidget(self.table)

    def apply_filters(self, field_filters: dict[str, list[str | int]]):
        """Apply filters to the table based on the provided field filters."""
        self.table.setSortingEnabled(False)
        items = self.model.get_collection().get_items()

        self.filtered_items = [
            item
            for item in items
            if all(
                field.metadata["filter_type"].value_in_filter(
                    getattr(item, field.name), field_filters.get(field.name, [])
                )
                for field in item.__dataclass_fields__.values()
                if field.metadata.get("filter_type") is not None
            )
        ]

    def update_display(self, headers, options):
        """Update the display of the table based on the model."""
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(self.filtered_items))
        for row, item in enumerate(self.filtered_items):
            for col, key in enumerate(options):
                if key == "checkbox":
                    item_widget = QTableWidgetItem()
                    item_widget.setFlags(
                        Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
                    )
                    item_widget.setCheckState(Qt.CheckState.Unchecked)
                    self.table.setItem(row, col, item_widget)
                    continue
                value = item.__getattribute__(key)
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
        """Apply live filtering based on the text in the line edits."""
        field_filters = {}
        for fname, line_edit in self.line_filters.items():
            if line_edit.text():
                field_filters[fname] = line_edit.text()

        for row in range(self.table.rowCount()):
            item = self.filtered_items[row]
            matches = all(
                field.metadata["filter_type"].value_in_filter(
                    getattr(item, field.name), field_filters.get(field.name, "")
                )
                for field in item.__dataclass_fields__.values()
                if field.metadata.get("filter_type") is FilterOption.LINE_EDIT
            )
            self.table.setRowHidden(row, not matches)

    def toggle_column_display(self, index, hide):
        self.table.setColumnHidden(index, hide)

    def get_selected_count(self, item):
        selected_count = 0
        for row in range(self.table.rowCount()):
            if (
                self.table.item(row, 0)
                and self.table.item(row, 0).checkState() == Qt.CheckState.Checked
            ):
                selected_count += 1

        return selected_count, selected_count == self.table.rowCount()

    def get_selected_items(self):
        selected_items = []
        for row in range(self.table.rowCount()):
            if (
                self.table.item(row, 0)
                and self.table.item(row, 0).checkState() == Qt.CheckState.Checked
            ):
                selected_items.append(self.filtered_items[row])
        return selected_items

    def toggle_select_all(self, state):
        for row in range(self.table.rowCount()):
            self.table.item(row, 0).setCheckState(state)

    def table_double_click(self, row, column):
        """Handle double-click on a table cell."""
        item_name = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
        if item_name:
            item = self.model.get_collection().get_item(item_name)
            self.show_item_details(item)

    def show_item_details(self, item):
        """Show details of the selected item in a new window."""
        if self.details_windows is not None:
            details_window = self.details_windows.get(item.name)
            if details_window:
                details_window.show()
            else:
                # Create a new details window if it doesn't exist
                window_class = self.model.get_detail_windowclass()
                window = window_class(item, self.details_windows)
                self.details_windows[item.name] = window
                window.main_controller = self
                window.show()
        else:
            print(f"No details window available for {item.name}")
