from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget
)
from ui.spell_tab import SpellTabContent
from ui.feat_tab import FeatTabContent
import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Sorts")

        # Main widget
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.spell_tab = SpellTabContent()
        self.central_widget.addTab(self.spell_tab, "Sorts")

        self.feat_tab = FeatTabContent()
        self.central_widget.addTab(self.feat_tab, "Dons")
        
        self.showMaximized()

    def closeEvent(self, event):
        for k, w in self.spell_tab.details_windows.items():
            w.close()
