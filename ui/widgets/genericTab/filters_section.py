from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QListWidgetItem,
    QSpinBox,
)
from PyQt6.QtCore import Qt
from ui.widgets.multi_selection_list import MultiSelectionListWidget
import os, json
from typing import Type, Generic, TypeVar
from model.generic_model import ExplorableModel, FilterOption, VisibilityOption

T = TypeVar("T", bound=ExplorableModel)


class GenericFilter(QWidget, Generic[T]):
    def __init__(
        self,
        model: Type[T],
        apply_filters
    ):
        super().__init__()
        self.model = model
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --- Filters ---
        self.filters: dict[
            str, MultiSelectionListWidget | tuple[QSpinBox, QSpinBox]
        ] = {}
        for fname, field in model.__dataclass_fields__.items():
            filter_type = field.metadata.get("filter_type")
            if filter_type == FilterOption.LIST:
                filter = MultiSelectionListWidget(field.metadata.get("label"))
                self.filters[fname] = filter
                layout.addWidget(filter)
            elif filter_type == FilterOption.INT_RANGE:
                vbox = QVBoxLayout()
                vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
                min = QSpinBox()
                min.setRange(0, 9)
                min.setValue(0)
                max = QSpinBox()
                max.setRange(0, 9)
                max.setValue(9)

                vbox.addWidget(QLabel(f"{field.metadata.get("label")} min:"))
                vbox.addWidget(min)
                vbox.addWidget(QLabel(f"{field.metadata.get("label")} max:"))
                vbox.addWidget(max)

                layout.addLayout(vbox)
                self.filters[fname] = (min, max)

        # --- Display options ---
        self.display_column = QVBoxLayout()
        self.display_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.display_column.addWidget(QLabel("Affichage"))
        self.display_checkboxes: dict[str, QCheckBox] = {}
        for fname, field in model.__dataclass_fields__.items():
            if field.metadata.get("visibility") == VisibilityOption.HIDDABLE or field.metadata.get("visibility") == VisibilityOption.HIDDABLE_WITH_FILTER:
                checkbox = QCheckBox(field.metadata.get("label"))
                checkbox.setChecked(True)
                self.display_column.addWidget(checkbox)
                self.display_checkboxes[fname] = checkbox

        # Filter button
        self.filter_button = QPushButton("Filtrer")
        self.filter_button.clicked.connect(apply_filters)
        self.display_column.addWidget(self.filter_button)
        layout.addLayout(self.display_column)

        self.display_column.setSpacing(0)
        self.display_column.setContentsMargins(0, 0, 0, 0)

        checkboxes_count = len(self.display_checkboxes.keys())
        checkbox_height = checkbox.sizeHint().height()
        for k, filter in self.filters.items():
            if type(filter) == MultiSelectionListWidget:
                filter.list.setMaximumHeight(
                    checkboxes_count * checkbox_height
                    + self.filter_button.sizeHint().height()
                )
                filter.list.setMaximumWidth(200)

        save_filters_btn = QPushButton("Enregistrer le filtre")
        layout.addWidget(save_filters_btn)
        save_filters_btn.clicked.connect(self.save_filters)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

    def checkbox_event_factory(self, cols, func):
        return lambda state: [
            func(col, state == Qt.CheckState.Unchecked) for col in cols
        ]

    def save_filters(self):
        filters = {}
        for fname, filter in self.filters.items():
            if type(filter) == MultiSelectionListWidget:
                filters[fname] = filter.get_selected_item_texts()
            if type(filter) == tuple:
                filters[fname] = [filter[0].value(), filter[1].value()]

        for fname, checkbox in self.display_checkboxes.items():
            filters[f"{fname}_checkbox"] = checkbox.isChecked()

        with open(
            f"{os.getcwd().replace("\\", "/")}/data/{self.model.__name__}_settings.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(filters, f)

    def load_filter_options(self, options: dict[str, list[str]]):
        for fname, filter in self.filters.items():
            if type(filter) == MultiSelectionListWidget:
                filter.clear()
                for element in options[fname]:
                    item = QListWidgetItem(element)
                    filter.addItem(item)
                    item.setSelected(True)
                filter.adjustSize()

    def get_filters(self) -> dict[str, list[str] | tuple[int, int]]:
        filters: dict[str, list[str] | tuple[int, int]] = {}
        for fname, filter in self.filters.items():
            if type(filter) == MultiSelectionListWidget:
                filters[fname] = filter.get_selected_item_texts()
            else:
                filters[fname] = (filter[0].value(), filter[1].value())
        return filters

    def load_filters(self, path):
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            filters: dict[str, list[str] | list[int] | bool] = json.load(f)

        for fname, values in filters.items():
            if not "_checkbox" in fname:
                filt = self.filters[fname]
                if type(filt) == MultiSelectionListWidget:
                    self.filters[fname].checkItems(values)
                elif type(filt) == tuple:
                    self.filters[fname][0].setValue(values[0])
                    self.filters[fname][1].setValue(values[1])
            elif "_checkbox" in fname:
                key = fname.replace("_checkbox", "")
                self.display_checkboxes[key].setChecked(values)