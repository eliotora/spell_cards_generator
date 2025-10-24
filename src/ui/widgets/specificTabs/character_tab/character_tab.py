from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QBoxLayout,
)

from .general_info.general_info import CharacterGeneralInfo

class CharacterTab(QWidget):
    """A tab to hold a character sheet"""

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self) -> QBoxLayout:
        """Creates the layout for the tab."""
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        general_info_widget = CharacterGeneralInfo()

        layout.addWidget(general_info_widget)

        layout.addStretch(10)

        return layout
