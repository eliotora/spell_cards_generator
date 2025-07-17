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
import locale, os, json

from ui.generic_detail_window import GenericDetailWindow

locale.setlocale(locale.LC_COLLATE, "French_France.1252")

class EldritchInvocationModels:
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.CARDS,
    ]

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.eldritch_invocations: list[EldritchInvocation] = load_eldritch_invocations_from_folder("data")
            cls.eldritch_invocations.sort(key=lambda i: locale.strxfrm(i.name))
            cls.instance = super(EldritchInvocationModels, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_item(cls, name: str):
        for Influx in cls.eldritch_invocations:
            if Influx.name.lower() == name.lower():
                return deepcopy(Influx)
        return None

    @classmethod
    def get_items(cls):
        return deepcopy(cls.eldritch_invocations)


@dataclass
class EldritchInvocation(ExplorableModel):
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

    def __str__(self):
        """String representation of the Eldritch Invocations."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    @classmethod
    def from_dict(cls, data: dict) -> "EldritchInvocation":
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

    @classmethod
    def get_collection(cls) -> Type:
        return EldritchInvocationModels

    @classmethod
    def get_detail_windowclass(cls):
        return GenericDetailWindow

def load_eldritch_invocations_from_folder(folder_path: str) -> list[EldritchInvocation]:
    eldritch_invocations = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        eldritch_invocations_folder = os.path.join(full_source_path, "eldritchs")
        if not os.path.exists(eldritch_invocations_folder):
            continue
        for filename in os.listdir(eldritch_invocations_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(eldritch_invocations_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        eldritch_invocation_data = json.load(file)
                        eldritch_invocation = EldritchInvocation(
                            name=eldritch_invocation_data.get("nom", ""),
                            vo_name=eldritch_invocation_data.get("nom_vo", ""),
                            vf_name=eldritch_invocation_data.get("nom_vf", ""),
                            prerequisite=eldritch_invocation_data.get("prérequis", ""),
                            description=eldritch_invocation_data.get("description", ""),
                            short_description=eldritch_invocation_data.get("description_short", ""),
                            source=source_folder,
                        )
                        eldritch_invocations.append(eldritch_invocation)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return eldritch_invocations
