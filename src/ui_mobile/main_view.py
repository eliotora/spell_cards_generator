import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class MainView(toga.Box):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.label = toga.Label(
            "Bienvenue dans DnD Spell Viewer (version mobile)",
            style=Pack(padding=10),
        )

        btn = toga.Button(
            "Afficher les sorts",
            on_press=self.show_spells,
            style=Pack(padding=10),
        )

        main_box.add(self.label)
        main_box.add(btn)

        print("MainView initialized")

        # self.main_window = toga.MainWindow(title="DnD Spell Viewer")
        # self.main_window.content = main_box
        # self.main_window.show()

    def show_spells(self, widget):
        self.label.text = ("Liste des sorts affichée ici")