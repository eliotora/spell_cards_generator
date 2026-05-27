from typing import Type
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from src.models.detailable_model import DetailableModel
from src.ui.details_windows.windows_manager import WindowsManager

from src.models.mixins import PopupMixin, ExplorableMixin
from src.models.base import BaseModel

class DetailledItemList(QListWidget):
    def __init__(self, model: Type[PopupMixin|ExplorableMixin|BaseModel]):
        super().__init__()
        self.item_model = model
        self.itemDoubleClicked.connect(self.display_item_details)

    def display_item_details(self, item: QListWidgetItem):
        window = WindowsManager().get_window(self.item_model.modelname, item.text())
        if window is None:
            window = self.item_model.get_popup_window_class()(self.item_model.collection.get_by_field("name", item.text()))
            WindowsManager().register_window(self.item_model.modelname, item.text(), window)
        window.show()
        window.activateWindow()


