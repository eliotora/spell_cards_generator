from model.loaders.maneuvers_loader import load_maneuvers_from_folder
from copy import deepcopy
import locale

locale.setlocale(locale.LC_COLLATE, 'French_France.1252')

class ManeuversModel:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.maneuvers = load_maneuvers_from_folder("data")
            cls.maneuvers.sort(key=lambda i: locale.strxfrm(i["nom"]))
            cls.instance = super(ManeuversModel, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_maneuver(cls, name: str):
        for maneuver in cls.maneuvers:
            if maneuver["nom"].lower() == name.lower():
                return deepcopy(maneuver)
        return None

    @classmethod
    def get_maneuvers(cls):
        return deepcopy(cls.maneuvers)