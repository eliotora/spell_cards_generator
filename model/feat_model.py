from dataclasses import dataclass
from typing import Optional, Type
from copy import deepcopy
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ExplorableModel,
)
from ui.feat_detail_window import FeatDetailWindow
import locale, os, json

from ui.generic_detail_window import GenericDetailWindow

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

class FeatModels:
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.feats: list[Feat] = load_feats_from_folder("data")
            cls.feats.sort(key=lambda i: locale.strxfrm(i.name))
            cls.instance = super(FeatModels, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_item(cls, name: str):
        for feat in cls.feats:
            if feat.name.lower() == name.lower():
                return deepcopy(feat)
        return None

    @classmethod
    def get_items(cls):
        return deepcopy(cls.feats)


@dataclass
class Feat(ExplorableModel):
    name: str = field_metadata(
        label="Nom",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.ALWAYS_VISIBLE,
    )
    vf_name: Optional[str] = field_metadata(
        label="Nom VF", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[2]
    )
    vo_name: Optional[str] = field_metadata(
        label="Nom VO", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[3]
    )
    prerequisite: str = field_metadata(
        label="Prérequis", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[4]
    )
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        cols_to_hide=[5],
    )
    source: str = field_metadata(
        label="Source",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[6],
    )

    def __str__(self):
        """String representation of the Feat."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    @classmethod
    def from_dict(cls, data: dict) -> "Feat":
        """Create a Feat instance from a dictionary."""
        return cls(
            name=data.get("nom", ""),
            vo_name=data.get("nom_vo"),
            vf_name=data.get("nom_vf"),
            prerequisite=data.get("prérequis", ""),
            description=data.get("description", ""),
            short_description=data.get("description_short"),
            source=data.get("source", ""),
        )

    @classmethod
    def get_collection(cls) -> Type:
        return FeatModels

    @classmethod
    def get_detail_windowclass(cls):
        return GenericDetailWindow


FEAT_FIELDS = [
    "nom",
    "nom_vo",
    "nom_vf",
    "prérequis",
    "description",
    "description_short",
]


def load_feats_from_folder(folder_path: str) -> list[Feat]:
    feats = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        feats_folder = os.path.join(full_source_path, "feats")
        if not os.path.exists(feats_folder):
            continue
        for filename in os.listdir(feats_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(feats_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        feat_data = json.load(file)
                        feat = Feat(
                            name=feat_data.get("nom", ""),
                            vo_name=feat_data.get("nom_vo", ""),
                            vf_name=feat_data.get("nom_vf", ""),
                            prerequisite=feat_data.get("prérequis", ""),
                            description=feat_data.get("description", ""),
                            short_description=feat_data.get("description_short", ""),
                            source=source_folder,
                        )
                        feats.append(feat)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return feats
