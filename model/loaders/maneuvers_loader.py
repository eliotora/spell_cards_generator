import os
import json

MANEUVER_FIELDS = ["nom", "nom_vo", "nom_vf", "description", "description_short"]

def load_maneuvers_from_folder(folder_path: str):
    maneuvers = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        maneuvers_folder = os.path.join(full_source_path, "maneuvers")
        if not os.path.exists(maneuvers_folder):
            continue
        for filename in os.listdir(maneuvers_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(maneuvers_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        maneuver_data = json.load(file)
                        maneuver = {
                            field: maneuver_data.get(field, "") for field in MANEUVER_FIELDS
                        }
                        maneuver["source"] = source_folder
                        maneuvers.append(maneuver)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return maneuvers
