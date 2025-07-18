from model.generic_model import ExplorableModel
from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, QSpacerItem, QFileDialog, QMessageBox
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QIcon
from PyQt6.QtCore import Qt, QMimeData
from typing import Type
import json

from utils.paths import get_export_dir



class DDList(QListWidget):
    def __init__(self, model: Type[ExplorableModel]):
        super().__init__()
        self.item_model = model
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

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
            self.item_model.get_collection().get_item(event.mimeData().text()).name
        )
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
            self.takeItem(row)
            self.adjustSizeToContents()


class SavebleDDList(QWidget):
    def __init__(self, model: Type[ExplorableModel], details_windows):
        super().__init__()
        self.model = model
        self.details_windows = details_windows
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        list_label = QLabel(f"Liste de {self.model.__name__}")
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

        self.list = DDList(self.model)
        self.list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.list.itemDoubleClicked.connect(self.item_double_click)

        label = QLabel(f"{self.model.__name__}")
        self.lock_button = QPushButton()
        self.lock_button.setIcon(QIcon("images/unlock-48.png"))
        self.lock_button.setCheckable(True)
        self.lock_button.setToolTip("Verrouiller / Déverrouiller le drag & drop")
        self.lock_button.clicked.connect(
            lambda state: [
                self.lock_button.setIcon(
                    QIcon("images/lock-48.png" if state else "images/unlock-48.png")
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
        self.show_details(self.model.get_collection.get_item(item.text()))

    def show_details(self, item: ExplorableModel):
        window = item.get_detail_windowclass()(item, self.details_windows)
        self.details_windows[item.name] = window
        window.show()

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
            list = {"nom": self.list_name_field.text(), f"items": items, "model_name": self.model.__name__}
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
        if self.model.__name__ != list["model_name"]:
            QMessageBox.warning(
                self,
                "Fichier non valide",
                f"Le fichier sélectionné ne correspond pas au bon model mais correspond au model {list["model_name"]}"
            )
            return

        self.list_name_field.setText(list["nom"])

        self.list.clear()
        for item_name in list["items"]:
            item:ExplorableModel = self.model.get_collection().get_item(item_name)
            self.list.addItem(item.name)

        self.lock_button.click()
        if not self.lock_button.isChecked():
            self.lock_button.click()



