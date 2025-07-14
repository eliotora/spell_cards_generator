from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QRadioButton, QLabel, QButtonGroup, QPushButton
from PyQt6.QtCore import Qt
from export.html_export import RULES, CARDS

class ManeuverExport(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Export options ---
        export_options_layout = QHBoxLayout()
        select_data_layout = QHBoxLayout()
        select_data_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.select_everything_checkbox = QCheckBox("Tout sélectionner")
        self.select_everything_checkbox.setChecked(False)
        self.print_vo_name_checkbox = QCheckBox("Imprimer le nom en VO")
        self.print_source_checkbox = QCheckBox("Imprimer la source")
        select_data_layout.addWidget(self.select_everything_checkbox)
        select_data_layout.addWidget(self.print_vo_name_checkbox)
        select_data_layout.addWidget(self.print_source_checkbox)

        # --- Export mode ---
        export_mode_layout = QHBoxLayout()
        export_mode_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.export_mode_label = QLabel("Format:")
        self.radio_rules = QRadioButton("Règles")
        self.radio_cards = QRadioButton("Cartes")
        self.radio_rules.setChecked(True)

        self.format_group = QButtonGroup()
        self.format_group.addButton(self.radio_rules, id=RULES)
        self.format_group.addButton(self.radio_cards, id=CARDS)
        export_mode_layout.addWidget(self.export_mode_label)
        export_mode_layout.addWidget(self.radio_rules)
        export_mode_layout.addWidget(self.radio_cards)

        export_options_layout.addLayout(select_data_layout)
        export_options_layout.addLayout(export_mode_layout)

        layout.addLayout(export_options_layout)

        # Adding export buttons
        export_buttons_layout = QHBoxLayout()
        self.selected_maneuver_count_label = QLabel("Manœuvres sélectionnées: 0")

        # Export buttons
        self.export_pdf_btn = QPushButton("Exporter en PDF")
        # export_pdf_btn.clicked.connect(self.export_pdf)
        self.export_pdf_btn.setDisabled(True)

        self.export_html_btn = QPushButton("Exporter en HTML")

        export_buttons_layout.addWidget(self.selected_maneuver_count_label)
        export_buttons_layout.addWidget(self.export_pdf_btn)
        export_buttons_layout.addWidget(self.export_html_btn)

        layout.addLayout(export_buttons_layout)

    def change_selected_maneuver_count_label(self, nbr:int, checked:bool):
        self.selected_maneuver_count_label.setText(f"Manœuvres sélectionnées: {nbr}")
        self.select_everything_checkbox.blockSignals(True)
        self.select_everything_checkbox.setChecked(checked)
        self.select_everything_checkbox.blockSignals(False)

    def get_export_mode(self) -> int:
        """
        Returns the selected export mode.
        :return: RULES or CARDS
        """
        return self.format_group.checkedId()

    def get_export_options(self) -> tuple[int, bool, bool]:
        """
        Returns the export options.
        :return: tuple of (export mode, print VO name, print source)
        """
        return (
            self.get_export_mode(),
            self.print_vo_name_checkbox.isChecked(),
            self.print_source_checkbox.isChecked()
        )
