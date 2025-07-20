from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from model.generic_model import ExplorableModel

class DetailledItemList(QListWidget):
    def __init__(self, details_windows, model: ExplorableModel):
        super().__init__()
        self.details_windows = details_windows
        self.item_model = model
        self.itemDoubleClicked.connect(self.display_item_details)

    def display_item_details(self, item: QListWidgetItem):
        item_name = item.text()
        if item_name not in self.details_windows:
            self.details_windows[item_name] = self.item_model.get_detail_windowclass()(self.item_model.get_collection().get_item(item_name), self.details_windows)
        self.details_windows[item_name].show()
        self.details_windows[item_name].activateWindow()


