import json
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt
from src.ui.widgets.generic_tab import GenericTabWithList, GenericTab
from src.ui.widgets.specificTabs.character_tab.character_tab import CharacterTab
from src.ui.widgets.specificTabs.spell_tab.spell_tab import SpellTab
from src.ui.widgets.specificTabs.all_lists_tab.all_lists_tab import AllListsTab
from src.models.feat_model import FeatModel
from src.models.maneuvers_model import ManeuverModel
from src.models.metamagic_model import MetamagicModel
from src.models.artificer_influx_model import Influx
from src.models.eldritch_invocation_model import EldritchInvocationModel
from src.models.profile_model import ProfileModel
from src.utils.paths import get_export_dir, load_data_if_new
from src.utils.shared_dict import SharedDict
from src.ui.details_windows.windows_manager import WindowsManager

from src.models.collections import BaseCollection
from src.models.repositories.data_repository import DataRepository
from src.models import SpellModel
from src.models.mixins import ExplorableMixin
from src.models.base.base_model import MODEL_NAME_MAPPING


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

        spells = DataRepository.load_all(SpellModel)
        spell_collection = BaseCollection(spells)
        SpellModel.collection = spell_collection

        self.spell_tab = SpellTab(self.spell_dict)
        self.tabs[SpellModel.__name__] = self.spell_tab
        self.tab_widget.addTab(self.spell_tab, "Sorts")

        self.createModelTab(FeatModel, "Dons")
        self.createModelTab(EldritchInvocationModel, "Invocations occultes")
        self.createModelTab(ManeuverModel, "Manœuvres")
        self.createModelTab(MetamagicModel, "Métamagies")
        self.createModelTab(ProfileModel, "Profiles")

        # self.influx_tab = GenericTabWithList(Influx, self.shared_dict)
        # self.tabs[Influx.__name__] = self.influx_tab
        # self.tab_widget.addTab(self.influx_tab, "Influx d'artificier")

        # self.all_lists_tab = AllListsTab(self.spell_dict, self.shared_dict)
        # self.tabs["All_lists"] = self.all_lists_tab
        # self.tab_widget.addTab(self.all_lists_tab, "Toutes les listes")

        # self.char_tab = CharacterTab()
        # self.tabs["Character"] = self.char_tab
        # self.tab_widget.addTab(self.char_tab, "Character")

        load_layout = QHBoxLayout()

        load_data_button = QPushButton()
        load_data_button.setText("Charger des données")
        load_data_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        load_data_button.clicked.connect(self.load_new_data)

        save_btn = QPushButton()
        save_btn.setText("Sauvegarder toutes les listes ensemble")
        save_btn.clicked.connect(self.save_all_lists)
        save_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        load_btn = QPushButton()
        load_btn.setText("Charger un ensemble de liste")
        load_btn.clicked.connect(self.load_all_lists)
        load_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        load_layout.addWidget(load_data_button)
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

        file_content: dict[ExplorableMixin, dict] = {}
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

    def load_new_data(self): #TODO: Redo
        path = QFileDialog.getExistingDirectory(
            self,
            "Sélectionnez les données à charger",
            str(get_export_dir()),
        )
        if not path:
            return

        try:
            ok, t = load_data_if_new(path)
        except Exception as e:
            print(e)
            error = QMessageBox()
            error.setWindowTitle("Erreur lors de l'import")
            error.setText("L'import des données nécessite un accès administrateur à un dossier. Veuillez relancer l'application en mode administrateur pour avoir accès à cette fonctionnalité.")
            error.exec()
            return

        text = f"L'import a été réalisé avec succès.{t}" if ok else f"L'import n'a pas été fait pour les sources suivantes:\n{t}"

        msg = QMessageBox()
        msg.setWindowTitle("Résultat de l'import")
        msg.setText(text)
        msg.exec()

        self.reload_data()

    def reload_data(self): #TODO: Redo
        for key, element in MODEL_NAME_MAPPING.items():
            element: ExplorableMixin = element
            element.collection = BaseCollection(DataRepository.load_all(element))
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if isinstance(tab, GenericTab):
                tab.reload_data()

    def createModelTab(self, model: ExplorableMixin, tab_name: str):
        models = DataRepository.load_all(model)
        model_collection = BaseCollection(models)
        model.collection = model_collection

        model_tab = GenericTabWithList(model, self.shared_dict)
        self.tabs[model.__name__] = model_tab
        self.tab_widget.addTab(model_tab,tab_name)