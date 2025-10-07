from dataclasses import dataclass
from typing import Optional
from models.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from models.detailable_model import DetailableModel
import locale, os, json


locale.setlocale(locale.LC_COLLATE, "French_France.1252")

def load_feats_from_folder(folder_path: str) -> list:
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

class FeatModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]
    load_items_method = load_feats_from_folder

@dataclass
class Feat(DetailableModel):
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
    collection = FeatModels
    color = "#C93C0C"

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

    def to_html_dict(self):
        result = {}
        result['title'] = self.name
        result["subtitle"] = ""
        if self.vo_name:
            result['subtitle'] = f"{self.vo_name}"
            if self.vf_name:
                result["subtitle"] += f" - {self.vf_name}"
        result['italics'] = [
            f"<em>{self.__class__.__dataclass_fields__[field].metadata['label']} : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}</em>"
            for field in ["prerequisite"] if self.__getattribute__(field) != ""
        ]
        result['bolds'] = []
        result['main_text'] = self.description
        result['source'] = self.source
        return result
