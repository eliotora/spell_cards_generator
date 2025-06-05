from playwright.sync_api import sync_playwright
from export.html_export import html_export
import os
import random

def html_to_pdf(html_path, output_filename):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'file://{html_path}')
        page.pdf(path=output_filename, format='A4', print_background=True)
        browser.close()


def exporter_pdf(spells, path, mode='rules'):
    if not spells:
        return
    
    i = random.randint(0, 1000000)
    html_path = path.replace('.pdf', f'_{i}.html')
    while os.path.exists(html_path):
        i = random.randint(0, 1000000)
        html_path = path.replace('.pdf', f'_{i}.html')

    html_export(spells, html_path, mode)

    html_to_pdf(html_path, path)

    os.remove(html_path)  # Clean up the temporary HTML file after conversion
