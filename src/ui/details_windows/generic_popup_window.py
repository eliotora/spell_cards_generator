import dataclasses
from typing import Any

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QMessageBox,
    QFormLayout,
    QListWidget,
)
from PySide6.QtCore import Qt
from src.utils.show_details import create_and_register_window
import re

from src.models.mixins import PopupMixin
from src.models.metadata import PopupMetadata


class GenericPopupWindow(QWidget):
    windows: list[QWidget] = []

    def __init__(self, item: PopupMixin, parent=None):
        super().__init__(parent)
        self.item = item
        self.setWindowTitle(str(self.item))
        self.setLayout(self.setup_layout())
        self.adjustSize()

    def setup_layout(self) -> QVBoxLayout:
        self.setStyleSheet("")
        with open("assets/styles/spell_detail.qss", "r") as f:
            style = f.read()
            self.setStyleSheet(style)
        self.resize(400, 600)

        # Main layout
        layout = QVBoxLayout()

        # Scrollarea for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form = QFormLayout(container)
        form.setSpacing(0)

        for field, meta, value in self._get_fields():
            widget = self._make_widget(meta, value)
            label = QLabel(f"<b>{meta.label}</b>")
            if meta.style:
                widget.setStyleSheet(meta.style)

            form.addRow(label, widget)

        # Space for additional widgets of sub-classes
        self._build_extra(form)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        return layout

    def _get_fields(self) -> list[tuple[str, PopupMetadata, Any]]:
        """Returns all fields, heritages and mixins included"""
        result = []
        for f in dataclasses.fields(self.item):
            meta: PopupMetadata = f.metadata.get(
                PopupMixin.METADATA_NAMESPACE, PopupMetadata()
            )
            if meta.hidden:
                continue
            result.append((f, meta, getattr(self.item, f.name)))
        return result

    def _make_widget(self, meta: PopupMetadata, value):
        match meta.widget:
            case "list":
                w = QListWidget()
                for item in value or []:
                    w.addItem(str(item))
                return w
            case _:
                w = QLabel(self._format_value(value))
                w.setWordWrap(True)
                return w

    def _format_value(self, value):
        if isinstance(value, list):
            return ", ".join(str(self._inbed_table_style(v)) for v in value) if value else "-"
        if value is None:
            return "-"
        return str(value)

    def _build_extra(self, form):
        """Hook for sub-classes"""
        pass

    def _inbed_table_style(self, description: str):
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

    def _handle_link_click(self, link):
        window = create_and_register_window(link)
        if window is None:
            QMessageBox.critical(
                self,
                "Not found",
                f'This item was not found. Please inform your administrator that the link "{link}" doesn\'t work in the object {self.item.source+" / "+self.item.modelname+" / "+self.item.name}',
                buttons=QMessageBox.StandardButton.Ok,
            )
            return
        self.windows.append(window)

    def closeEvent(self, event):
        for w in self.windows:
            w.close()
