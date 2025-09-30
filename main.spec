# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Inclure les fichiers "data", "images", "styles", "output"
extra_datas = [
    ('data', 'data'),              # même s'il est vide
    ('images', 'images'),
    ('styles', 'styles'),
    ('output', 'output'),
    ('version.json', '.'),
    ('export/html_templates', 'export/html_templates'),
    ('app.ico', '.')
    # Chromium Playwright : change le chemin exact ci-dessous si besoin
    # (os.path.expanduser('~\\AppData\\Local\\ms-playwright'), 'ms-playwright')
]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=extra_datas,
    # hiddenimports=['playwright.sync_api'],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    icon=['app.ico'],
)

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