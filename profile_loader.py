import os
import json

PROFILE_FIELD = [
    "nom",
    "nom_VO",
    "nom_VF",
    "type",
    "taille",
    "alignement",
    "classe d'armure",
    "points de vie",
    "vitesse",
    "force",
    "dextérité",
    "constitution",
    "intelligence",
    "sagesse",
    "charisme",
    "immunités (dégâts)",
    "immunités (états)",
    "sens",
    "langues",
    "actions"
]

def load_profiles_from_folder(folder_path: str):
    profiles = []

    for source_folder in os.listdir(folder_path):
        full_source_path = os.path.join(folder_path, source_folder)
        if not os.path.isdir(full_source_path):
            continue

        # --- Load profiles ---
        profiles_folder = os.path.join(full_source_path, "profiles")
        if not os.path.exists(profiles_folder):
            continue
        for filename in os.listdir(profiles_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(profiles_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        profile_data = json.load(file)
                        profile = {
                            field: profile_data.get(field, "") for field in PROFILE_FIELD
                        }
                        profile["source"] = source_folder
                        profiles.append(profile)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

        return profiles