from PyQt6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QWidget, QTableView
from model.spell_model import JSONTableModel
from export.pdf_export import exporter_pdf
from export.html_export import exporter_html
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lecteur JSON avec export")
        self.resize(800, 600)

        self.table_view = QTableView()
        self.model = None

        load_button = QPushButton("Charger JSON")
        load_button.clicked.connect(self.load_json)

        export_pdf_btn = QPushButton("Exporter en PDF")
        export_pdf_btn.clicked.connect(self.export_pdf)

        export_html_btn = QPushButton("Exporter en HTML")
        export_html_btn.clicked.connect(self.export_html)

        layout = QVBoxLayout()
        layout.addWidget(load_button)
        layout.addWidget(export_pdf_btn)
        layout.addWidget(export_html_btn)
        layout.addWidget(self.table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data = []

    def load_json(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier JSON", "", "JSON Files (*.json)")
        if chemin:
            with open(chemin, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                self.model = JSONTableModel(self.data)
                self.table_view.setModel(self.model)

    def export_pdf(self):
        if self.data:
            exporter_pdf(self.data, "export.pdf")

    def export_html(self):
        if self.data:
            exporter_html(self.data, "export.html")