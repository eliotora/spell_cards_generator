# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Répertoires racine
BASE_DIR = os.path.abspath(os.path.dirname(__name__))
SRC_DIR = os.path.join(BASE_DIR, "src")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Fichiers et dossiers supplémentaires à inclure
extra_datas = [
    (ASSETS_DIR, "assets"),
    (os.path.join(BASE_DIR, "version.json"), "."),
    (os.path.join(BASE_DIR, "app.ico"), "."),
]

# --- Étape 1 : Analyse du script principal ---
a = Analysis(
    [os.path.join(SRC_DIR, "main.py")],
    pathex=[SRC_DIR],
    binaries=[],
    datas=extra_datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# --- Étape 2 : Création de l’archive Python ---
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --- Étape 3 : Génération de l’exécutable ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='dnd_spell_viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(BASE_DIR, "app.ico"),
)

# --- Étape 4 : Assemblage final
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=''
)