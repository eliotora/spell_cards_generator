from playwright.sync_api import sync_playwright
from export.html_export import html_export
import os
import random
from pathlib import Path
import sys

def get_chromium_path():
    if getattr(sys, 'frozen', False):
        # Exécution depuis un .exe PyInstaller
        base_path = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent
        # Recherche le dossier chrome-win dans ms-playwright
        chrome_dirs = list((base_path / 'ms-playwright').glob('chromium-*/chrome-win/chrome.exe'))
        if chrome_dirs:
            return chrome_dirs[0]
        else:
            raise FileNotFoundError("Chromium intégré introuvable dans ms-playwright.")
    else:
        # Mode dev
        return Path.home() / 'AppData' / 'Local' / 'ms-playwright' / 'chromium-1169' / 'chrome-win' / 'chrome.exe'

def html_to_pdf(html_path, output_filename):
    chromium_exe = get_chromium_path()
    if not chromium_exe.exists():
        raise FileNotFoundError(f"Chromium introuvable : {chromium_exe}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=str(chromium_exe),
            headless=True
        )
        page = browser.new_page()
        page.goto(f'file://{html_path}')
        page.pdf(path=output_filename, format='A4', print_background=True)
        browser.close()


def exporter_pdf(spells, path, mode='rules', show_source=False, show_VO_name=False):
    if not spells:
        return

    i = random.randint(0, 1000000)
    # html_path = path.replace('.pdf', f'_{i}.html')
    html_path = os.path.join(os.getcwd(), f"output/temp_{i}.html")
    while os.path.exists(html_path):
        i = random.randint(0, 1000000)
        # html_path = path.replace('.pdf', f'_{i}.html')
        html_path = os.path.join(os.getcwd(), f"output/temp_{i}.html")

    html_export(spells, html_path, mode, show_source=show_source, show_VO_name=show_VO_name)

    html_to_pdf(html_path, path)
    # weasy_to_pdf(html_path, path)

    os.remove(html_path)  # Clean up the temporary HTML file after conversion
