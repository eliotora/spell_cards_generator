from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from ui.widgets.specificTabs.character_tab.underlabeled_line_edit import UnderlabeledLineEdit

class LevelXpWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.level = UnderlabeledLineEdit("Level".upper(), label_alignement=Qt.AlignmentFlag.AlignCenter)
        self.xp = UnderlabeledLineEdit("XP".upper(), label_alignement=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.level, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.xp, Qt.AlignmentFlag.AlignTop)

        return layout

