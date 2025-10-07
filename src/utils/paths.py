import os, json
from pathlib import Path
from shutil import rmtree, copytree

def get_export_dir():
    export_dir = Path(
        os.path.expandvars(r"%USERPROFILE%\Documents\DnD Spell Viewer Exports")
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir

def check_import_validity(path, source_name):
    content = os.listdir(path)
    if not "version" in content:
        return False, f"{source_name}: No version file"
    for file_or_dir in content:
        if not (os.path.isdir(os.path.join(path, file_or_dir)) or file_or_dir == "version"):
            return False, f"{source_name}: One file is not version nor a directory"
        elif os.path.isdir(os.path.join(path, file_or_dir)): # directory on the level of spell of spell_list...
            dir_content = os.listdir(os.path.join(path, file_or_dir))
            for file in dir_content:
                if not file.endswith(".json"): # should only contain json files
                    return False, f"{source_name}: One of the files is not a json file"
        else: # Version file
            if not source_name in os.listdir("data") or not "version" in os.listdir(f"data/{source_name}"):
                continue
            with open(f"{path}//{file_or_dir}", "r", encoding="utf-8") as f:
                new_content = json.load(f)
            with open(f"data/{source_name}/version", "r", encoding="utf-8") as f:
                old_content = json.load(f)

            if new_content["source_name"] != old_content["source_name"]:
                return False, f"{source_name}: The source is different than expected"

            old_version, new_version = (old_content["version"].split("."), new_content["version"].split("."))

            for i in range(len(new_version)):
                if old_version > new_version:
                    return False, f"{source_name}: The version of the data is older than the actual"
    return True, None

def import_data(path, source_name):
    copytree(path, f"data/{source_name}", dirs_exist_ok=True)

def load_data_if_new(path):
    text = ""
    if os.path.exists(path) and os.path.isdir(path):
        path_content = os.listdir(path)
        last_dir = path.split("/")[-1]
        if "version" in path_content:
            ok, t = check_import_validity(path, last_dir)
            if t: text += t
            if ok:
                import_data(path, last_dir)
            return ok, text

        elif all([os.path.isdir(os.path.join(path, e)) for e in path_content]):
            for dir in path_content:
                ok, t = check_import_validity(f"{path}/{dir}", dir)
                if ok:
                    import_data(f"{path}/{dir}", dir)
                else:
                    text += "\n" + t
    else:
        return False, "Le chemin n'existe pas ou n'est pas un dossier"

    return False if text else True, text