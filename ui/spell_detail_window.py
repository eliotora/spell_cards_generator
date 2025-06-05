from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


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
        self.layout.addWidget(self.scroll_area)

        # Body
        self.content_widget = QWidget()
        self.content_widget.setObjectName("col")
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel(f"<strong><span style='font-size:18pt;'>{spell["nom"][0]}</span><span style='font-size:16pt;'>{spell['nom'][1:].upper()}</span></strong>")
        self.title.setProperty("class", "h1")
        self.content_layout.addWidget(self.title)

        trad = ""
        if "nom_VO" in spell and spell["nom_VO"] != "" and spell["nom_VO"] is not None:
            trad += f"[ {spell['nom_VO']} ]"
        if "nom_VF" in spell and spell["nom_VF"] != "" and spell["nom_VF"] is not None:
            if "nom_VO" in spell and spell["nom_VO"] != "":
                trad += " - "
            trad += f"[ {spell['nom_VF']} ]"
        self.trad = QLabel(f"{trad}")
        self.trad.setProperty("class", "trad")
        self.content_layout.addWidget(self.trad)

        ecole = "niveau " + str(spell.get("niveau", "N/A")) + " - " + spell.get("école", "N/A") + (" (rituel)" if spell.get("rituel", False) else "")
        self.ecole = QLabel(ecole)
        self.ecole.setProperty("class", "ecole")
        self.content_layout.addWidget(self.ecole)

        self.t = QLabel(f"<strong>Temps d'incantation:</strong> {spell.get('temps_d\'incantation', 'N/A')}")
        self.t.setProperty("class", "t")
        self.t.setWordWrap(True)
        self.content_layout.addWidget(self.t)

        self.r = QLabel(f"<strong>Portée:</strong> {spell.get('portée', 'N/A')}")
        self.r.setProperty("class", "r")
        self.r.setWordWrap(True)
        self.content_layout.addWidget(self.r)

        self.c = QLabel(f"<strong>Composantes:</strong> {', '.join(spell.get('composantes', []))}")
        self.c.setProperty("class", "c")
        self.c.setWordWrap(True)
        self.content_layout.addWidget(self.c)

        self.d = QLabel(f"<strong>Durée:</strong> {spell.get('durée', 'N/A')}")
        self.d.setProperty("class", "d")
        self.d.setWordWrap(True)
        self.content_layout.addWidget(self.d)

        self.description = QLabel(f"{spell.get('description', 'Aucune description disponible.')}")
        self.description.setProperty("class", "description")
        self.description.setWordWrap(True)
        self.content_layout.addWidget(self.description)

        if spell.get("à_niveau_supérieur", "") != "" and spell.get("à_niveau_supérieur", "") is not None:
            self.niveau_sup = QLabel(f"<strong><em>À niveau supérieur:</em></strong> {spell['à_niveau_supérieur']}")
            self.niveau_sup.setProperty("class", "description")
            self.niveau_sup.setWordWrap(True)
            self.content_layout.addWidget(self.niveau_sup)

        self.footer = QWidget()
        self.footer.setProperty("class", "footer")
        self.footer_layout = QHBoxLayout()
        self.footer.setLayout(self.footer_layout)

        for class_name in spell.get("classes", []):
            class_label = QLabel(f"{class_name}")
            class_label.setProperty("class", "classe")
            self.footer_layout.addWidget(class_label)
        
        source_label = QLabel(f"{spell.get('source', 'N/A')}")
        source_label.setProperty("class", "source")
        self.footer_layout.addWidget(source_label)

        self.content_layout.addWidget(self.footer)
        self.footer_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


        with open("styles/spell_detail.qss", "r", encoding="utf-8") as f:
            stylesheet = f.read()
            self.apply_stylesheet(stylesheet)

        self.scroll_area.adjustSize()

        self.adjustSize()

    def apply_stylesheet(self, stylesheet):
        """Applies a custom stylesheet to the widget."""
        self.setStyleSheet(stylesheet)
        self.scroll_area.setStyleSheet(stylesheet)
        self.content_widget.setStyleSheet(stylesheet)
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setStyleSheet(stylesheet)
