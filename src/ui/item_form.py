from enum import Enum
from types import UnionType

from PySide6.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QMainWindow,
    QTextEdit,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
)
from typing import Union, get_origin, get_args, get_type_hints

from src.models.metadata.json_metadata import JsonMetadata
from src.ui.rich_text_editor import *
from src.models.item_model import ItemModel
from src.models.magic_item_model import (
    MagicItemModel,
    ExplorableMixin,
    ExplorerMetadata,
)


class ItemCreatorForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur de texte riche")
        self.resize(900, 650)
        self._setup_layout()

    def _setup_layout(self):
        self.setWindowTitle("Éditeur de texte riche")
        self.resize(900, 650)

        sa = QScrollArea()
        sa.setWidgetResizable(True)

        central_w = QWidget()
        sa.setWidget(central_w)
        main_layout = QVBoxLayout()
        central_w.setLayout(main_layout)
        self.setCentralWidget(sa)

        self.field_value_table = {}

        for field, field_json_meta in MagicItemModel.json_fields():
            field_explorer_meta: ExplorerMetadata = field.metadata.get(
                ExplorableMixin.METADATA_NAMESPACE
            )
            field_display_name = field_explorer_meta.label
            field_type = field_json_meta.form_type

            w = QWidget()
            l = QHBoxLayout()
            w.setLayout(l)
            l.addWidget(QLabel(f"{field_display_name} :"))
            if field_type is None:
                v = QLabel("None")
            elif field_type is str:
                v = QLineEdit()
            elif field_type is bool:
                v = QCheckBox()
            elif field_type is int:
                v = QSpinBox(minimum=-1000, maximum=100000000)
            elif field_type is float:
                v = QDoubleSpinBox(
                    minimum=-1000, maximum=1000, singleStep=0.001, decimals=3
                )
            elif get_origin(field_type) == list:
                args = get_args(field_type)[0]
                v = QListWidget()
                v.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
                arg_origin = get_origin(args)
                if arg_origin is None:
                    value_class = args
                    if issubclass(value_class, Enum):
                        for val in value_class:
                            i = QListWidgetItem(str(val))
                            i.setData(1, val.name)
                            v.addItem(i)
                elif arg_origin is UnionType or arg_origin is Union:
                    value_classes = get_args(args)
                    for c in value_classes:
                        if issubclass(c, Enum):
                            for val in c:
                                i = QListWidgetItem(str(val))
                                i.setData(1, val.name)
                                v.addItem(i)
            elif field_type is RichTextEditor:
                v = RichTextEditor()
            else:
                print(field_type)
                v = None
            if v is not None:
                l.addWidget(v)
            self.field_value_table[field.name] = v

            main_layout.addWidget(w)

        menu = self.menuBar().addMenu("Fichier")

        act_save = QAction("Enregistrer fichier JSON", self)
        act_save.setShortcut("Ctrl+S")
        act_save.triggered.connect(self._save_json)
        menu.addAction(act_save)

            # act_open = QAction("Ouvrir un ficheir JSON", self)
            # act_open.setShortcut("Ctrl+O")
            # act_open.triggered.connect(self._open_json)
            # menu.addAction(act_open)

    def get_value_from_widget(self, widget: QWidget):
        if widget is None:
            return None
        elif isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QCheckBox):
            return widget.checkState() == Qt.CheckState.Checked
        elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
            return widget.value()
        elif isinstance(widget, QListWidget):
            return [s.data(1) for s in widget.selectedItems()]
        elif isinstance(widget, RichTextEditor):
            html = widget.to_html()
            content = html.split("</head>")[1].split("</body>")[0]
            return content.split("\n")[1:]

    def _save_json(self):
        from ast import literal_eval

        json_dict = {}
        hints = get_type_hints(MagicItemModel)
        for field, json_meta in MagicItemModel.json_fields():
            val = self.get_value_from_widget(self.field_value_table[field.name])
            if not val:
                continue

            hint = hints[field.name]
            origin = get_origin(hint)
            if origin is Union or origin is UnionType:
                json_dict[field.name] = val
                continue
            if origin and not isinstance(val, origin):
                val = literal_eval(val)

            json_dict[field.name] = val

        print(json_dict)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ItemCreatorForm()
    win.show()
    sys.exit(app.exec())
