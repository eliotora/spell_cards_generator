import dataclasses
from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QMessageBox, QFormLayout, QListWidget
from PySide6.QtCore import Qt
from src.utils.show_details import create_and_register_window
import re

from src.models.mixins import PopupMixin
from src.models.metadata import PopupMetadata


class GenericPopupWindow(QWidget):

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

    def _get_fields(self) -> list[tuple[str,PopupMetadata, Any]]:
        """Returns all fields, heritages and mixins included"""
        result = []
        for f in dataclasses.fields(self.item):
            meta: PopupMetadata = f.metadata.get(PopupMixin.METADATA_NAMESPACE, PopupMetadata())
            if meta.hidden:
                continue
            result.append((f, meta, getattr(self.item, f.name)))
        return result

    def _make_widget(self, meta:PopupMetadata, value):
        match meta.widget:
            case "list":
                w = QListWidget()
                for item in (value or []):
                    w.addItem(str(item))
                return w
            case _:
                w = QLabel(self._format_value(value))
                w.setWordWrap(True)
                return w

    def _format_value(self, value):
        if isinstance(value, list):
            return ", ".join(str(v) for v in value) if value else "-"
        if value is None:
            return "-"
        return str(value)

    def _build_extra(self, form):
        """Hook for sub-classes"""
        pass
