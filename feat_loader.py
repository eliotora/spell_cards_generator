import os
import json

FEAT_FIELDS = [
    "nom",
    "nom_vo",
    "nom_vf",
    "prérequis",
    "description",
    "description_short"
]

def load_feats_from_folder(folder_path: str):
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
                        feat = {
                            field: feat_data.get(field, "") for field in FEAT_FIELDS
                        }
                        feat["source"] = source_folder
                        feats.append(feat)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Erreur lors du chargement de {filename}: {e}")

    return feats