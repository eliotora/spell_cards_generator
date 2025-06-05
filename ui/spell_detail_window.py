from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


class SpellDetailWindow(QWidget):
    def __init__(self, spell):
        print(f"SpellDetailWindow: {spell}")
        super().__init__()
        self.setWindowTitle(spell.get("nom", "Détails du sort"))
        self.resize(400, 600)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(0)

        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Body
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        # self.content_layout.setSpacing(0)

        # Col
        self.col = QWidget()
        self.col.setObjectName("col")
        self.content_layout.addWidget(self.col)

        self.col_layout = QVBoxLayout()
        self.col.setLayout(self.col_layout)
        # self.col_layout.setContentsMargins(0, 0, 0, 0)
        # self.col_layout.setSpacing(0)

        # Col1
        self.col1 = QWidget()
        self.col1.setObjectName("col1")
        self.col_layout.addWidget(self.col1)

        self.col1_layout = QVBoxLayout()
        # self.col1_layout.setContentsMargins(0, 0, 0, 0)
        # self.col1_layout.setSpacing(0)
        self.col1.setLayout(self.col1_layout)
        self.col1_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel(f"<h1>{spell["nom"]}<h1>")
        self.title.setProperty("class", "h1")
        self.col1_layout.addWidget(self.title)

        self.trad = QLabel(f"[ {spell["nom_VO"]} ]")
        self.trad.setProperty("class", "trad")
        self.col1_layout.addWidget(self.trad)

        ecole = "niveau" + str(spell.get("niveau", "N/A")) + " - " + spell.get("école", "N/A") + (" (rituel)" if spell.get("rituel", False) else "")
        self.ecole = QLabel(ecole)
        self.ecole.setProperty("class", "ecole")
        self.col1_layout.addWidget(self.ecole)

        self.t = QLabel(f"<strong>Temps d'incantation:</strong> {spell.get('temps_d\'incantation', 'N/A')}")
        self.t.setProperty("class", "t")
        self.col1_layout.addWidget(self.t)

        self.r = QLabel(f"<strong>Portée:</strong> {spell.get('portée', 'N/A')}")
        self.r.setProperty("class", "r")
        self.col1_layout.addWidget(self.r)

        self.c = QLabel(f"<strong>Composantes:</strong> {', '.join(spell.get('composantes', []))}")
        self.c.setProperty("class", "c")
        self.col1_layout.addWidget(self.c)

        self.d = QLabel(f"<strong>Durée:</strong> {spell.get('durée', 'N/A')}")
        self.d.setProperty("class", "d")
        self.col1_layout.addWidget(self.d)

        self.description = QLabel(f"{spell.get('description', 'Aucune description disponible.')}")
        self.description.setProperty("class", "description")
        self.description.setWordWrap(True)
        self.col1_layout.addWidget(self.description)

        self.niveau_sup = QLabel(f"{spell.get('à_niveau_supérieur', '')}")
        self.niveau_sup.setProperty("class", "description")
        self.niveau_sup.setWordWrap(True)
        self.col1_layout.addWidget(self.niveau_sup)


        # # Affichage des détails du sort
        # for key, value in spell.items():
        #     if isinstance(value, list):
        #         value = ", ".join(value)
        #     elif isinstance(value, bool):
        #         value = "Oui" if value else "Non"
        #     elif isinstance(value, str):
        #         value = value.replace("\n", "<br>").replace("\r", "")
        #         if value == "":
        #             continue  # Skip empty strings
        #     elif value is None:
        #         value = "N/A"
        #     label = QLabel(f"<b>{key.replace("_", " ").capitalize()}:</b> {value}")
        #     if key in ["nom"]:
        #         label.setObjectName("TitreSort")
        #         label.setText(f"<h1>{value}</h1>")
        #     if key in ["description", "description_short"]:
        #         label.setObjectName("DescriptionSort")
        #     label.setWordWrap(True)
        #     self.content_layout.addWidget(label)

        with open("styles/spell_detail.qss", "r", encoding="utf-8") as f:
            stylesheet = f.read()
            self.apply_stylesheet(stylesheet)

    def apply_stylesheet(self, stylesheet):
        """Applies a custom stylesheet to the widget."""
        self.setStyleSheet(stylesheet)
        self.scroll_area.setStyleSheet(stylesheet)
        self.content_widget.setStyleSheet(stylesheet)
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setStyleSheet(stylesheet)
