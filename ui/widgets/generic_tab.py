from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from model.generic_model import ExplorableModel, FilterOption, VisibilityOption
from typing import TypeVar, Generic, Type

from ui.widgets.genericTab.genericDDList import SavebleDDList
from utils.paths import get_export_dir
from export.html_export import html_export

from ui.widgets.genericTab.table_section import GenericTable
from ui.widgets.genericTab.filters_section import GenericFilter
from ui.widgets.genericTab.export_section import GenericExport
import os

T = TypeVar("T", bound=ExplorableModel)


class GenericTab(Generic[T], QWidget):
    """A generic tab class that presents a model with a list, filters and export section."""

    def __init__(self, model: Type[T]):
        self.model = model
        self.items = model.get_collection()

        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self) -> QVBoxLayout:
        """Create the layout for the tab."""
        layout = QVBoxLayout()

        self.table_widget = GenericTable(
            self.model,
        )
        self.filters_widget = GenericFilter(self.model, self.apply_filters)
        self.export_widget = GenericExport(self.model)

        def display_checkbox_factory(cols, visibility, fname):
            if visibility == VisibilityOption.HIDDABLE:
                return lambda state: [
                    self.table_widget.toggle_column_display(
                        col, state == Qt.CheckState.Unchecked
                    )
                    for col in cols
                ]
            if visibility == VisibilityOption.HIDDABLE_WITH_FILTER:
                return lambda state: [
                    self.table_widget.toggle_column_display(
                        col, state == Qt.CheckState.Unchecked
                    )
                    for col in cols
                ] + [
                    self.table_widget.line_filters[fname].setHidden(
                        state == Qt.CheckState.Unchecked
                    ),
                    self.table_widget.line_filters[fname].clear(),
                ]

        for fname, field in self.model.__dataclass_fields__.items():
            if (
                field.metadata.get("visibility") == VisibilityOption.HIDDABLE
                or field.metadata.get("visibility")
                == VisibilityOption.HIDDABLE_WITH_FILTER
            ):
                self.filters_widget.display_checkboxes[fname].checkStateChanged.connect(
                    display_checkbox_factory(
                        field.metadata.get("cols_to_hide"),
                        field.metadata.get("visibility"),
                        fname,
                    )
                )

        self.export_widget.select_everything_checkbox.checkStateChanged.connect(
            self.table_widget.toggle_select_all
        )
        self.export_widget.export_html_btn.clicked.connect(self.export_selected_html)
        self.table_widget.table.itemChanged.connect(self.update_selected_count)

        layout.addWidget(self.filters_widget)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.export_widget)
        self.load_data()
        return layout

    def load_data(self):
        data = self.items().get_items()

        options = {}
        for fname, field in self.model.__dataclass_fields__.items():
            if field.metadata.get("filter_type") == FilterOption.LIST:
                if field.type == list[str]:
                    options[fname] = sorted(
                        set(
                            item
                            for object in data
                            for item in object.__getattribute__(fname)
                        )
                    )
                else:
                    options[fname] = sorted(
                        set(item.__getattribute__(fname) for item in data)
                    )

        self.filters_widget.load_filter_options(options)
        self.apply_filters()
        self.filters_widget.load_filters(
            f"{os.getcwd().replace("\\", "/")}/data/{self.model.__name__}_settings.json"
        )
        self.apply_filters()

    def apply_filters(self):
        filters = self.filters_widget.get_filters()
        self.table_widget.apply_filters(filters)

        headers = ["✔"] + [
            item.metadata.get("label")
            for key, item in self.model.__dataclass_fields__.items()
            if item.metadata.get("visibility") != VisibilityOption.ALWAYS_HIDDEN
        ]
        cols = ["checkbox"] + [
            key
            for key, item in self.model.__dataclass_fields__.items()
            if item.metadata.get("visibility") != VisibilityOption.ALWAYS_HIDDEN
        ]
        self.table_widget.update_display(headers, cols)

    def export_selected_html(self):
        selected_items = self.table_widget.get_selected_items()
        if not selected_items:
            QMessageBox.warning(
                self,
                f"Aucun {self.model.__name__} sélectionné",
                f"Veuillez sélectionner au moins un.e {self.model.__name__} à exporter",
            )
            return
        self.export_html(selected_items)

    def export_html(self, items):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer HTML",
            str(get_export_dir()),
            "Fichier HTML (*.html)",
        )
        if not path:
            return  # L'utilisateur a annulé

        mode, show_VO_name, show_source = self.export_widget.get_export_options()

        if items and path:
            html_export(
                items,
                path,
                mode,
                show_VO_name=show_VO_name,
                show_source=show_source,
                data_type=self.model,
            )
            QMessageBox.information(
                self,
                "Exportation réussie",
                f"{len(items)} {self.model.__name__} ont été exportés avec succès en HTML.",
            )

    def update_selected_count(self, item):
        if item.column() != 0:
            return

        seleted_count, all = self.table_widget.get_selected_count(item)
        self.export_widget.change_selected_count_label(seleted_count, all)

    def reload_data(self):
        self.load_data()


class GenericTabWithList(GenericTab):
    def __init__(self, model: Type[T], shared_dict):
        self._shared_dict = shared_dict
        super().__init__(model)

    def create_layout(self):
        layout = QHBoxLayout()
        left_layout = super().create_layout()
        layout.addLayout(left_layout)

        ##### Right part #####
        self.list_widget = SavebleDDList(self.model, self._shared_dict)
        self.list_widget.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.list_widget)
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
