from PySide6.QtWidgets import QMessageBox

from src.models.base.base_model import MODEL_NAME_MAPPING
from src.models.collections import BaseCollection
from src.ui.details_windows.windows_manager import WindowsManager

def get_item_from_path(path:str):
    path_items = path.split("/")
    collection: BaseCollection = MODEL_NAME_MAPPING.get(path_items[0].lower()).collection
    item = collection.get_by_field("name", path_items[1])
    return item

def create_and_register_window(path: str):
    path_items = path.split("/")
    item = get_item_from_path(path)
    if item is None:
        return
    window = WindowsManager().get_window(path_items[0], item.name)
    if window is None:
        window = item.get_popup_window_class()(item)
        WindowsManager().register_window(path_items[0], item.name, window)
    window.show()
    window.activateWindow()
    return window