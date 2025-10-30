from PySide6.QtWidgets import QWidget, QLabel, QTableWidget, QVBoxLayout
from PySide6.QtCore import Qt

class SpellTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        title = QLabel("CANTRIPS & PREPARED SPELLS")

        self.spell_table = QTableWidget()
        headers = [
            "Level", "Name", "Casting Time", "Range", "Concentration, Ritual & Required Material", "Notes"
        ]
        self.spell_table.setColumnCount(len(headers))
        self.spell_table.setHorizontalHeaderLabels(headers)
        self.spell_table.verticalHeader().hide()

        layout.addWidget(title)
        layout.addWidget(self.spell_table)

        return layout

