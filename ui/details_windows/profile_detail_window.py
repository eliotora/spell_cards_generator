from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from ui.details_windows.generic_detail_window import GenericDetailWindow

class ProfileDetailWindow(GenericDetailWindow):
    def __init__(self, profile):
        super().__init__(profile)

    def setup_layout(self):
        self.setWindowTitle(self.item.name)
        self.resize(400, 600)

        # Main Layout
        layout = QVBoxLayout()
        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

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

        self.title = QLabel(
            f"<strong><span style='font-size:18pt;'>{self.item.name[0]}</span><span style='font-size:16pt;'>{self.item.name[1:].upper()}</span></strong>"
        )
        self.title.setObjectName("name")
        self.content_layout.addWidget(self.title)

        if (
            (
                self.item.vo_name != ""
                and self.item.vo_name is not None
            )
            or (
                self.item.vf_name != ""
                and self.item.vf_name is not None
            )
        ):
            trad = ""
            if (
                self.item.vo_name != ""
                and self.item.vo_name is not None
            ):
                trad += f"[ {self.item.vo_name} ]"
            if (
                self.item.vf_name != ""
                and self.item.vf_name is not None
            ):
                if trad != "":
                    trad += " - "
                trad += f"[ {self.item.vf_name} ]"
            self.trad = QLabel(trad)
            self.trad.setObjectName("trad")
            self.content_layout.addWidget(self.trad)

        self.sans_serif_widget = QWidget()
        self.sans_serif_layout = QVBoxLayout()
        self.sans_serif_widget.setLayout(self.sans_serif_layout)
        self.content_layout.addWidget(self.sans_serif_widget)
        self.sans_serif_widget.setObjectName("sans_serif")

        type = self.item.type.capitalize() + " de taille " + self.item.size
        type += f", {self.item.alignment}" if self.item.alignment else ""
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

        ca = QLabel(f"<strong>Classe d'armure </strong>{self.item.ac}")
        ca.setWordWrap(True)
        self.red_layout.addWidget(ca)

        pv = QLabel(f"<strong>Points de vie </strong>{self.item.hp}")
        pv.setWordWrap(True)
        self.red_layout.addWidget(pv)

        speed = QLabel(f"<strong>Vitesse </strong>{self.item.speed}")
        speed.setWordWrap(True)
        self.red_layout.addWidget(speed)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        self.stat = QWidget()
        self.stat.setObjectName("carac")
        # self.stat.setMaximumWidth(500)
        self.stat_layout = QHBoxLayout()
        self.stat_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stat_layout.setContentsMargins(0, 0, 0, 0)
        self.stat_layout.setSpacing(0)
        self.stat.setLayout(self.stat_layout)
        self.red_layout.addWidget(self.stat)
        for stat, value in self.item.stats.items():
            stat_mod = (value - 10) // 2
            l1 = QLabel(
                f"<strong>{stat[:3].upper()}</strong><br>{value} ({"{0:+}".format(stat_mod)})"
            )
            l1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stat_layout.addWidget(l1, stretch=1)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        if self.item.details:
            for detail in self.item.details:
                if self.item.details[detail]:
                    l = QLabel(
                        f"<strong>{detail}. </strong>{", ".join(self.item.details[detail])}"
                    )
                    self.red_layout.addWidget(l)
                    l.setWordWrap(True)

        svg_sep = QSvgWidget("./images/profile_sep.svg")
        self.red_layout.addWidget(svg_sep)

        # --- Traits ---
        if self.item.traits:
            for trait in self.item.traits:
                t = self.item.traits[trait]
                text = f"<strong><em>{trait}. </em></strong>{t}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        # --- Actions ---
        if self.item.actions:
            self.action_section = QLabel("ACTIONS")
            self.action_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.action_section)

            for action in self.item.actions:
                act = self.item.actions[action]
                text = f"<strong><em>{action}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if self.item.bonus_actions:
            print("Action bonus, ", self.item.bonus_actions)
            self.bonusaction_section = QLabel("ACTIONS BONUS")
            self.bonusaction_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.bonusaction_section)

            for bonusaction in self.item.bonus_actions:
                act = self.item.bonus_actions[bonusaction]
                text = f"<strong><em>{bonusaction}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if self.item.reactions:
            self.reaction_section = QLabel("RÉACTIONS")
            self.reaction_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.reaction_section)

            for reaction in self.item.reactions:
                act = self.item.reactions[reaction]
                text = f"<strong><em>{reaction}. </em></strong>{act}"
                label = QLabel(text)
                label.setObjectName("p")
                label.setWordWrap(True)
                self.sans_serif_layout.addWidget(label)

        if self.item.legendary_actions:
            self.leg_action_section = QLabel("ACTIONS LÉGENDAIRES")
            self.leg_action_section.setObjectName("rub")
            self.sans_serif_layout.addWidget(self.leg_action_section)
            legtext = QLabel(self.item.legendary_actions)
            legtext.setWordWrap(True)
            legtext.setObjectName("p")
            self.sans_serif_layout.addWidget(legtext)

            for leg_action in self.item.legendary_actions:
                act = self.item.legendary_actions[leg_action]
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

        with open("styles/profile_detail.qss", "r", encoding="utf-8") as f:
            stylesheet = f.read()
            self.apply_stylesheet(stylesheet)

        return layout

    def apply_stylesheet(self, stylesheet):
        """Applies a custom stylesheet to the widget"""

        def recusive_applying(widget: QWidget):
            widget.setStyleSheet(stylesheet)
            layout = widget.layout()
            if layout:
                for i in range(layout.count()):
                    w = layout.itemAt(i).widget()
                    if w:
                        recusive_applying(w)

        self.setStyleSheet(stylesheet)
        recusive_applying(self.content_widget)
