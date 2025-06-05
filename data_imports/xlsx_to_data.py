from math import nan
import pandas as pd
import os
import json

def import_spells(file_path):
    """
    Imports spells from an Excel file and converts them to a dictionary format.

    :param file_path: Path to the Excel file containing spells data.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
    else:
        # Read the Excel file
        df = pd.read_excel(file_path)

        data = df.to_dict(orient='records')

        # print(data)

        for row in data:
            row["concentration"] = "concentration" in row["durée"].lower()
            composantes = row["composantes"].split(" (")[0].split(", ")
            if "(" in row["composantes"]:
                composantes[-1] = " (".join([composantes[-1], row["composantes"].split(" (")[1]])
            row["composantes"] = composantes
            row["à_niveau_supérieur"] = row["à_niveau_supérieur"] if row["à_niveau_supérieur"] == nan else ""
            row["nom_VO"] = row["nom_VO"].lower().capitalize()
            row["école"]  = row["école"].lower()
            with open("./data/Crooked Moon/spells/" + row["nom"].replace(" ", "_") + ".json", "w", encoding="utf-8") as f:
                json.dump(row, f, ensure_ascii=False , indent=4)
        print(f"Spells imported from {file_path} successfully.")
        print(f"Imported {len(data)} spells.")

def import_spell_lists(file_path):
    """
    Imports spell lists from an Excel file and converts them to a dictionary format.

    :param file_path: Path to the Excel file containing spell lists data.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
    else:
        df = pd.read_excel(file_path)
        print(df["Classe"].unique())

        classes = df["Classe"].unique()
        for classe in classes:
            print(f"Importing spells for class: {classe}")
            class_df = df[df["Classe"] == classe]
            data = {
                "classe": classe,
                "sorts": class_df["Nom"].tolist(),
            }
            with open(f"./data/Crooked Moon/spell_lists/{classe.replace(' ', '_')}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print("Spell lists imported successfully.")


if __name__=="__main__":
    # Define the path to the Excel file
    # excel_file_path = './CrookedMoon_spells.xlsx'
    import_spells("./data_imports/CrookedMoon_spells.xlsx")
    import_spell_lists("./data_imports/CrookedMoon_spell_lists.xlsx")

