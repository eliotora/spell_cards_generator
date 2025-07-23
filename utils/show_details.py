from model.generic_model import ExplorableModel, MODEL_NAME_MAPPING

def get_item_from_path(path:str) -> ExplorableModel:
    path_items = path.split("/")
    print(path_items)
    collection = MODEL_NAME_MAPPING[path_items[0]].get_collection()
    item = collection.get_item(path_items[1])
    print(item)
    return item


