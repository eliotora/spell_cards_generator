from src.models.generic_model import ExplorableModel
from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, QSpacerItem, QFileDialog, QMessageBox
from PySide6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QIcon
from PySide6.QtCore import Qt, QMimeData
from typing import Type
import json

from src.ui.details_windows.windows_manager import WindowsManager
from src.utils.shared_dict import SharedDict
from src.utils.paths import get_export_dir

from src.models.mixins import ExplorableMixin, PopupMixin
from src.models.base import BaseModel



class DDList(QListWidget):
    def __init__(self, model: Type[ExplorableMixin|PopupMixin|BaseModel], shared_dict: SharedDict):
        super().__init__()
        self.item_model = model
        self._shared_dict = shared_dict
        self._shared_dict.categoryChanged.connect(self.update_list)
        self._register_list()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def _register_list(self):
        self._key = self.item_model.modelname
        self._shared_dict.add_list(self._key, [])

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasText():
            item_name = e.mimeData().text()
            if not self.findItems(item_name, Qt.MatchFlag.MatchExactly):
                e.acceptProposedAction()

    def dragMoveEvent(self, e: QDragMoveEvent):
        if e.mimeData().hasText():
            item_name = e.mimeData().text()
            if not self.findItems(item_name, Qt.MatchFlag.MatchExactly):
                e.acceptProposedAction()

    def dropEvent(self, event):
        self.addItem(
            self.item_model.get_collection().get_by_field("name", event.mimeData().text()).name
        )
        self._shared_dict.add_item(self._key, self.item_model.get_collection().get_by_field("name", event.mimeData().text()).name)
        event.acceptProposedAction()
        self.adjustSizeToContents()
        self.sortItems()

    def adjustSizeToContents(self):
        max_width = 0
        total_height = 18 if self.acceptDrops() else 0
        for i in range(self.count()):
            item = self.item(i)
            size = self.visualItemRect(item).size()
            max_width = max(max_width, size.width())
            total_height += size.height()

        if total_height == 0:
            total_height = 18
        if max_width == 0:
            max_width == 100

        frame_width = self.frameWidth() * 2
        self.setFixedHeight(total_height + frame_width)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return

        mime_data = QMimeData()
        mime_data.setText(item.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        result = drag.exec(Qt.DropAction.MoveAction | Qt.DropAction.CopyAction)

        if result == Qt.DropAction.IgnoreAction:
            row = self.row(item)
            self.takeItem(row) # TODO test si c'est pas redondant.
            self._shared_dict.remove_item(self._key, item)
            self.adjustSizeToContents()

    def update_list(self, key:str, items: list[str]):
        if self._key == key:
            current = [self.item(i).text() for i in range(self.count())]
            if current != items:
                self.clear()
                self.addItems(items)
                self.adjustSizeToContents()

    def addItems(self, labels):
        # self._shared_dict.blockSignals(True)
        super().addItems(labels)
        for label in labels:
            self._shared_dict.add_item(self._key, label)
        # self._shared_dict.blockSignals(False)

    def addItem(self, label):
        super().addItem(label)
        # self._shared_dict.blockSignals(True)
        self._shared_dict.add_item(self._key, label)
        # self._shared_dict.blockSignals(False)

class SavebleDDList(QWidget):
    def __init__(self, model: Type[ExplorableMixin|PopupMixin|BaseModel], shared_dict: SharedDict):
        super().__init__()
        self.model = model
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        list_label = QLabel(f"Liste de {self.model.modelname}")
        list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(list_label)

        name_layout = QHBoxLayout()
        name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_layout.setSpacing(4)
        name_layout.setContentsMargins(0,0,0,0)

        list_name_label = QLabel("Nom: ")
        list_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_name_field = QLineEdit()
        self.list_name_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.list_name_field.setAcceptDrops(False)
        self.list_name_field.setPlaceholderText("nouveau")

        name_layout.addWidget(list_name_label)
        name_layout.addWidget(self.list_name_field)
        main_layout.addLayout(name_layout)

        self.list = DDList(self.model, shared_dict)
        self.list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.list.itemDoubleClicked.connect(self.item_double_click)

        label = QLabel(f"{self.model.modelname}")
        self.lock_button = QPushButton()
        self.lock_button.setIcon(QIcon("assets/images/unlock-48.png"))
        self.lock_button.setCheckable(True)
        self.lock_button.setToolTip("Verrouiller / Déverrouiller le drag & drop")
        self.lock_button.clicked.connect(
            lambda state: [
                self.lock_button.setIcon(
                    QIcon("assets/images/lock-48.png" if state else "assets/images/unlock-48.png")
                ),
                self.list.setAcceptDrops(not state),
                self.list.setDragEnabled(not state),
                self.list.adjustSizeToContents()
            ]
        )

        label_lock_layout = QHBoxLayout()
        label_lock_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignLeft)
        label_lock_layout.addWidget(self.lock_button, 0, Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(label_lock_layout)
        main_layout.addWidget(self.list)

        main_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        save_btn = QPushButton()
        save_btn.setText("Enregistrer")
        save_btn.clicked.connect(self.save_list)
        main_layout.addWidget(save_btn)

        load_btn = QPushButton()
        load_btn.setText("Charger")
        load_btn.clicked.connect(self.load_list)
        main_layout.addWidget(load_btn)

        self.list.adjustSizeToContents()

    def item_double_click(self, item):
        self.show_details(self.model.get_collection().get_by_field("name", item.text()))

    def show_details(self, item: PopupMixin):
        window = WindowsManager().get_window(self.model.modelname.lower(), item.name)
        if window is None:
            window = item.__class__.get_popup_window_class()(item)
            WindowsManager().register_window(self.model.modelname.lower(), item.name, window)
        window.show()
        window.activateWindow()

    def save_list(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer la liste",
            str(get_export_dir()),
            "Fichier JSON (*.json)",
        )
        if not path:
            return
        items = self.list_to_dict()

        if items:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(items, f)

    def list_to_dict(self) -> dict:
        items = []
        for i in range(self.list.count()):
            item = self.list.item(i)
            items.append(item.text())

        if items:
            list = {"nom": self.list_name_field.text(), f"items": items, "model_name": self.model.modelname}
            return list

    def load_list(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir une liste de sorts",
            str(get_export_dir()),
            "Fichier JSON (*.json)",
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            list = json.load(f)

        self.load_list_items(list)

    def load_list_items(self, list:dict):
        if self.model.modelname != list["model_name"]:
            QMessageBox.warning(
                self,
                "Fichier non valide",
                f"Le fichier sélectionné ne correspond pas au bon model mais correspond au model {list["model_name"]}"
            )
            return

        self.list_name_field.setText(list["nom"])

        self.list.clear()
        for item_name in list["items"]:
            item:ExplorableMixin = self.model.get_collection().get_by_field("name", item_name)
            self.list.addItem(item.name)

        self.lock_button.click()
        if not self.lock_button.isChecked():
            self.lock_button.click()



