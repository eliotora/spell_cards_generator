import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
import traceback

def excepthook(type, value, tb):
    with open("error.log", "w", encoding="utf-8") as f:
        traceback.print_exception(type, value, tb, file=f)
    # Optionnel : affiche aussi dans la console
    print("".join(traceback.format_exception(type, value, tb)))
    sys.__excepthook__(type, value, tb)

sys.excepthook = excepthook

def main():
    app = QApplication(sys.argv)
    with open("styles/main_style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
    app.setWindowIcon(QIcon("app.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    sys.excepthook = excepthook
    try:
        main()
    except Exception as e:
        with open("error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise
