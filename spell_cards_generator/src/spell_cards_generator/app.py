import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from src.ui_mobile.main_view import MainView


class SpellCardsApp(toga.App):
    def startup(self):
        # Crée ta fenêtre principale
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Instancie ta vue principale
        self.main_view = MainView()
        self.main_view.startup()

        # Ajoute-la à la fenêtre
        self.main_window.content = self.main_view

        # Affiche la fenêtre
        self.main_window.show()
        print("Showing main window")


def main():
    # Toga va appeler main() pour obtenir une instance de App
    return SpellCardsApp('Spell Cards Generator', 'com.eliotora.spell_cards_generator')
