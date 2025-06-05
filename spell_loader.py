import os
import json

SPELL_FIELDS = [
    "nom",
    "nom_VF",
    "nom_VO",
    "niveau",
    "école",
    "temps_d'incantation",
    "portée",
    "composantes",
    "durée",
    "concentration",
    "rituel",
    "description",
    "à_niveau_supérieur",
    "description_short",
]


def load_spells_from_folder(folder_path: str):
    spells = []
    class_lookup = {}

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load class spell lists ---
        class_folder = os.path.join(full_source_path, "spell_lists")
        if os.path.isdir(class_folder):
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
        for filename in os.listdir(spell_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(spell_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        spell_data = json.load(file)
                        spell = {
                            field: spell_data.get(field, "") for field in SPELL_FIELDS
                        }
                        spell["source"] = source_folder
                        spell["classes"] = sorted(
                            class_lookup.get(spell_data.get("nom", ""), [])
                        )
                        spells.append(spell)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    print(spells[:5])
    return spells
