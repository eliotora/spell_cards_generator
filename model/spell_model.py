from dataclasses import dataclass
from typing import Optional
from model.generic_model import (
    field_metadata,
    ExportOption,
    FilterOption,
    VisibilityOption,
    ModelCollection
)
from model.detailable_model import DetailableModel, MODEL_EXPORT_MODE_HTML_FILES
from ui.details_windows.spell_detail_window import SpellDetailWindow
import locale, os, json

locale.setlocale(locale.LC_COLLATE, "French_France.1252")


def load_spells_from_folder(folder_path: str) -> list:
    spells = []
    class_lookup = {}

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load class spell lists ---
        class_folder = os.path.join(full_source_path, "spell_lists")
        if os.path.exists(class_folder) and os.path.isdir(class_folder):
            for class_file in os.listdir(class_folder):
                if class_file.endswith(".json"):
                    file_path = os.path.join(class_folder, class_file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            class_data = json.load(file)
                            for spell_name in class_data.get("sorts", []):
                                class_lookup.setdefault(spell_name, set()).add(
                                    class_data.get("classe", "")
                                )
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Erreur lors du chargement de {class_file}: {e}")

        # --- Load spells ---
        spell_folder = os.path.join(full_source_path, "spells")
        if os.path.exists(spell_folder) and os.path.isdir(spell_folder):
            for filename in os.listdir(spell_folder):
                if filename.endswith(".json"):
                    file_path = os.path.join(spell_folder, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            spell_data = json.load(file)
                            spell = Spell(
                                name=spell_data.get("nom"),
                                vf_name=spell_data.get("nom_VF"),
                                vo_name=spell_data.get("nom_VO"),
                                level=spell_data.get("niveau"),
                                schools=spell_data.get("école"),
                                casting_time=spell_data.get("temps_d'incantation"),
                                range=spell_data.get("portée"),
                                components=spell_data.get("composantes"),
                                duration=spell_data.get("durée"),
                                concentration=spell_data.get("concentration"),
                                ritual=spell_data.get("rituel"),
                                description=spell_data.get("description"),
                                at_higher_levels=spell_data.get("à_niveau_supérieur"),
                                short_description=spell_data.get("description_short"),
                                source=source_folder,
                                classes=sorted(
                                    class_lookup.get(spell_data.get("nom", ""), [])
                                ),
                            )

                            spells.append(spell)
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"Erreur lors du chargement de {filename}: {e}")

    return spells

class SpellModels(ModelCollection):
    export_options: list[ExportOption] = [
        ExportOption.RULES,
        ExportOption.GRIMOIRE,
        ExportOption.CARDS,
    ]
    load_items_method = load_spells_from_folder

    def __init__(self):
        for export_option in self.export_options:
            MODEL_EXPORT_MODE_HTML_FILES[(Spell.__name__, export_option.value)] = f"{Spell.__name__.lower()}_{export_option.name.lower()}.html"


@dataclass
class Spell(DetailableModel):
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
    classes: list[str] = field_metadata(
        label="Classes",
        visibility=VisibilityOption.ALWAYS_HIDDEN,
        filter_type=FilterOption.LIST,
    )
    schools: list[str] = field_metadata(
        label="École",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[5],
        filter_type=FilterOption.LIST,
    )
    level: int = field_metadata(
        label="Niveau",
        filter_type=FilterOption.INT_RANGE,
        visibility=VisibilityOption.ALWAYS_VISIBLE,
    )

    casting_time: str = field_metadata(
        label="Temps d'incantation",
        visibility=VisibilityOption.HIDDABLE,
        cols_to_hide=[6],
    )
    range: str = field_metadata(
        label="Portée", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[7]
    )
    components: list[str] = field_metadata(
        label="Composantes", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[8]
    )
    duration: str = field_metadata(
        label="Durée", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    concentration: bool = field_metadata(
        label="Concentration", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[9]
    )
    ritual: bool = field_metadata(
        label="Rituel", visibility=VisibilityOption.HIDDABLE, cols_to_hide=[10]
    )
    description: str = field_metadata(
        label="Description", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    short_description: Optional[str] = field_metadata(
        label="Description",
        visibility=VisibilityOption.HIDDABLE_WITH_FILTER,
        filter_type=FilterOption.LINE_EDIT,
        cols_to_hide=[11],
    )
    at_higher_levels: Optional[str] = field_metadata(
        label="Aux niveaux supérieurs", visibility=VisibilityOption.ALWAYS_HIDDEN
    )
    source: str = field_metadata(
        label="Source",
        visibility=VisibilityOption.HIDDABLE,
        filter_type=FilterOption.LIST,
        cols_to_hide=[12],
    )
    collection = SpellModels
    details_window_class = SpellDetailWindow
    color = "#6D0000"

    def __str__(self):
        """String representation of the Spell."""
        return f"{self.name} ({self.source}) - {self.description[:50]}..."

    def to_html_dict(self):
        result = {}
        result['title'] = self.name
        if self.vo_name:
            result['subtitle'] = self.vo_name
            if self.vf_name:
                result["subtitle"] += " + " + self.vf_name
        result['italics'] = [f"niveau {self.level} - {self.schools[0] if len(self.schools) < 2 else f"{self.schools[0]} ({", ".join(self.schools[1:])})" }{f" (rituel)" if self.ritual else ""}"]
        result['bolds'] = [f"<strong>{self.__class__.__dataclass_fields__[field].metadata['label']}</strong> : {self.__getattribute__(field) if not isinstance(self.__getattribute__(field), list) else ", ".join(self.__getattribute__(field))}"
                           for field in ["casting_time", "range", "components", "duration"]]
        result['main_text'] = f"{self.description}{f"<br><strong>Aux niveaux supérieurs. </strong>{self.at_higher_levels}" if self.at_higher_levels else ""}"
        result["footer"] = [f"<div class='classe'>{classe}</div>" for classe in self.classes]
        result["source"] = self.source
        result["level"] = self.level
        result["name"] = self.name
        return result


MODEL_EXPORT_MODE_HTML_FILES[(Spell.__name__.lower(), ExportOption.GRIMOIRE.value)] = "spell_grimoire.html"
