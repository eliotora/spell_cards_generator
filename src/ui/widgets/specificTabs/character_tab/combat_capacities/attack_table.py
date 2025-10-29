from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget
from PySide6.QtCore import Qt

class AttackTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5,5,5,5)

        label = QLabel("WEAPONS & DAMAGE CANTRIPS")
        self.table = QTableWidget(rowCount=6, columnCount=4)
        self.table.setHorizontalHeaderLabels(["Name", "Atk Bonus / DC", "Damages & Type", "Notes"])
        self.table.verticalHeader().hide()

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.table)

        return layout
