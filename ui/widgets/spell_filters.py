from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSpinBox,
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

class SpellFilters(QWidget):
    def __init__(self, apply_filters, description_checkbox_event):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ---- Class Filter ----
        self.class_filter = MultiSelectionListWidget("Classes")
        layout.addWidget(self.class_filter)

        # ---- School Filter ----
        self.school_filter = MultiSelectionListWidget("School")
        layout.addWidget(self.school_filter)

        self.spell_level_box = QVBoxLayout()
        self.spell_level_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.minlevel = QSpinBox()
        self.minlevel.setRange(0, 9)
        self.minlevel.setValue(0)
        self.maxlevel = QSpinBox()
        self.maxlevel.setRange(0, 9)
        self.maxlevel.setValue(9)

        self.spell_level_box.addWidget(QLabel("Niveau min:"))
        self.spell_level_box.addWidget(self.minlevel)
        self.spell_level_box.addWidget(QLabel("Niveau max:"))
        self.spell_level_box.addWidget(self.maxlevel)

        layout.addLayout(self.spell_level_box)

        # ---- Source Filter ----
        self.source_filter = MultiSelectionListWidget("Sources")
        layout.addWidget(self.source_filter)

        self.display_column = QVBoxLayout()
        self.display_column.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.display_column.addWidget(QLabel("Affichage:"))
        self.vf_name_checkbox = QCheckBox("Nom VF")
        self.vo_name_checkbox = QCheckBox("Nom VO")
        self.school_checkbox = QCheckBox("École")
        self.info_checkbox = QCheckBox("Info")
        self.concentration_checkbox = QCheckBox("Concentration")
        self.ritual_checkbox = QCheckBox("Rituel")
        self.description_checkbox = QCheckBox("Description")
        self.source_checkbox = QCheckBox("Source")

        # Initial state of checkboxes
        self.school_checkbox.setChecked(True)
        self.info_checkbox.setChecked(True)
        self.concentration_checkbox.setChecked(True)
        self.ritual_checkbox.setChecked(True)

        # Signal connections for checkboxes
        self.vf_name_checkbox.checkStateChanged.connect(apply_filters)
        self.vo_name_checkbox.checkStateChanged.connect(apply_filters)
        self.school_checkbox.checkStateChanged.connect(apply_filters)
        self.info_checkbox.checkStateChanged.connect(apply_filters)
        self.concentration_checkbox.checkStateChanged.connect(apply_filters)
        self.ritual_checkbox.checkStateChanged.connect(apply_filters)
        self.description_checkbox.checkStateChanged.connect(
            description_checkbox_event
        )
        self.source_checkbox.checkStateChanged.connect(apply_filters)

        # Add checkboxes to the display column
        self.display_column.addWidget(self.vf_name_checkbox)
        self.display_column.addWidget(self.vo_name_checkbox)
        self.display_column.addWidget(self.school_checkbox)
        self.display_column.addWidget(self.info_checkbox)
        self.display_column.addWidget(self.concentration_checkbox)
        self.display_column.addWidget(self.ritual_checkbox)
        self.display_column.addWidget(self.description_checkbox)
        self.display_column.addWidget(self.source_checkbox)

        # Filter button
        self.filter_button = QPushButton("Filtrer")
        self.filter_button.clicked.connect(apply_filters)
        self.display_column.addWidget(self.filter_button)
        layout.addLayout(self.display_column)

        self.display_column.setSpacing(0)
        self.display_column.setContentsMargins(0, 0, 0, 0)

        checkboxes_count = 8
        checkbox_height = self.vf_name_checkbox.sizeHint().height()
        self.class_filter.list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())
        self.school_filter.list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())
        self.source_filter.list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())

        self.class_filter.list.setMaximumWidth(200)
        self.school_filter.list.setMaximumWidth(200)
        self.source_filter.list.setMaximumWidth(200)

        save_filters_btn = QPushButton("Sauver le filtre")
        layout.addWidget(save_filters_btn)
        save_filters_btn.clicked.connect(self.save_filters)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

    def save_filters(self):
        filters = {}
        filters["selected_classes"] = self.class_filter.get_selected_item_texts()

        filters["selected_sources"] = self.source_filter.get_selected_item_texts()
        filters["selected_schools"] = self.school_filter.get_selected_item_texts()
        filters["min_level"] = self.minlevel.value()
        filters["max_level"] = self.maxlevel.value()

        filters["vf_name"] = self.vf_name_checkbox.isChecked()
        filters["vo_name"] = self.vo_name_checkbox.isChecked()
        filters["school"] = self.school_checkbox.isChecked()
        filters["info"] = self.info_checkbox.isChecked()
        filters["concentration"] = self.concentration_checkbox.isChecked()
        filters["rituel"] = self.ritual_checkbox.isChecked()
        filters["description"] = self.description_checkbox.isChecked()
        filters["source"] = self.source_checkbox.isChecked()

        with open(
            f"{os.getcwd().replace("\\", "/")}/data/filter_settings.json",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(filters))

    def load_filter_options(self, schools, sources, classes):
        self.school_filter.clear()
        for school in schools:
            item = QListWidgetItem(school)
            self.school_filter.addItem(item)
            item.setSelected(True)
        self.school_filter.adjustSize()

        self.source_filter.clear()
        for source in sources:
            item = QListWidgetItem(source)
            self.source_filter.addItem(item)
            item.setSelected(True)
        self.source_filter.adjustSize()

        self.class_filter.clear()
        for classe in classes:
            item = QListWidgetItem(classe)
            self.class_filter.addItem(item)
            item.setSelected(True)
        self.class_filter.adjustSize()

    def get_filters(self):
        return self.class_filter.get_selected_item_texts(), self.source_filter.get_selected_item_texts(), self.school_filter.get_selected_item_texts(), self.minlevel.value(), self.maxlevel.value()

    def get_display_headers(self):
        return [
            "✔",
            "Sort",
            "VF" if self.vf_name_checkbox.isChecked() else None,
            "VO" if self.vo_name_checkbox.isChecked() else None,
            "Niv",
            "École" if self.school_checkbox.isChecked() else None,
            "Incantation" if self.info_checkbox.isChecked() else None,
            "Portée" if self.info_checkbox.isChecked() else None,
            "Composantes" if self.info_checkbox.isChecked() else None,
            "Concentration" if self.concentration_checkbox.isChecked() else None,
            "Rituel" if self.ritual_checkbox.isChecked() else None,
            "Description" if self.description_checkbox.isChecked() else None,
            "Source" if self.source_checkbox.isChecked() else None
        ]

    def get_display_options(self):
        return [
            "checkbox",
            "nom",
            "nom_VF" if self.vf_name_checkbox.isChecked() else None,
            "nom_VO" if self.vo_name_checkbox.isChecked() else None,
            "niveau",
            "école" if self.school_checkbox.isChecked() else None,
            "temps_d'incantation" if self.info_checkbox.isChecked() else None,
            "portée" if self.info_checkbox.isChecked() else None,
            "composantes" if self.info_checkbox.isChecked() else None,
            "concentration" if self.concentration_checkbox.isChecked() else None,
            "rituel" if self.ritual_checkbox.isChecked() else None,
            "description_short" if self.description_checkbox.isChecked() else None,
            "source" if self.source_checkbox.isChecked() else None,
        ]

    def load_filters(self):
        filter_data_path = f"{os.getcwd().replace("\\","/")}/data/filter_settings.json"
        if os.path.exists(filter_data_path):
            with open(filter_data_path, "r", encoding="utf-8") as f:
                filters = json.load(f)

                self.class_filter.checkItems(filters["selected_classes"])
                self.source_filter.checkItems(filters["selected_sources"])
                self.school_filter.checkItems(filters["selected_schools"])

                self.minlevel.setValue(filters["min_level"])
                self.maxlevel.setValue(filters["max_level"])

                for checkbox_name, checkbox in {
                    "vf_name": self.vf_name_checkbox,
                    "vo_name": self.vo_name_checkbox,
                    "school": self.school_checkbox,
                    "info": self.info_checkbox,
                    "concentration": self.concentration_checkbox,
                    "rituel": self.ritual_checkbox,
                    "description": self.description_checkbox,
                    "source": self.source_checkbox,
                }.items():
                    checkbox.setChecked(filters[checkbox_name])