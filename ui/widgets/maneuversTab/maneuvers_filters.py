from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QListWidgetItem
)
from PyQt6.QtCore import Qt
from ui.widgets.multi_selection_list import MultiSelectionListWidget
import os, json

class ManeuverFilters(QWidget):
    def __init__(self, apply_filters, description_checkbox_event, display_checkbox_event):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # --- Source filter ---
        self.source_filter = MultiSelectionListWidget("Sources")
        layout.addWidget(self.source_filter)

        # --- Display options ---
        self.display_column = QVBoxLayout()
        self.display_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.display_column.addWidget(QLabel("Affichage:"))
        self.vf_name_checkbox = QCheckBox("Nom VF")
        self.vo_name_checkbox = QCheckBox("Nom VO")
        self.description_checkbox = QCheckBox("Description")
        self.source_checkbox = QCheckBox("Source")

        # Initial state of checkboxes
        self.description_checkbox.setChecked(True)
        self.source_checkbox.setChecked(True)
        # Signal connections for checkboxes
        self.vf_name_checkbox.checkStateChanged.connect(
            lambda state: display_checkbox_event(2, state == Qt.CheckState.Unchecked)
        )
        self.vo_name_checkbox.checkStateChanged.connect(
            lambda state: display_checkbox_event(3, state == Qt.CheckState.Unchecked)
        )
        self.description_checkbox.checkStateChanged.connect(
            description_checkbox_event
        )
        self.source_checkbox.checkStateChanged.connect(
            lambda state: display_checkbox_event(5, state == Qt.CheckState.Unchecked)
        )
        # Add checkboxes to the display column
        self.display_column.addWidget(self.vf_name_checkbox)
        self.display_column.addWidget(self.vo_name_checkbox)
        self.display_column.addWidget(self.description_checkbox)
        self.display_column.addWidget(self.source_checkbox)
        layout.addLayout(self.display_column)

        # --- Apply filters button ---
        self.apply_filters_button = QPushButton("Filtrer")
        self.apply_filters_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.apply_filters_button.clicked.connect(apply_filters)
        layout.addWidget(self.apply_filters_button)

        self.display_column.setSpacing(0)
        self.display_column.setContentsMargins(0, 0, 0, 0)

        checkboxes_count = 4
        checkboxes_height = self.vf_name_checkbox.sizeHint().height() * checkboxes_count
        self.source_filter.setMaximumHeight(checkboxes_count * checkboxes_height + self.display_column.sizeHint().height())

        self.source_filter.list.setMaximumWidth(200)

        save_filter_btn = QPushButton("Sauver le filtre")
        save_filter_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(save_filter_btn)
        save_filter_btn.clicked.connect(self.save_filters)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

    def save_filters(self):
        filters = {}
        filters["sources"] = [item.text() for item in self.source_filter.list.selectedItems()]
        filters["vf_name"] = self.vf_name_checkbox.isChecked()
        filters["vo_name"] = self.vo_name_checkbox.isChecked()
        filters["description"] = self.description_checkbox.isChecked()
        filters["source"] = self.source_checkbox.isChecked()

        with open(
            f"{os.getcwd().replace(os.sep, '/')}/data/maneuver_filter_settings.json", "w", encoding="utf-8"
        ) as f:
            f.write(json.dumps(filters))

    def load_filter_options(self, sources):
        self.source_filter.clear()
        for source in sources:
            item = QListWidgetItem(source)
            self.source_filter.addItem(item)
            item.setSelected(True)
        self.source_filter.adjustSize()

    def get_filters(self):
        return self.source_filter.get_selected_item_texts()

    def load_filters(self):
        filter_data_path = f"{os.getcwd().replace(os.sep, '/')}/data/maneuver_filter_settings.json"
        if os.path.exists(filter_data_path):
            with open(filter_data_path, "r", encoding="utf-8") as f:
                filters = json.load(f)
                self.source_filter.checkItems(filters.get("sources", []))
                self.vf_name_checkbox.setChecked(filters.get("vf_name", True))
                self.vo_name_checkbox.setChecked(filters.get("vo_name", True))
                self.description_checkbox.setChecked(filters.get("description", True))
                self.source_checkbox.setChecked(filters.get("source", True))

    def fire_checked_signals(self):
        self.vf_name_checkbox.checkStateChanged.emit(self.vf_name_checkbox.checkState())
        self.vo_name_checkbox.checkStateChanged.emit(self.vo_name_checkbox.checkState())
        self.description_checkbox.checkStateChanged.emit(self.description_checkbox.checkState())
        self.source_checkbox.checkStateChanged.emit(self.source_checkbox.checkState())