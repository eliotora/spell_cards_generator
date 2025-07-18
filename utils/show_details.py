from model.generic_model import ExplorableModel
from model.spell_model import SpellModels

PATH_COLLECTION_MAPPING = {
    "sort": SpellModels
}


def get_item_from_path(path:str) -> ExplorableModel:
    path_items = path.split("/")
    print(path_items)
    collection = PATH_COLLECTION_MAPPING[path_items[0]]
    item = collection.get_item(path_items[1])
    print(item)
    return item


