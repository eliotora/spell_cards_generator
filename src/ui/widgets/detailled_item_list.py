from typing import Type
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from models.detailable_model import DetailableModel
from ui.details_windows.windows_manager import WindowsManager

class DetailledItemList(QListWidget):
    def __init__(self, model: Type[DetailableModel]):
        super().__init__()
        self.item_model = model
        self.itemDoubleClicked.connect(self.display_item_details)

    def display_item_details(self, item: QListWidgetItem):
        window = WindowsManager().get_window(self.item_model.__name__, item.text())
        if window is None:
            window = self.item_model.get_detail_windowclass()(self.item_model.get_collection().get_item(item.text()))
            WindowsManager().register_window(self.item_model.__name__, item.text(), window)
        window.show()
        window.activateWindow()


