from dataclasses import dataclass
from typing import Optional
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from model.detailable_model import DetailableModel
import locale, os, json


locale.setlocale(locale.LC_COLLATE, "French_France.1252")

def load_influxs_from_folder(folder_path: str) -> list:
    influxs = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        influxs_folder = os.path.join(full_source_path, "influxs")
        if not os.path.exists(influxs_folder):
            continue
        for filename in os.listdir(influxs_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(influxs_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        influx_data = json.load(file)
                        influx = Influx(
                            name=influx_data.get("nom", ""),
                            vo_name=influx_data.get("nom_vo", ""),
                            vf_name=influx_data.get("nom_vf", ""),
                            prerequisite=influx_data.get("prérequis", ""),
                            item=influx_data.get("objet", ""),
                            description=influx_data.get("description", ""),
                            short_description=influx_data.get("description_short", ""),
                            source=source_folder,
                        )
                        influxs.append(influx)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return influxs

class InfluxModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]
    load_items_method = load_influxs_from_folder

@dataclass
class Influx(DetailableModel):
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
    prerequisite: Optional[str] = field_metadata(
        label="Prérequis", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[4]
    )
    item: str = field_metadata(
        label="Objet", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[5]
    )
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        filter_type=FilterOption.LINE_EDIT,
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        cols_to_hide=[6],
    )
    source: str = field_metadata(
        label="Source",
        filter_type=FilterOption.LIST,
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[7],
    )
    collection = InfluxModels
    color = "#dec400"

    def __str__(self):
        """String representation of the Influx."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    @classmethod
    def from_dict(cls, data: dict) -> "Influx":
        """Create a Influx instance from a dictionary."""
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
        result["title"] = self.name
        result["subtitle"] = ""
        if self.vo_name:
            result["subtitle"] = f"{self.vo_name}"
            if self.vf_name:
                result["subtitle"] += f" - {self.vf_name}"
        result["italics"] = [
            f"<em>{self.__class__.__dataclass_fields__[field].metadata['label']} : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}</em>"
            for field in ["prerequisite", "item"] if self.__getattribute__(field) != ""
        ]
        result['bolds'] = []
        result['main_text'] = self.description
        result['source'] = self.source
        return result
