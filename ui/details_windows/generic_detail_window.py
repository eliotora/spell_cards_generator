from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from utils.show_details import create_and_register_window
import re


class GenericDetailWindow(QWidget):
    windows: list[QWidget] = []

    def __init__(self, item):
        super().__init__()
        self.item = item
        self.setLayout(self.setup_layout())
        self.adjustSize()


    def setup_layout(self) -> QVBoxLayout:
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

        for fname, field in self.item.__dataclass_fields__.items():
            if fname not in [
                "name",
                "vo_name",
                "vf_name",
                "description",
                "source",
                "classes",
                "short_description",
            ]:
                f = self.item.__getattribute__(fname)
                if f:
                    label = QLabel(f"<em>{field.metadata.get("label")}: {f}</em>")
                    label.setWordWrap(True)
                    self.content_layout.addWidget(label)

        description_text = self.item.description
        description_text = self.inbed_table_style(description_text)
        self.description = QLabel(description_text)
        self.description.setProperty("class", "description")
        self.description.setWordWrap(True)
        self.description.setOpenExternalLinks(False)
        self.description.linkActivated.connect(self.handle_link_click)
        self.content_layout.addWidget(self.description)

        self.footer = QWidget()
        self.footer.setProperty("class", "footer")
        self.footer_layout = QHBoxLayout()
        self.footer.setLayout(self.footer_layout)

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

    def apply_stylesheet(self, stylesheet):
        """Applies a custom stylesheet to the widget."""
        self.setStyleSheet(stylesheet)
        self.scroll_area.setStyleSheet(stylesheet)
        self.content_widget.setStyleSheet(stylesheet)
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setStyleSheet(stylesheet)

    def inbed_table_style(self, description):
        """Applies a custom style to tables in the description."""
        if "<table" in description:
            description = description.replace(
                "<table",
                "<table style='margin:6px 0 0 0; border-spacing:0; font-family:arial, sans-serif; font-size:17px; padding:0; box-sizing: border-box; display:table; border-collapse: separate; text-indent: initial; unicode-bidi: isolate; border-color: gray; text-align: justify; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'",
            )
            description = description.replace(
                "<tbody",
                "tbody style=margin:0; padding:0; box-sizing: border-box; displace: table-row-group; vertical-align: middle; unicode-bidi: isolate; border-color: inherit; margin-top: 6: border-spacing: 0; font-family: arial, sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; text-align: justify; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'",
            )
            tr_style = "margin:0; padding:0; box-sizing: border-box; display: table-row; vertical-align: inherit; unicode-bidi: isolate; border-color: inherit; margin-top: 6px; border-spacing: 0; font-family: arial, sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; text-align: justify; padding: 6px 0 6px 0; line-height: 1.5; overflow-y: scroll;"
            description = description.replace(
                '<th class="center"',
                "<th style='min-width: 45px; padding: 2 4 2 4; text-align: center; font-weight: bold; vertical-align: bottom; margin: 0; box-sizing: border-box; display: table-cell; unicode-bidi: isolate; border-spacing: 0; font-family: arial; sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'",
            )
            description = description.replace(
                "<th>",
                "<th style='min-width: 45px; padding: 2 4 2 4; text-align: left; font-weight: bold; vertical-align: bottom; margin: 0; box-sizing: border-box; display: table-cell; unicode-bidi: isolate; border-spacing: 0; font-family: arial; sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'>",
            )
            description = description.replace(
                '<td class="center"',
                "<td style='min-width: 45px; padding: 2 4 2 4; text-align: center; vertical-align: top; margin: 0; box-sizing: border-box; display: table-cell; unicode-bidi: isolate; border-spacing: 0; font-family: arial, sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'",
            )
            description = description.replace(
                "<td>",
                "<td style='min-width: 45px; padding: 2 4 2 4; text-align: left; vertical-align: top; margin: 0; box-sizing: border-box; display: table-cell; unicode-bidi: isolate; border-spacing: 0; font-family: arial, sans-serif; font-size: 17px; border-collapse: separate; text-indent: initial; padding: 6 0 6 0; line-height: 1.5; overflow-y: scroll;'>",
            )

            # Trouver tous les <tr ...> et ajouter un style selon l'index
            def tr_replacer(match):
                idx = tr_replacer.counter
                tr_replacer.counter += 1
                style = (
                    tr_style + " background-color: #D6d0e0;"
                    if idx % 2 == 1
                    else tr_style
                )
                if style:
                    return f"<tr style='{style}'"
                else:
                    return "<tr"

            tr_replacer.counter = 0

            # Remplacer chaque <tr> (avec ou sans attributs)
            description = re.sub("<tr", tr_replacer, description)
            description = description.replace("</table>", "</table><br>")
        return description

    def handle_link_click(self, link):
        self.windows.append(create_and_register_window(link))

    def closeEvent(self, event):
        for w in self.windows:
            w.close()
