from feat_loader import load_feats_from_folder
from copy import deepcopy
import locale

locale.setlocale(locale.LC_COLLATE, 'French_France.1252')

class FeatModels:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.feats = load_feats_from_folder("data")
            cls.feats.sort(key=lambda i: locale.strxfrm(i["nom"]))
            cls.instance = super(FeatModels, cls).__new__(cls)
        return cls.instance

    def get_feat(cls, name:str):
        for feat in cls.feats:
            if feat["nom"].lower() == name.lower():
                return deepcopy(feat)
        return None

    def get_feats(cls):
        return deepcopy(cls.feats)

