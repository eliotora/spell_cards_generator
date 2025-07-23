from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from ui.details_windows.generic_detail_window import GenericDetailWindow


class SpellDetailWindow(GenericDetailWindow):

    def __init__(self, spell, details_windows):
        super().__init__(spell, details_windows)

    def setup_layout(self):
        self.setStyleSheet("")
        with open("styles/spell_detail.qss", "r") as f:
            style = f.read()
            self.setStyleSheet(style)
        self.setWindowTitle(self.item.name)
        self.resize(400, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Scroll area pour le contenu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Body
        self.content_widget = QWidget()
        self.content_widget.setObjectName("col")
        self.scroll_area.setWidget(self.content_widget)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel(
            f"<strong><span style='font-size:18pt;'>{self.item.name[0]}</span><span style='font-size:16pt;'>{self.item.name[1:].upper()}</span></strong>"
        )
        self.title.setProperty("class", "h1")
        self.content_layout.addWidget(self.title)

        trad = ""
        if self.item.vo_name != "" and self.item.vo_name is not None:
            trad += f"[ {self.item.vo_name} ]"
        if self.item.vf_name != "" and self.item.vf_name is not None:
            if self.item.vo_name != "":
                trad += " - "
            trad += f"[ {self.item.vf_name} ]"
        self.trad = QLabel(f"{trad}")
        self.trad.setProperty("class", "trad")
        self.content_layout.addWidget(self.trad)

        ecole = (
            "niveau "
            + str(self.item.level)
            + " - "
            + self.item.school
            + (" (rituel)" if self.item.ritual else "")
        )
        self.ecole = QLabel(ecole)
        self.ecole.setProperty("class", "ecole")
        self.content_layout.addWidget(self.ecole)

        self.t = QLabel(f"<strong>Temps d'incantation:</strong> {self.item.casting_time}")
        self.t.setProperty("class", "t")
        self.t.setWordWrap(True)
        self.content_layout.addWidget(self.t)

        self.r = QLabel(f"<strong>Portée:</strong> {self.item.range}")
        self.r.setProperty("class", "r")
        self.r.setWordWrap(True)
        self.content_layout.addWidget(self.r)

        self.c = QLabel(f"<strong>Composantes:</strong> {', '.join(self.item.components)}")
        self.c.setProperty("class", "c")
        self.c.setWordWrap(True)
        self.content_layout.addWidget(self.c)

        self.d = QLabel(f"<strong>Durée:</strong> {self.item.duration}")
        self.d.setProperty("class", "d")
        self.d.setWordWrap(True)
        self.content_layout.addWidget(self.d)

        description_text = self.item.description
        description_text = self.inbed_table_style(description_text)
        self.description = QLabel(description_text)
        self.description.setProperty("class", "description")
        self.description.setWordWrap(True)
        self.description.setOpenExternalLinks(False)
        self.description.linkActivated.connect(self.handle_link_click)
        self.content_layout.addWidget(self.description)

        if self.item.at_higher_levels is not None:
            self.niveau_sup = QLabel(
                f"<strong><em>À niveau supérieur:</em></strong> {self.item.at_higher_levels}"
            )
            self.niveau_sup.setProperty("class", "description")
            self.niveau_sup.setWordWrap(True)
            self.content_layout.addWidget(self.niveau_sup)

        self.footer = QWidget()
        self.footer.setProperty("class", "footer")
        self.footer_layout = QHBoxLayout()
        self.footer.setLayout(self.footer_layout)

        for class_name in self.item.classes:
            class_label = QLabel(f"{class_name}")
            class_label.setProperty("class", "classe")
            self.footer_layout.addWidget(class_label)

        source_label = QLabel(f"{self.item.source}")
        source_label.setProperty("class", "source")
        self.footer_layout.addWidget(source_label)

        self.content_layout.addWidget(self.footer)
        self.footer_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        with open("styles/spell_detail.qss", "r", encoding="utf-8") as f:
            stylesheet = f.read()
            self.apply_stylesheet(stylesheet)

        self.scroll_area.adjustSize()

        return layout
