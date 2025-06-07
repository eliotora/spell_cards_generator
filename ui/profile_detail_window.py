from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


class Profile_detail_window(QWidget):
    def __init__(self, profile):
        super().__init__()
        self.setWindowTitle(profile.get("nom", "Détails du profile"))
        self.resize(400, 600)

        # Main Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Bloc
        self.content_widget = QWidget()
        self.content_widget.setObjectName("bloc")
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel(f"<strong><span style='font-size:18pt;'>{profile["nom"][0]}</span><span style='font-size:16pt;'>{profile["nom"][1:].upper()}</span></strong>")
        self.title.setProperty("class", "h1")
        self.content_layout.addWidget(self.title)

        trad = ""
        if "nom_VO" in profile and profile["nom_VO"] != "" and profile["nom_VO"] is not None:
            trad += f"[ {profile["nom_VO"]} ]"
        if "nom_VF" in profile and profile["nom_VF"] != "" and profile["nom-VF"] is not None:
            if trad != "":
                trad += " - "
            trad += f"[ {profile["nom_VF"]} ]"
        self.trad = QLabel(trad)
        self.trad.setProperty("class", "trad")
        self.content_layout.addWidget(self.trad)

        self.sans_serif_widget = QWidget()
        self.sans_serif_layout = QVBoxLayout()
        self.sans_serif_widget.setLayout(self.sans_serif_layout)
        self.content_layout.addWidget(self.sans_serif_widget)
        self.sans_serif_widget.setProperty("class", "sans_serif")

        type = profile["type"].capitalize() + " de taille " + profile["taille"] + ", " + profile["alignement"]
        self.type = QLabel(f"{type}")
        self.type.setProperty("class", "type")
        self.sans_serif_layout.addWidget(self.type)

        self.red_widget = QWidget()
        self.red_layout = QVBoxLayout()
        self.red_widget.setLayout(self.red_layout)
        self.sans_serif_layout.addWidget(self.red_widget)

        self.red_layout.addWidget(QLabel(f"<strong>Classe d'armure </strong>{profile["classe d'armure"]}"))
        self.red_layout.addWidget(QLabel(f"<strong>Points de vie </strong>{profile["points de vie"]}"))
        self.red_layout.addWidget(QLabel(f"<strong>Vitesse </strong>{profile["vitesse"]}"))

        self.stat = QWidget()
        self.stat_layout = QHBoxLayout()
        self.stat.setLayout(self.stat_layout)
        self.red_layout.addWidget(self.stat)
        for stat in ["force", "dextérité", "constitution", "intelligence", "sagesse", "charisme"]:
            print(profile[stat])
            stat_box = QWidget()
            stat_box_layout = QVBoxLayout()
            stat_box.setLayout(stat_box_layout)
            stat_box.setProperty("class", "carac")
            stat_box_layout.addWidget(QLabel(f"<strong>{stat[:3].upper()}</strong>"))
            stat_mod = (profile[stat] - 10) // 2
            stat_box_layout.addWidget(QLabel(f"{profile[stat]} ({"{0:+}".format(stat_mod)})"))
            self.stat_layout.addWidget(stat_box)

        if "immunités (dégâts)" in profile and profile["immunités (dégâts)"]:
            self.red_layout.addWidget(QLabel(f"<strong>Immunités (dégâts) </strong>{", ".join(profile["immunités (dégâts)"])}"))

        if "immunités (états)" in profile and profile["immunités (états)"]:
            self.red_layout.addWidget(QLabel(f"<strong>Immunités (états) </strong>{", ".join(profile["immunités (états)"])}"))

        if "sens" in profile and profile["sens"]:
            self.red_layout.addWidget(QLabel(f"<strong>Sens </strong>{profile["sens"]}"))

        if "langues" in profile and profile["langues"]:
            self.red_layout.addWidget(QLabel(f"<strong>Langues </strong>{profile["langues"]}"))

        # --- Actions ---
        if "actions" in profile and profile["actions"]:
            self.action_section = QLabel("ACTIONS")
            self.action_section.setProperty("class", "rub")
            self.sans_serif_layout.addWidget(self.action_section)

            for action in profile["actions"]:
                act = profile["actions"][action]
                text = f"<strong><em>{action}. </em></strong><em>{act["type"]}</em>{act["bonus"]}, {act["portée"]} <em>Touché: </em>{act["dégâts"]}"
                label = QLabel(text)
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)
