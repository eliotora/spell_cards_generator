from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget


class Profile_detail_window(QWidget):
    def __init__(self, profile, show_VO_name=True):
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
        self.content_widget.setObjectName("content")
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.orange_top = QWidget()
        self.orange_top.setObjectName("orange")
        self.content_layout.addWidget(self.orange_top)
        self.orange_top.setMinimumHeight(6)

        self.title = QLabel(f"<strong><span style='font-size:18pt;'>{profile["nom"][0]}</span><span style='font-size:16pt;'>{profile["nom"][1:].upper()}</span></strong>")
        self.title.setObjectName("name")
        self.content_layout.addWidget(self.title)

        if show_VO_name and (
            "nom_VO" in profile and profile["nom_VO"] != "" and profile["nom_VO"] is not None
        ) or (
            "nom_VF" in profile and profile["nom_VF"] != "" and profile["nom-VF"] is not None
        ):
            trad = ""
            if "nom_VO" in profile and profile["nom_VO"] != "" and profile["nom_VO"] is not None:
                trad += f"[ {profile["nom_VO"]} ]"
            if "nom_VF" in profile and profile["nom_VF"] != "" and profile["nom-VF"] is not None:
                if trad != "":
                    trad += " - "
                trad += f"[ {profile["nom_VF"]} ]"
            self.trad = QLabel(trad)
            self.trad.setObjectName("trad")
            self.content_layout.addWidget(self.trad)

        self.sans_serif_widget = QWidget()
        self.sans_serif_layout = QVBoxLayout()
        self.sans_serif_widget.setLayout(self.sans_serif_layout)
        self.content_layout.addWidget(self.sans_serif_widget)
        self.sans_serif_widget.setObjectName("sans_serif")

        type = profile["type"].capitalize() + " de taille " + profile["taille"]
        type += f", {profile["alignement"]}" if profile["alignement"] else ""
        self.type = QLabel(f"{type}")
        self.type.setWordWrap(True)
        self.type.setObjectName("type")
        self.sans_serif_layout.addWidget(self.type)

        self.red_widget = QWidget()
        self.red_layout = QVBoxLayout()
        self.red_widget.setLayout(self.red_layout)
        self.red_widget.setObjectName("red")
        self.sans_serif_layout.addWidget(self.red_widget)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        ca = QLabel(f"<strong>Classe d'armure </strong>{profile["classe d'armure"]}")
        ca.setWordWrap(True)
        self.red_layout.addWidget(ca)

        pv = QLabel(f"<strong>Points de vie </strong>{profile["points de vie"]}")
        pv.setWordWrap(True)
        self.red_layout.addWidget(pv)

        speed = QLabel(f"<strong>Vitesse </strong>{profile["vitesse"]}")
        speed.setWordWrap(True)
        self.red_layout.addWidget(speed)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        self.stat = QWidget()
        self.stat.setObjectName("carac")
        # self.stat.setMaximumWidth(500)
        self.stat_layout = QHBoxLayout()
        self.stat_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stat_layout.setContentsMargins(0,0,0,0)
        self.stat_layout.setSpacing(0)
        self.stat.setLayout(self.stat_layout)
        self.red_layout.addWidget(self.stat)
        for stat in ["force", "dextérité", "constitution", "intelligence", "sagesse", "charisme"]:
            stat_mod = (profile[stat] - 10) // 2
            l1 = QLabel(f"<strong>{stat[:3].upper()}</strong><br>{profile[stat]} ({"{0:+}".format(stat_mod)})")
            l1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # l1.setContentsMargins(0,0,0,0)
            self.stat_layout.addWidget(l1, stretch=1)

            # print(stat_box.size())

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        if "détails" in profile and profile["détails"]:
            for detail in profile["détails"]:
                if profile["détails"][detail]:
                    l = QLabel(f"<strong>{detail}. </strong>{", ".join(profile["détails"][detail])}")
                    self.red_layout.addWidget(l)
                    l.setWordWrap(True)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        # --- Traits ---
        if "traits" in profile and profile["traits"]:
            for trait in profile["traits"]:
                t = profile["traits"][trait]
                text = f"<strong><em>{trait}. </em></strong>{t}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        # --- Actions ---
        if "actions" in profile and profile["actions"]:
            self.action_section = QLabel("ACTIONS")
            self.action_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.action_section)

            for action in profile["actions"]:
                act = profile["actions"][action]
                if act["type"] == "Capacité":
                    text = f"<strong><em>{action}. </em></strong>{act["bonus"]}"
                else:
                    text = f"<strong><em>{action}. </em></strong><em>{act["type"]}</em>{act["bonus"]}, {act["portée"]} <em>Touché: </em>{act["dégâts"]}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if "actions bonus" in profile and profile["actions bonus"]:
            self.bonusaction_section = QLabel("ACTIONS BONUS")
            self.bonusaction_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.bonusaction_section)

            for bonusaction in profile["actions bonus"]:
                act = profile["actions bonus"][bonusaction]
                text = f"<strong><em>{bonusaction}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if "réactions" in profile and profile["réactions"]:
            self.reaction_section = QLabel("RÉACTIONS")
            self.reaction_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.reaction_section)

            for reaction in profile["réactions"]:
                act = profile["réactions"][reaction]
                text = f"<strong><em>{reaction}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if "actions_leg" in profile and profile["actions_leg"]:
            self.leg_action_section = QLabel("ACTIONS LÉGENDAIRES")
            self.leg_action_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.leg_action_section)
            legtext = QLabel(profile["actions_leg_texte"])
            legtext.setWordWrap(True)
            legtext.setObjectName("p")
            self.sans_serif_layout.addWidget(legtext)

            for leg_action in profile["actions_leg"]:
                act = profile["actions_leg"][leg_action]
                text = f"<strong><em>{leg_action}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        self.orange_bot = QWidget()
        self.orange_bot.setObjectName("orange")
        self.content_layout.addWidget(self.orange_bot)
        self.orange_bot.setMinimumHeight(6)
        self.setMinimumWidth(450)
        self.adjustSize()

        with open("styles/profile_detail.qss", "r", encoding="utf-8") as f:
            stylesheet = f.read()
            self.apply_stylesheet(stylesheet)


    def apply_stylesheet(self, stylesheet):
        """Applies a custom stylesheet to the widget"""
        def recusive_applying(widget:QWidget):
            widget.setStyleSheet(stylesheet)
            layout = widget.layout()
            if layout:
                for i in range(layout.count()):
                    w = layout.itemAt(i).widget()
                    if w:
                        recusive_applying(w)

        self.setStyleSheet(stylesheet)
        recusive_applying(self.content_widget)

