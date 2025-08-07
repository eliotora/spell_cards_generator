import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
import traceback
import json
from utils.update_checks import check_for_updates, download_and_install

with open("version.json", "r") as f:
    version_info = json.load(f)
    VERSION = version_info.get("version", "unknown")


def excepthook(type, value, tb):
    with open("error.log", "w", encoding="utf-8") as f:
        traceback.print_exception(type, value, tb, file=f)
    # Optionnel : affiche aussi dans la console
    print("".join(traceback.format_exception(type, value, tb)))
    sys.__excepthook__(type, value, tb)


sys.excepthook = excepthook


def main():
    app = QApplication(sys.argv)
    with open("version.json", "r") as f:
        version_info = json.load(f)
        current_version = version_info.get("version", "unknown")
    print(f"Current version: {current_version}")
    latest, url = check_for_updates(current_version)
    if latest:
        reply = QMessageBox.question(
            None,
            "New Version Available",
            f"A new version {latest} is available. Do you want to download it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            download_and_install(url)

    with open("styles/main_style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
    app.setWindowIcon(QIcon("app.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    sys.excepthook = excepthook
    try:
        main()
    except Exception as e:
        with open("error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise
