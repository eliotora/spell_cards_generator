from models.generic_model import MODEL_NAME_MAPPING
from ui.details_windows.windows_manager import WindowsManager

def get_item_from_path(path:str):
    path_items = path.split("/")
    collection = MODEL_NAME_MAPPING[path_items[0].lower()].get_collection()
    item = collection.get_item(path_items[1])
    return item

def create_and_register_window(path: str):
    path_items = path.split("/")
    item = get_item_from_path(path)
    if item is None:
        return
    window = WindowsManager().get_window(path_items[0], item.name)
    if window is None:
        window = item.get_detail_windowclass()(item)
        WindowsManager().register_window(path_items[0], item.name, window)
    window.show()
    window.activateWindow()
    return window