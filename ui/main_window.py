from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget
)
from ui.widgets.generic_tab import GenericTab
from ui.widgets.specificTabs.spell_tab import SpellTab
from model.feat_model import Feat
from model.spell_model import Spell
from model.maneuvers_model import Maneuver


class MainWindow(QMainWindow):
    details_window = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Sorts")

        # Main widget
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.spell_tab = SpellTab(self.details_window)
        self.central_widget.addTab(self.spell_tab, "Sorts")

        self.feat_tab = GenericTab(Feat, self.details_window)
        self.central_widget.addTab(self.feat_tab, "Dons")

        self.maneuver_tab = GenericTab(Maneuver, self.details_window)
        self.central_widget.addTab(self.maneuver_tab, "Manœuvres")

        self.showMaximized()

    def closeEvent(self, event):
        pass
        # for k, w in self.spell_tab.details_windows.items():
        #     w.close()
