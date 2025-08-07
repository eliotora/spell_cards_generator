from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent
from model.spell_model import SpellModels, Spell
from ui.widgets.genericTab.genericDDList import DDList


class LeveledSpellList(DDList):
    def __init__(self, level: int, shared_dict):
        self.level = level
        super().__init__(Spell, shared_dict)

    def _register_list(self):
        self._key = str(self.level)
        self._shared_dict.add_list(self._key, [])

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            spell = SpellModels().get_item(event.mimeData().text())
            if (
                spell
                and spell.level == self.level
                and not self.findItems(spell.name, Qt.MatchFlag.MatchExactly)
            ):
                event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        spell = SpellModels().get_item(event.mimeData().text())
        if (
            event.mimeData().hasText()
            and spell.level == self.level
            and not self.findItems(spell.name, Qt.MatchFlag.MatchExactly)
        ):
            event.acceptProposedAction()


class DDTable(QTableWidget):
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
