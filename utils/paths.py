import os
from pathlib import Path

def get_export_dir():
    export_dir = Path(
        os.path.expandvars(r"%USERPROFILE%\Documents\DnD Spell Viewer Exports")
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir