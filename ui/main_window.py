from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget
)
from ui.widgets.generic_tab import GenericTab
from ui.widgets.specificTabs.spell_tab import SpellTab
from model.feat_model import Feat
from model.maneuvers_model import Maneuver
from model.metamagic_model import Metamagic
from model.artificer_influx_model import Influx
from model.eldritch_invocation_model import EldritchInvocation


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

        self.eldritch_invocation_tab = GenericTab(EldritchInvocation, self.details_window)
        self.central_widget.addTab(self.eldritch_invocation_tab, "Invocations occultes")

        self.maneuver_tab = GenericTab(Maneuver, self.details_window)
        self.central_widget.addTab(self.maneuver_tab, "Manœuvres")

        self.metamagic_tab = GenericTab(Metamagic, self.details_window)
        self.central_widget.addTab(self.metamagic_tab, "Métamagie")

        self.influx_tab = GenericTab(Influx, self.details_window)
        self.central_widget.addTab(self.influx_tab, "Influx d'artificier")

        self.showMaximized()

    def closeEvent(self, event):
        for k, w in self.details_window.items():
            w.close()
