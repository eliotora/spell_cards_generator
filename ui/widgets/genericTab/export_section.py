from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QRadioButton, QButtonGroup, QLabel, QPushButton
from PyQt6.QtCore import Qt
from model.generic_model import ExplorableModel
from typing import Type


class GenericExport(QWidget):
    def __init__(self, model: Type[ExplorableModel]):
        super().__init__()
        self.model = model
        model_collection =model.get_collection()

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
        export_mode_label = QLabel("Format:")
        export_mode_layout.addWidget(export_mode_label)
        self.format_group = QButtonGroup()
        self.export_mode_rbuttons = {}
        for export_mode in model_collection.export_options:
            rbutton = QRadioButton(export_mode.name)
            self.format_group.addButton(rbutton, id=export_mode)
            self.export_mode_rbuttons[export_mode] = rbutton
            export_mode_layout.addWidget(rbutton)

        self.format_group.buttons()[0].setChecked(True)

        export_options_layout.addLayout(select_data_layout)
        export_options_layout.addLayout(export_mode_layout)

        layout.addLayout(export_options_layout)

        # Adding export buttons
        export_buttons_layout = QHBoxLayout()
        self.selected_count_label = QLabel(f"{model.__name__} sélectionnés: 0")

        # Export buttons
        self.export_pdf_btn = QPushButton("Exporter en PDF")
        # self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.export_pdf_btn.setDisabled(True)

        self.export_html_btn = QPushButton("Exporter en HTML")

        export_buttons_layout.addWidget(self.selected_count_label)
        export_buttons_layout.addWidget(self.export_pdf_btn)
        export_buttons_layout.addWidget(self.export_html_btn)
        layout.addLayout(export_buttons_layout)

    def change_selected_count_label(self, nbr:int, all: bool):
        self.selected_count_label.setText(f"{self.model.__name__} sélectionnés: {nbr}")
        self.select_everything_checkbox.blockSignals(True)
        self.select_everything_checkbox.setChecked(all)
        self.select_everything_checkbox.blockSignals(False)

    def get_export_mode(self) -> int:
        return self.format_group.checkedId()

    def get_export_options(self) -> tuple[int, bool, bool]:
        return (
            self.get_export_mode(),
            self.print_vo_name_checkbox.isChecked(),
            self.print_source_checkbox.isChecked()
        )

