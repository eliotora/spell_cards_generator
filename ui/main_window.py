from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QLabel,
    QSpinBox,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from export.pdf_export import exporter_pdf
from export.html_export import exporter_html
from spell_loader import load_spells_from_folder
from ui.spell_detail_window import SpellDetailWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Sorts")
        self.resize(1000, 600)

        # Crée le widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # ==== Barre de filtre ====
        filter_layout = QHBoxLayout()

        # ---- Class Filter ----
        self.class_box = QVBoxLayout()
        self.top_class_box = QHBoxLayout()

        ## Checkbox to toggle class selection
        self.toggle_class_selection_box = QCheckBox()
        self.toggle_class_selection_box.setChecked(True)
        self.toggle_class_selection_box.checkStateChanged.connect(
            self.toggle_class_selection
        )
        self.top_class_box.addWidget(self.toggle_class_selection_box)

        ## Label
        self.top_class_box.addWidget(QLabel("Classes:"))
        self.class_box.addLayout(self.top_class_box)

        ## List of class
        self.class_list = QListWidget()
        self.class_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.class_list.clicked.connect(self.update_class_checkbox_state)
        self.class_box.addWidget(self.class_list)
        filter_layout.addLayout(self.class_box)

        # ---- Source Filter ----
        self.source_box = QVBoxLayout()
        self.top_source_box = QHBoxLayout()

        ## Checkbox to toggle source selection
        self.toggle_source_selection_box = QCheckBox()
        self.toggle_source_selection_box.setChecked(True)
        self.toggle_source_selection_box.checkStateChanged.connect(
            self.toggle_source_selection
        )
        self.top_source_box.addWidget(self.toggle_source_selection_box)

        ## Label
        self.top_source_box.addWidget(QLabel("Sources:"))
        self.source_box.addLayout(self.top_source_box)

        ## List of sources
        self.source_list = QListWidget()
        self.source_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.source_list.clicked.connect(self.update_source_checkbox_state)
        self.source_box.addWidget(self.source_list)
        filter_layout.addLayout(self.source_box)

        # ---- School Filter ----
        self.school_box = QVBoxLayout()
        self.top_box = QHBoxLayout()

        ## Checkbox to toggle school selection
        self.toggle_school_selection_box = QCheckBox()
        self.toggle_school_selection_box.setChecked(True)
        self.toggle_school_selection_box.checkStateChanged.connect(
            self.toggle_school_selection
        )
        self.top_box.addWidget(self.toggle_school_selection_box)

        ## Label
        self.top_box.addWidget(QLabel("Écoles:"))
        self.school_box.addLayout(self.top_box)

        ## List of schools
        self.school_list = QListWidget()
        self.school_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.school_list.clicked.connect(self.update_school_checkbox_state)
        self.school_box.addWidget(self.school_list)

        filter_layout.addLayout(self.school_box)

        # Niveau min/max
        self.minlevel = QSpinBox()
        self.minlevel.setRange(0, 9)
        self.minlevel.setValue(0)
        self.maxlevel = QSpinBox()
        self.maxlevel.setRange(0, 9)
        self.maxlevel.setValue(9)

        filter_layout.addWidget(QLabel("Niveau min:"))
        filter_layout.addWidget(self.minlevel)
        filter_layout.addWidget(QLabel("Niveau max:"))
        filter_layout.addWidget(self.maxlevel)

        # Bouton de filtrage
        self.filter_button = QPushButton("Filtrer")
        self.filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.filter_button)

        self.layout.addLayout(filter_layout)
        # ---- Fin de la barre de filtre ----

        # Table des sorts
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.load_spells()

        # Boutons d'export
        export_pdf_btn = QPushButton("Exporter en PDF")
        export_pdf_btn.clicked.connect(self.export_pdf)

        export_html_btn = QPushButton("Exporter en HTML")
        export_html_btn.clicked.connect(self.export_html)

        self.layout.addWidget(export_pdf_btn)
        self.layout.addWidget(export_html_btn)

    def load_spells(self):
        self.spells = load_spells_from_folder("data")
        headers = [
            "Sort",
            "Niv",
            "École",
            "Incantation",
            "Portée",
            "Composantes",
            "Concentration",
            "Rituel",
        ]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.spells))

        for row, spell in enumerate(self.spells):
            for col, key in enumerate(
                [
                    "nom",
                    "niveau",
                    "école",
                    "temps_d'incantation",
                    "portée",
                    "composantes",
                    "concentration",
                    "rituel",
                ]
            ):
                value = spell.get(key, "")
                if isinstance(value, list):
                    value = ", ".join(value)
                elif isinstance(value, bool):
                    value = "Oui" if value else "Non"
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.table.cellDoubleClicked.connect(self.show_spell_details)

        # Filling the list of schools
        self.school_list.clear()
        self.schools = sorted(set(spell.get("école", "") for spell in self.spells))
        for school in self.schools:
            item = QListWidgetItem(school)
            self.school_list.addItem(item)
            item.setSelected(True)

        # Filling the list of sources
        self.source_list.clear()
        self.sources = sorted(set(spell.get("source", "") for spell in self.spells))
        for source in self.sources:
            item = QListWidgetItem(source)
            self.source_list.addItem(item)
            item.setSelected(True)

        # Filling the list of classes
        self.class_list.clear()
        self.classes = sorted({cls for spell in self.spells for cls in spell.get("classes", [])})
        for class_name in self.classes:
            item = QListWidgetItem(class_name)
            self.class_list.addItem(item)
            item.setSelected(True)

        self.apply_filters()

    def apply_filters(self):
        # Filters
        selected_classes = [item.text() for item in self.class_list.selectedItems()]
        selected_sources = [item.text() for item in self.source_list.selectedItems()]
        selected_schools = [item.text() for item in self.school_list.selectedItems()]
        min_level = self.minlevel.value()
        max_level = self.maxlevel.value()

        # Filtering
        self.filtered_spells = [
            spell
            for spell in self.spells
            if (
                any(cls in selected_classes for cls in spell.get("classes", []))
                 and
                spell.get("source") in selected_sources
                 and
                spell.get("école") in selected_schools
                 and
                min_level <= spell.get("niveau", 0) <= max_level
            )
        ]

        # Update table
        self.table.setRowCount(len(self.filtered_spells))
        for row, spell in enumerate(self.filtered_spells):
            for col, key in enumerate(
                [
                    "nom",
                    "niveau",
                    "école",
                    "temps_d'incantation",
                    "portée",
                    "composantes",
                    "concentration",
                    "rituel",
                ]
            ):
                value = spell.get(key, "")
                if isinstance(value, list):
                    value = ", ".join(value)
                elif isinstance(value, bool):
                    value = "Oui" if value else "Non"
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def show_spell_details(self, row, column):
        spell = self.filtered_spells[row]
        self.details_window = SpellDetailWindow(spell)
        self.details_window.show()

    def toggle_school_selection(self, state):
        checked = state == Qt.CheckState.Checked

        for i in range(self.school_list.count()):
            self.school_list.item(i).setSelected(checked)

    def toggle_source_selection(self, state):
        checked = state == Qt.CheckState.Checked

        for i in range(self.source_list.count()):
            self.source_list.item(i).setSelected(checked)

    def toggle_class_selection(self, state):
        checked = state == Qt.CheckState.Checked

        for i in range(self.class_list.count()):
            self.class_list.item(i).setSelected(checked)

    def update_school_checkbox_state(self):
        total = self.school_list.count()
        selected = sum(item.isSelected() for item in self.school_list.selectedItems())

        all_selected = selected == total

        self.toggle_school_selection_box.blockSignals(True)
        self.toggle_school_selection_box.setChecked(all_selected)
        self.toggle_school_selection_box.blockSignals(False)

    def update_source_checkbox_state(self):
        total = self.source_list.count()
        selected = sum(item.isSelected() for item in self.source_list.selectedItems())

        all_selected = selected == total

        self.toggle_source_selection_box.blockSignals(True)
        self.toggle_source_selection_box.setChecked(all_selected)
        self.toggle_source_selection_box.blockSignals(False)

    def update_class_checkbox_state(self):
        total = self.class_list.count()
        selected = sum(item.isSelected() for item in self.class_list.selectedItems())

        all_selected = selected == total

        self.toggle_class_selection_box.blockSignals(True)
        self.toggle_class_selection_box.setChecked(all_selected)
        self.toggle_class_selection_box.blockSignals(False)

    def export_pdf(self):
        if self.data:
            exporter_pdf(self.data, "export.pdf")

    def export_html(self):
        if self.data:
            exporter_html(self.data, "export.html")
