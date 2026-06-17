from PySide6.QtWidgets import QVBoxLayout,QHBoxLayout, QScrollArea, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget

from src.ui.details_windows.generic_popup_window import GenericPopupWindow
from src.ui.popup_factory import PopupFactory
from src.models.item_model import ItemModel


class ItemPopupWindow(GenericPopupWindow):
    def __init__(self, item: ItemModel, parent=None):
        super().__init__(item, parent)
        self.setWindowTitle(item.name)

    def setup_layout(self):
        item: ItemModel = self.item
        self.setStyleSheet("")
        with open("assets/styles/item_popup.qss") as f:
            style = f.read()
            self.setStyleSheet(style)
        self.resize(400, 600)

        # Main layout
        layout = QVBoxLayout()

        # Scrollarea for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout.addWidget(scroll)
        scroll.setWidget(container)
        in_layout = QVBoxLayout()
        container.setLayout(in_layout)
        in_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Layout setup
        middle_h_widget = QWidget()
        middle_h_layout = QHBoxLayout()
        middle_h_widget.setLayout(middle_h_layout)

        # Content
        name_label = QLabel(item.name.upper())
        type_label = QLabel(", ".join([str(t).capitalize() for t in item.item_type]))

        if item.weapon_data:
            weapon_sub_type = QLabel(item.weapon_data.weapontype)

        if item.value_cp or item.weight:
            a = []
            if item.value_cp: a.append(f"{f"{str(item.value_cp)}"}")
            if item.weight: a.append(f"{item.weight} kg")
            s = ", ".join(a)
            price_weight_label = QLabel(s)

        item_label = None

        datas = [item.weapon_data, item.armor_data, item.mount_data, item.vehicle_data]
        if any(datas):
            res = "\n".join([d.get_data_text() for d in datas if d])
            item_label = QLabel(res)
            item_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            item_label.setWordWrap(True)

        separator = QWidget()

        # Entries
        entries = []
        for entry_name, entry in item.get_entries():
            if entry_name:
                entry_label = QLabel(f"<b><em>{entry_name}.</em></b> {entry}")
            else:
                entry_label = QLabel(f"{entry}")
            entry_label.setWordWrap(True)
            entries.append(entry_label)

        source_label = QLabel(f"<b>Source: </b>{item.source}")


        # Add content to layout
        in_layout.addWidget(name_label)
        in_layout.addWidget(type_label)
        if item.weapon_data: in_layout.addWidget(weapon_sub_type)
        if price_weight_label: middle_h_layout.addWidget(price_weight_label)
        if item_label: middle_h_layout.addWidget(item_label)
        in_layout.addWidget(middle_h_widget)
        in_layout.addWidget(separator)
        for e in entries:
            in_layout.addWidget(e)
        in_layout.addWidget(source_label)

        scroll.adjustSize()

        # Widget naming for style:
        container.setObjectName("container")
        name_label.setObjectName("title")
        type_label.setObjectName("type")
        if item.weapon_data: weapon_sub_type.setObjectName("subtype")
        separator.setObjectName("orange")

        return layout



PopupFactory.register(ItemModel, ItemPopupWindow)
ItemModel.popup_window_class = ItemPopupWindow