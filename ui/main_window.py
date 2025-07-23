import json
from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QFileDialog
)
from PyQt6.QtCore import Qt
from ui.widgets.generic_tab import GenericTabWithList
from ui.widgets.specificTabs.spell_tab.spell_tab import SpellTab
from ui.widgets.specificTabs.all_lists_tab.all_lists_tab import AllListsTab
from model.generic_model import ExplorableModel
from model.spell_model import Spell
from model.feat_model import Feat
from model.maneuvers_model import Maneuver
from model.metamagic_model import Metamagic
from model.artificer_influx_model import Influx
from model.eldritch_invocation_model import EldritchInvocation
from model.profile_model import Profile
from utils.paths import get_export_dir
from utils.shared_dict import SharedDict
from ui.details_windows.windows_manager import WindowsManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Sorts")

        self.tabs: dict[str, GenericTabWithList|SpellTab]= {}
        self.shared_dict = SharedDict()
        self.spell_dict = SharedDict()

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.spell_tab = SpellTab(self.spell_dict)
        self.tabs[Spell.__name__] = self.spell_tab
        self.tab_widget.addTab(self.spell_tab, "Sorts")

        self.feat_tab = GenericTabWithList(Feat, self.shared_dict)
        self.tabs[Feat.__name__] = self.feat_tab
        self.tab_widget.addTab(self.feat_tab, "Dons")

        self.eldritch_invocation_tab = GenericTabWithList(EldritchInvocation, self.shared_dict)
        self.tabs[EldritchInvocation.__name__] = self.eldritch_invocation_tab
        self.tab_widget.addTab(self.eldritch_invocation_tab, "Invocations occultes")

        self.maneuver_tab = GenericTabWithList(Maneuver, self.shared_dict)
        self.tabs[Maneuver.__name__] = self.maneuver_tab
        self.tab_widget.addTab(self.maneuver_tab, "Manœuvres")

        self.metamagic_tab = GenericTabWithList(Metamagic, self.shared_dict)
        self.tabs[Metamagic.__name__] = self.metamagic_tab
        self.tab_widget.addTab(self.metamagic_tab, "Métamagie")

        self.influx_tab = GenericTabWithList(Influx, self.shared_dict)
        self.tabs[Influx.__name__] = self.influx_tab
        self.tab_widget.addTab(self.influx_tab, "Influx d'artificier")

        self.all_lists_tab = AllListsTab(self.spell_dict, self.shared_dict)
        self.tabs["All_lists"] = self.all_lists_tab
        self.tab_widget.addTab(self.all_lists_tab, "Toutes les listes")

        Profile.get_collection()()

        load_layout = QHBoxLayout()
        save_btn = QPushButton()
        save_btn.setText("Sauvegarder toutes les listes ensemble")
        save_btn.clicked.connect(self.save_all_lists)
        save_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        load_btn = QPushButton()
        load_btn.setText("Charger un ensemble de liste")
        load_btn.clicked.connect(self.load_all_lists)
        load_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        load_layout.addWidget(save_btn)
        load_layout.addWidget(load_btn)
        load_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(load_layout)

        self.showMaximized()

    def closeEvent(self, event):
        WindowsManager().close_all_windows()

    def save_all_lists(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer les listes",
            str(get_export_dir()),
            "Fichier JSON (*.json)"
        )

        if not path:
            return

        file_content: dict[ExplorableModel, dict] = {}
        for model, tab in self.tabs.items():
            file_content[model] = tab.list_widget.list_to_dict()

        if file_content:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(file_content, file)


    def load_all_lists(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir les listes",
            str(get_export_dir()),
            "Fichier JSON (*.json)"
        )
        if not path:
            return
        with open(path, 'r', encoding="utf-8") as f:
            lists = json.load(f)

        for model, list in lists.items():
            tab = self.tabs[model]
            if list:
                tab.list_widget.load_list_items(list)

