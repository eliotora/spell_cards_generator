from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ui.widgets.SpellList import LeveledSpellList
from ui.spell_detail_window import SpellDetailWindow
from model.spell_model import SpellModels
from utils.paths import get_export_dir
import json


class SpellGrimoireWidget(QWidget):
    spell_models = SpellModels()

    def __init__(self, details_windows, parent = ...):
        super().__init__(parent)
        self.details_windows = details_windows
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        grimoire_label = QLabel("Liste de sorts")
        grimoire_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(grimoire_label)

        grimoire_name_box = QWidget()
        grimoire_name_layout = QHBoxLayout()
        grimoire_name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grimoire_name_layout.setSpacing(4)
        grimoire_name_layout.setContentsMargins(0,0,0,0)

        grimoire_name_label = QLabel("Nom:")
        grimoire_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grimoire_name_field = QLineEdit()
        self.grimoire_name_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.grimoire_name_field.setAcceptDrops(False)
        self.grimoire_name_field.setPlaceholderText("nouveau")

        grimoire_name_layout.addWidget(grimoire_name_label)
        grimoire_name_layout.addWidget(self.grimoire_name_field)
        grimoire_name_box.setLayout(grimoire_name_layout)
        main_layout.addWidget(grimoire_name_box)

        spell_list_box = QWidget()
        spell_list_layout = QGridLayout()
        spell_list_box.setLayout(spell_list_layout)
        spell_list_layout.setSpacing(4)
        spell_list_layout.setContentsMargins(0,0,0,0)
        spell_list_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(spell_list_box)

        self.spell_lists: dict[int, tuple[LeveledSpellList, QPushButton]] = {}
        for level in range(10):
            level_label = QLabel(
                f"Niveau {level}" if level > 0 else "Tours de magie"
            )
            spell_list = LeveledSpellList(level)
            spell_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            spell_list.itemDoubleClicked.connect(self.spell_double_click)

            lock_button = QPushButton()
            lock_button.setIcon(QIcon("images/unlock-48.png"))
            lock_button.setCheckable(True)
            lock_button.setToolTip("Verrouiller / Déverrouiller le drag & drop")
            lock_button.clicked.connect(
                self.toggle_lock_factory(lock_button, spell_list)
            )

            self.spell_lists[level] = (spell_list, lock_button)

            spell_list_layout.addWidget(
                level_label, 2*(level%5), 2*(level//5),
                Qt.AlignmentFlag.AlignLeft
            )
            spell_list_layout.addWidget(
                lock_button, 2*(level%5), 2*(level//5)+1,
                Qt.AlignmentFlag.AlignRight
            )
            spell_list_layout.addWidget(
                spell_list,
                2*(level%5)+1,
                2*(level//5),
                1,
                2,
                Qt.AlignmentFlag.AlignCenter
            )

            spell_list.adjustSizeToContents()
        main_layout.addSpacerItem(
            QSpacerItem(0,0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.html_export_btn = QPushButton()
        self.html_export_btn.setText("Exporter la liste en HTML")
        main_layout.addWidget(self.html_export_btn)

        save_btn = QPushButton()
        save_btn.setText("Sauver")
        save_btn.clicked.connect(self.save_spell_list)
        main_layout.addWidget(save_btn)

        load_btn = QPushButton()
        load_btn.setText("Charger")
        load_btn.clicked.connect(self.load_spell_list)
        main_layout.addWidget(load_btn)

    def spell_double_click(self, item):
        spell_name = item.text()
        self.show_spell_details(self.spell_models.get_item(spell_name))

    def show_spell_details(self, spell):
        window = SpellDetailWindow(spell, self.details_windows)
        self.details_windows[spell.name] = window
        window.main_controler = self
        window.show()

    def toggle_lock_factory(self, btn: QPushButton, list: LeveledSpellList):
        def toggle_lock(locked):
            btn.setIcon(
                QIcon("images/lock-48.png" if locked else "images/unlock-48.png")
            )
            list.setAcceptDrops(not locked)
            list.setDragEnabled(not locked)
            list.adjustSizeToContents()

        return toggle_lock

    def save_spell_list(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer la liste de sorts",
            str(get_export_dir()),
            "Fichier JSON (*.json)",
        )
        if not path:
            return
        spells = []
        for key, item in self.spell_lists.items():
            for i in range(item[0].count()):
                spell = item[0].item(i)
                spells.append(spell.text())

        if spells:
            spell_list = {"nom": self.grimoire_name_field.text(), "spells": spells}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(spell_list, f)

    def load_spell_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir une liste de sorts",
            str(get_export_dir()),
            "Fichier JSON (*.json)",
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            spell_list = json.load(f)
        self.grimoire_name_field.setText(spell_list["nom"])

        for key, item in self.spell_lists.items():
            liste = item[0]
            liste.clear()
            btn: QPushButton = item[1]
            if not btn.isChecked():
                btn.click()

        for spell_name in spell_list["spells"]:
            spell = SpellModels().get_item(spell_name)
            lvl = spell.level
            self.spell_lists[lvl][0].addItem(spell.name)

    def get_spells(self) -> dict[str, str|int|list[str]]:
        spell_list = []
        for key, item in self.spell_lists.items():
            for i in range(item[0].count()):
                spell_list.append(SpellModels().get_item(item[0].item(i).text()))
        return spell_list
