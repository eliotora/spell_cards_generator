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
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QFileDialog,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
# from export.pdf_export import exporter_pdf
from export.html_export import html_export
from model.spell_model import SpellModels
from profile_loader import load_profiles_from_folder
from ui.spell_detail_window import SpellDetailWindow
import os
from pathlib import Path
from ui.widgets.SpellList import SpellList, SpellTable
import json


class MainWindow(QMainWindow):
    details_windows = {}
    default_export_dir = os.path.join(os.getcwd(), "output")

    def __init__(self):
        super().__init__()
        self.spell_models = SpellModels()
        self.setWindowTitle("Liste des Sorts")

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        ##### Left part #####
        self.left_col = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_col.setLayout(self.left_layout)
        self.layout.addWidget(self.left_col)

        # ==== Filter row ====
        filter_layout = QHBoxLayout()
        filter_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # ---- Class Filter ----
        self.class_box = QVBoxLayout()

        ## Checkbox to toggle class selection
        self.toggle_class_selection_box = QCheckBox()
        self.toggle_class_selection_box.setText("Classes:")
        self.toggle_class_selection_box.setChecked(True)
        self.toggle_class_selection_box.checkStateChanged.connect(
            self.toggle_class_selection
        )
        self.class_box.addWidget(self.toggle_class_selection_box)

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

        ## Checkbox to toggle source selection
        self.toggle_source_selection_box = QCheckBox()
        self.toggle_source_selection_box.setText("Sources:")
        self.toggle_source_selection_box.setChecked(True)
        self.toggle_source_selection_box.checkStateChanged.connect(
            self.toggle_source_selection
        )
        self.source_box.addWidget(self.toggle_source_selection_box)

        # ---- School Filter ----
        self.school_box = QVBoxLayout()

        ## Checkbox to toggle school selection
        self.toggle_school_selection_box = QCheckBox()
        self.toggle_school_selection_box.setText("Écoles:")
        self.toggle_school_selection_box.setChecked(True)
        self.toggle_school_selection_box.checkStateChanged.connect(
            self.toggle_school_selection
        )
        self.school_box.addWidget(self.toggle_school_selection_box)


        ## List of schools
        self.school_list = QListWidget()
        self.school_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.school_list.clicked.connect(self.update_school_checkbox_state)
        self.school_box.addWidget(self.school_list)

        filter_layout.addLayout(self.school_box)

        ## Level Filter
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

        filter_layout.addLayout(self.spell_level_box)

        ## List of sources
        self.source_list = QListWidget()
        self.source_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.source_list.clicked.connect(self.update_source_checkbox_state)
        self.source_box.addWidget(self.source_list)
        filter_layout.addLayout(self.source_box)

        # ---- Display and filter button column ----
        # Display column
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
        self.vf_name_checkbox.checkStateChanged.connect(self.apply_filters)
        self.vo_name_checkbox.checkStateChanged.connect(self.apply_filters)
        self.school_checkbox.checkStateChanged.connect(self.apply_filters)
        self.info_checkbox.checkStateChanged.connect(self.apply_filters)
        self.concentration_checkbox.checkStateChanged.connect(self.apply_filters)
        self.ritual_checkbox.checkStateChanged.connect(self.apply_filters)
        self.description_checkbox.checkStateChanged.connect(self.description_checkbox_event)
        self.source_checkbox.checkStateChanged.connect(self.apply_filters)

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
        self.filter_button.clicked.connect(self.apply_filters)
        self.display_column.addWidget(self.filter_button)
        filter_layout.addLayout(self.display_column)

        self.display_column.setSpacing(0)
        self.display_column.setContentsMargins(0,0,0,0)

        checkboxes_count = 8
        checkbox_height = self.vf_name_checkbox.sizeHint().height()
        self.class_list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())
        self.school_list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())
        self.source_list.setMaximumHeight(checkboxes_count * checkbox_height + self.filter_button.sizeHint().height())

        self.class_list.setMaximumWidth(200)
        self.school_list.setMaximumWidth(200)
        self.source_list.setMaximumWidth(200)

        # Ajoute ce spacer à la fin du layout pour éviter que les éléments s'étendent :
        filter_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.left_layout.addLayout(filter_layout)

        # ---- End of filters section ----
        # ---- Live filtering ----
        filter_layout2 = QHBoxLayout()
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("sort")
        self.name_filter.textChanged.connect(self.live_filter)
        self.name_filter.setClearButtonEnabled(True)
        self.name_filter.setAcceptDrops(False)
        filter_layout2.addWidget(self.name_filter)

        self.description_filter = QLineEdit()
        self.description_filter.setPlaceholderText("description")
        self.description_filter.textChanged.connect(self.live_filter)
        self.description_filter.setClearButtonEnabled(True)
        self.description_filter.setAcceptDrops(False)
        self.description_filter.setVisible(False)  # Initially hidden
        filter_layout2.addWidget(self.description_filter)

        self.left_layout.addLayout(filter_layout2)

        # Table des sorts
        self.table = SpellTable()
        self.table.verticalHeader().setVisible(False)
        self.table.setDragEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.table.setSortingEnabled(True)
        self.left_layout.addWidget(self.table)

        self.load_spells()
        self.load_profiles()

        # ==== Export section ====
        export_options_layout = QHBoxLayout()
        select_data_layout = QHBoxLayout()
        select_data_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.select_everything_checkbox = QCheckBox("Tout sélectionner")
        self.select_everything_checkbox.setChecked(False)
        self.select_everything_checkbox.checkStateChanged.connect(
            lambda state: [
                self.table.item(row, 0).setCheckState(Qt.CheckState.Checked if state == Qt.CheckState.Checked else Qt.CheckState.Unchecked)
                for row in range(self.table.rowCount())
            ]
        )
        self.print_vo_name_checkbox = QCheckBox("Imprimer le nom en VO")
        self.print_source_checkbox = QCheckBox("Imprimer la source")
        select_data_layout.addWidget(self.select_everything_checkbox)
        select_data_layout.addWidget(self.print_vo_name_checkbox)
        select_data_layout.addWidget(self.print_source_checkbox)

        export_mode_layout = QHBoxLayout()
        export_mode_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.export_mode_label = QLabel("Format:")
        self.radio_rules = QRadioButton("Règles")
        self.radio_grimoire = QRadioButton("Grimoire")
        self.radio_cards = QRadioButton("Cartes")
        self.radio_rules.setChecked(True)

        self.format_group = QButtonGroup()
        self.format_group.addButton(self.radio_rules, id=0)
        self.format_group.addButton(self.radio_grimoire, id=1)
        self.format_group.addButton(self.radio_cards, id=2)
        export_mode_layout.addWidget(self.export_mode_label)
        export_mode_layout.addWidget(self.radio_rules)
        export_mode_layout.addWidget(self.radio_grimoire)
        export_mode_layout.addWidget(self.radio_cards)

        export_options_layout.addLayout(select_data_layout)
        export_options_layout.addLayout(export_mode_layout)
        self.table.itemChanged.connect(self.update_selected_spell_count)

        self.left_layout.addLayout(export_options_layout)

        # Adding export buttons
        export_buttons_layout = QHBoxLayout()
        self.selected_spell_count_label = QLabel("Sorts sélectionnés: 0")

        # Boutons d'export
        export_pdf_btn = QPushButton("Exporter en PDF")
        # export_pdf_btn.clicked.connect(self.export_pdf)
        export_pdf_btn.setDisabled(True)

        export_html_btn = QPushButton("Exporter en HTML")
        export_html_btn.clicked.connect(self.export_selected_html)

        export_buttons_layout.addWidget(self.selected_spell_count_label)
        export_buttons_layout.addWidget(export_pdf_btn)
        export_buttons_layout.addWidget(export_html_btn)
        self.left_layout.addLayout(export_buttons_layout)

        ##### Right part #####
        self.right_col_widget = QWidget()
        self.right_col_layout = QVBoxLayout()
        self.right_col_layout.setSpacing(4)
        self.right_col_layout.setContentsMargins(0,0,0,0)
        self.right_col_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_col_widget.setLayout(self.right_col_layout)
        self.layout.addWidget(self.right_col_widget)

        self.right_col_label = QLabel("Liste de sort")
        self.right_col_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_col_layout.addWidget(self.right_col_label)

        self.spell_lst_name_box = QWidget()
        self.spell_lst_name_layout = QHBoxLayout()
        self.spell_lst_name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spell_lst_name_box.setLayout(self.spell_lst_name_layout)
        self.spell_lst_name_layout.setSpacing(4)
        self.spell_lst_name_layout.setContentsMargins(0,0,0,0)
        self.spell_list_name_label = QLabel("Nom:")
        self.spell_list_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spell_list_name_field = QLineEdit()
        self.spell_list_name_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.spell_list_name_field.setAcceptDrops(False)
        self.spell_list_name_field.setPlaceholderText("nouveau")
        self.spell_lst_name_layout.addWidget(self.spell_list_name_label)
        self.spell_lst_name_layout.addWidget(self.spell_list_name_field)
        self.right_col_layout.addWidget(self.spell_lst_name_box)

        self.spell_lists_widget = QWidget()
        self.right_col_layout.addWidget(self.spell_lists_widget)
        self.spell_lists_widget_layout = QHBoxLayout()
        self.spell_lists_widget_layout.setSpacing(4)
        self.spell_lists_widget_layout.setContentsMargins(0,0,0,0)
        self.spell_lists_widget_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spell_lists_widget.setLayout(self.spell_lists_widget_layout)


        self.level_0_to_4_widget = QWidget()
        self.spell_lists_widget_layout.addWidget(self.level_0_to_4_widget)
        self.level_0_to_4_widget_layout = QVBoxLayout()
        self.level_0_to_4_widget_layout.setSpacing(4)
        self.level_0_to_4_widget_layout.setContentsMargins(0,0,0,0)
        self.level_0_to_4_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.level_0_to_4_widget.setLayout(self.level_0_to_4_widget_layout)
        self.level_5_to_9_widget = QWidget()
        self.spell_lists_widget_layout.addWidget(self.level_5_to_9_widget)
        self.level_5_to_9_widget_layout = QVBoxLayout()
        self.level_5_to_9_widget_layout.setSpacing(4)
        self.level_5_to_9_widget_layout.setContentsMargins(0,0,0,0)
        self.level_5_to_9_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.level_5_to_9_widget.setLayout(self.level_5_to_9_widget_layout)

        self.spell_lists: dict[int, tuple[SpellList, QPushButton]] = {}
        for level in range(10):
            spell_list_level_label = QLabel(f"Niveau {level}" if level > 0 else "Tours de magie")
            spell_list = SpellList(level)
            spell_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            spell_list.itemDoubleClicked.connect(self.spell_list_double_click)

            lock_button = QPushButton()
            lock_button.setIcon(QIcon("images/unlock-48.png"))
            lock_button.setCheckable(True)
            lock_button.setToolTip("Verrouiller / Déverrouiller le drag & drop")
            lock_button.clicked.connect(self.toggle_lock_factory(lock_button, spell_list))
            self.spell_lists[level] = (spell_list, lock_button)

            label_widget = QWidget()
            label_widget_layout = QHBoxLayout()
            label_widget_layout.setSpacing(4)
            label_widget_layout.setContentsMargins(0,0,0,0)
            label_widget_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            label_widget.setLayout(label_widget_layout)
            label_widget_layout.addWidget(spell_list_level_label)
            label_widget_layout.addWidget(lock_button)
            if level < 5:
                self.level_0_to_4_widget_layout.addWidget(label_widget)
                self.level_0_to_4_widget_layout.addWidget(spell_list)
            else:
                self.level_5_to_9_widget_layout.addWidget(label_widget)
                self.level_5_to_9_widget_layout.addWidget(spell_list)
            spell_list.adjustSizeToContents()
        self.right_col_layout.addSpacerItem(QSpacerItem(0,0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.spl_lst_html_btn = QPushButton()
        self.spl_lst_html_btn.setText("Exporter la liste en HTML")
        self.spl_lst_html_btn.clicked.connect(self.export_spell_list_html)
        self.right_col_layout.addWidget(self.spl_lst_html_btn)
        self.save_btn = QPushButton()
        self.save_btn.setText("Sauver")
        self.save_btn.clicked.connect(self.save_spell_list)
        self.load_btn = QPushButton()
        self.load_btn.setText("Charger")
        self.load_btn.clicked.connect(self.load_spell_list)
        self.right_col_layout.addWidget(self.save_btn)
        self.right_col_layout.addWidget(self.load_btn)

        self.right_col_widget.hide()

        spell_list_hide_btn = QPushButton()
        spell_list_hide_btn.clicked.connect(
            lambda : self.right_col_widget.setHidden(
                bool(spell_list_hide_btn.setText("<" if self.right_col_widget.isHidden() else ">") or
                not (self.right_col_widget.isHidden())
                )
                )
            )
        spell_list_hide_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding)
        spell_list_hide_btn.setFixedWidth(20)
        spell_list_hide_btn.setText(">")

        self.layout.addWidget(spell_list_hide_btn)

        self.showMaximized()


    def load_profiles(self):
        self.profiles = load_profiles_from_folder("data")

    def get_profile(self, profile_name):
        for p in self.profiles:
            if p["nom"] == profile_name:
                return p
        return None

    def load_spells(self):
        spells = self.spell_models.get_spells()
        self.table.cellDoubleClicked.connect(self.table_spell_double_click)

        # Filling the list of schools
        self.school_list.clear()
        self.schools = sorted(set(spell.get("école", "") for spell in spells))
        for school in self.schools:
            item = QListWidgetItem(school)
            self.school_list.addItem(item)
            item.setSelected(True)
        self.school_list.adjustSize()

        # Filling the list of sources
        self.source_list.clear()
        self.sources = sorted(set(spell.get("source", "") for spell in spells))
        for source in self.sources:
            item = QListWidgetItem(source)
            self.source_list.addItem(item)
            item.setSelected(True)
        self.source_list.adjustSize()

        # Filling the list of classes
        self.class_list.clear()
        self.classes = sorted({cls for spell in spells for cls in spell.get("classes", [])})
        for class_name in self.classes:
            item = QListWidgetItem(class_name)
            self.class_list.addItem(item)
            item.setSelected(True)
        self.class_list.adjustSize()

        self.apply_filters()

    def apply_filters(self):
        spells = self.spell_models.get_spells()

        # Reset sorts
        self.table.setSortingEnabled(False)

        # Filters
        selected_classes = [item.text() for item in self.class_list.selectedItems()]
        selected_sources = [item.text() for item in self.source_list.selectedItems()]
        selected_schools = [item.text() for item in self.school_list.selectedItems()]
        min_level = self.minlevel.value()
        max_level = self.maxlevel.value()
        name_filter = self.name_filter.text().strip().lower()

        # Filtering
        self.filtered_spells = [
            spell
            for spell in spells
            if (
                any(cls in selected_classes for cls in spell.get("classes", []))
                 and
                spell.get("source") in selected_sources
                 and
                spell.get("école") in selected_schools
                 and
                min_level <= spell.get("niveau", 0) <= max_level
                 and
                (name_filter in spell.get("nom", "").lower() or (spell.get("nom_VF", "") is not None and name_filter in spell.get("nom_VF", "").lower()))
                 and
                (self.description_filter.text().strip().lower() in spell.get("description_short", "").lower() if self.description_checkbox.isChecked() else True)
            )
        ]

        headers = [
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
            "Source" if self.source_checkbox.isChecked() else None,
        ]
        headers = [header for header in headers if header is not None]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Update table
        cols = [
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
        cols = [col for col in cols if col is not None]
        self.table.setRowCount(len(self.filtered_spells))
        for row, spell in enumerate(self.filtered_spells):
            for col, key in enumerate(cols):
                if key == "checkbox":
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    item.setCheckState(Qt.CheckState.Unchecked)
                    self.table.setItem(row, col, item)
                    continue
                value = spell.get(key, "")
                if isinstance(value, list):
                    values = [v.split("(")[0].strip() for v in value if v]
                    if len(values) == 4:
                        print(value, values)
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

        # Apply filters to the spells
        for row in range(self.table.rowCount()):
            spell = self.filtered_spells[row]
            matches_name = name_filter in spell.get("nom", "").lower() or (spell.get("nom_VF", "") is not None and name_filter in spell.get("nom_VF", "").lower())
            matches_description = description_filter in spell.get("description_short", "").lower()

            # Check if the spell matches the filters
            if matches_name and (not self.description_checkbox.isChecked() or matches_description):
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def show_spell_details(self, spell):
        window = SpellDetailWindow(spell)
        self.details_windows[spell["nom"]] = window
        window.main_controler = self
        window.show()

    def table_spell_double_click(self, row, column):
        spell_name = self.table.item(row, 1).text()
        spell = self.spell_models.get_spell(spell_name)
        self.show_spell_details(spell)

    def spell_list_double_click(self, item):
        spell_name = item.text()
        self.show_spell_details(self.spell_models.get_spell(spell_name))

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

    def description_checkbox_event(self, state):
        if state == Qt.CheckState.Checked:
            self.description_filter.setVisible(True)
        else:
            self.description_filter.setVisible(False)
            self.description_filter.clear()
        self.apply_filters()

    def update_selected_spell_count(self, item):
        if item.column() != 0:
            return

        # Update the count of selected spells

        selected_count = 0
        for row in range(self.table.rowCount()):
            check_item = self.table.item(row, 0)
            if check_item and check_item.checkState() == Qt.CheckState.Checked:
                selected_count += 1

        self.selected_spell_count_label.setText(f"Sorts sélectionnés: {selected_count}")
        self.select_everything_checkbox.blockSignals(True)
        self.select_everything_checkbox.setChecked(selected_count == self.table.rowCount())
        self.select_everything_checkbox.blockSignals(False)

    def get_selected_spells(self):
        selected_spells = []
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.CheckState.Checked:
                selected_spells.append(self.filtered_spells[row])
        return selected_spells

    def toggle_lock_factory(self, btn:QPushButton, list: SpellList):
        def toggle_lock(locked):
            btn.setIcon(QIcon("images/lock-48.png" if locked else "images/unlock-48.png"))
            list.setAcceptDrops(not locked)
            list.setDragEnabled(not locked)
            list.adjustSizeToContents()

        return toggle_lock

    def load_spell_list(self):
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir une liste de sorts", str(self.get_export_dir()), "Fichier JSON (*.json)")
        if not path:
            return
        with open(path, 'r', encoding='utf-8') as f:
            spell_list = json.load(f)
        self.spell_list_name_field.setText(spell_list["nom"])

        for key, item in self.spell_lists.items():
            liste = item[0]
            liste.clear()
            btn:QPushButton = item[1]
            if not btn.isChecked():
                btn.click()

        for spell_name in spell_list["spells"]:
            spell = SpellModels().get_spell(spell_name)
            lvl = spell["niveau"]
            self.spell_lists[lvl][0].addItem(spell["nom"])

    def save_spell_list(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer la liste de sorts" , str(self.get_export_dir()), "Fichier JSON (*.json)")
        if not path:
            return
        spells = []
        for key, item in self.spell_lists.items():
            for i in range(item[0].count()):
                spell = item[0].item(i)
                spells.append(spell.text())

        if spells:
            spell_list = {
                "nom": self.spell_list_name_field.text(),
                "spells": spells
            }
            with open(path, "w", encoding='utf-8') as f:
                json.dump(spell_list, f)

    # def export_pdf(self):
    #     selected_spells = self.get_selected_spells()
    #     if not selected_spells:
    #         QMessageBox.warning(
    #             self, "Aucun sort sélectionné", "Veuillez sélectionner au moins un sort à exporter."
    #         )
    #         return

    #     print(f"Exporting {len(selected_spells)} spells to PDF...")
    #     path, _ = QFileDialog.getSaveFileName(self, "Enregistrer PDF", self.default_export_dir, "Fichier PDF (*.pdf)")
    #     if not path:
    #         return  # L'utilisateur a annulé

    #     if self.radio_rules.isChecked():
    #         mode= 'rules'
    #     elif self.radio_grimoire.isChecked():
    #         mode = 'grimoire'
    #     elif self.radio_cards.isChecked():
    #         mode = 'cards'

    #     show_VO_name = self.print_vo_name_checkbox.isChecked()
    #     show_source = self.print_source_checkbox.isChecked()

    #     if selected_spells and path:
    #         exporter_pdf(selected_spells, path, mode, show_source=show_source, show_VO_name=show_VO_name)
    #         QMessageBox.information(self, "Exportation réussie", f"{len(selected_spells)} sorts ont été exportés avec succès en PDF.")
    def get_export_dir(self):
        export_dir = Path(os.path.expandvars(r'%USERPROFILE%\Documents\DnD Spell Viewer Exports'))
        export_dir.mkdir(parents=True, exist_ok=True)
        return export_dir

    def export_html(self, spells):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer HTML", str(self.get_export_dir()), "Fichier HTML (*.html)")
        if not path:
            return  # L'utilisateur a annulé

        if self.radio_rules.isChecked():
            mode= 'rules'
        elif self.radio_grimoire.isChecked():
            mode = 'grimoire'
        elif self.radio_cards.isChecked():
            mode = 'cards'

        show_VO_name = self.print_vo_name_checkbox.isChecked()
        show_source = self.print_source_checkbox.isChecked()

        if spells and path:
            html_export(spells, path, mode, show_VO_name=show_VO_name, show_source=show_source)
            QMessageBox.information(self, "Exportation réussie", f"{len(spells)} sorts ont été exportés avec succès en HTML.")

    def export_selected_html(self):
        selected_spells = self.get_selected_spells()
        if not selected_spells:
            QMessageBox.warning(
                self, "Aucun sort sélectionné", "Veuillez sélectionner au moins un sort à exporter."
            )
            return

        self.export_html(selected_spells)

    def export_spell_list_html(self):
        spell_list = []
        for key, item in self.spell_lists.items():
            for i in range(item[0].count()):
                spell_list.append(SpellModels().get_spell(item[0].item(i).text()))

        if not spell_list:
            QMessageBox.warning(
                self, "Aucun sort dans la liste", "Veuillez ajouter au moins un sort dans la liste pour exporter."
            )
            return

        self.export_html(spell_list)

    def closeEvent(self, event):
        for k,w in self.details_windows.items():
            w.close()