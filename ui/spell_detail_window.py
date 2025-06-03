from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea


class SpellDetailWindow(QWidget):
    def __init__(self, spell):
        super().__init__()
        self.setWindowTitle(spell.get("nom", "Détails du sort"))
        self.resize(400, 600)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.layout.addWidget(self.scroll_area)

        # Affichage des détails du sort
        for key, value in spell.items():
            if isinstance(value, list):
                value = ", ".join(value)
            elif isinstance(value, bool):
                value = "Oui" if value else "Non"
            elif value is None:
                value = "N/A"
            label = QLabel(f"<b>{key.replace("_", " ").capitalize()}:</b> {value}")
            label.setWordWrap(True)
            self.content_layout.addWidget(label)
