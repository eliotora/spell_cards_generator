from model.generic_model import MODEL_NAME_MAPPING

def get_item_from_path(path:str):
    path_items = path.split("/")
    collection = MODEL_NAME_MAPPING[path_items[0].lower()].get_collection()
    item = collection.get_item(path_items[1])
    return item

def create_and_register_window(path: str, details_windows: dict):
    path_items = path.split("/")
    item = get_item_from_path(path)
    if item is None:
        return
    if path_items[0] not in details_windows:
        details_windows[path_items[0]] = {}
    if item.name not in details_windows[path_items[0]]:
        window = item.get_detail_windowclass()(item, details_windows)
        details_windows[path_items[0]][item.name] = window
    else:
        window = details_windows[path_items[0]][item.name]
    window.show()
    window.activateWindow()
