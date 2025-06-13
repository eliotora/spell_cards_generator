from PyQt6.QtWidgets import QListWidget, QTableWidget
from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent
from model.spell_model import SpellModels

class SpellList(QListWidget):
    def __init__(self, level:int):
        super().__init__()
        self.level = level
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event:QDragEnterEvent):
        if event.mimeData().hasText():
            spell = SpellModels().get_spell(event.mimeData().text())
            if spell and spell["niveau"] == self.level and not self.findItems(spell["nom"], Qt.MatchFlag.MatchExactly):
                event.acceptProposedAction()

    def dragMoveEvent(self, event:QDragMoveEvent):
        spell = SpellModels().get_spell(event.mimeData().text())
        if event.mimeData().hasText() and spell["niveau"] == self.level and not self.findItems(spell["nom"], Qt.MatchFlag.MatchExactly):
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.addItem(SpellModels().get_spell(event.mimeData().text())["nom"])
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
            max_width = 100

        # Prendre en compte les marges internes
        frame_width = self.frameWidth() * 2
        self.setFixedHeight(
            total_height + frame_width
        )

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return

        mime_data = QMimeData()
        mime_data.setText(item.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        result = drag.exec(Qt.DropAction.MoveAction| Qt.DropAction.CopyAction)

        if result == Qt.DropAction.IgnoreAction:
            row = self.row(item)
            self.takeItem(row)
            self.adjustSizeToContents()


class SpellTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QTableWidget.DragDropMode.DragOnly)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    def startDrag(self, supportedActions):
        row = self.currentRow()
        data = self.item(row, 1).text()
        mime_data = QMimeData()
        mime_data.setText(data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.CopyAction)

