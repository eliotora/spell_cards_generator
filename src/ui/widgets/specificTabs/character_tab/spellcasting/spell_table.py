from PySide6.QtWidgets import QWidget, QLabel, QTableWidget, QVBoxLayout, QTableWidgetItem, QCheckBox, QHBoxLayout, QPushButton, QListWidget, QDialog, QLineEdit
from PySide6.QtCore import Qt, Signal
from src.ui.details_windows.windows_manager import WindowsManager
from src.models.spell_model import SpellModel

class SelectOneSpellList(QDialog):
    add_spell_signal = Signal(SpellModel)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select a Spell to Add")
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.filter_spells_name)
        layout.addWidget(self.name_input)

        self.spell_list = QListWidget()
        self.spell_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.spell_list)

        self.add_button = QPushButton("Add Spell")
        self.add_button.clicked.connect(self.add_spell)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_spell(self):
        if self.spell_list.currentItem() is None:
            return
        spell = SpellModel.collection.get_by_field("name", self.spell_list.currentItem().text())
        self.add_spell_signal.emit(spell)
        self.close()

    def populate_spells(self, spells: list[SpellModel]):
        self.spell_list.clear()
        for spell in spells:
            self.spell_list.addItem(spell.name)

    def filter_spells_name(self):
        text = self.name_input.text().lower()
        for r in range(self.spell_list.count()):
            row = self.spell_list.item(r)
            row.setHidden((not text in row.text().lower()))
class SpellTableWidget(QWidget):
    add_spell_popup : SelectOneSpellList = None

    def __init__(self):
        super().__init__()
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()

        title = QLabel("CANTRIPS & PREPARED SPELLS")

        self.spell_table = QTableWidget()
        headers = [
            "Level", "Name", "Casting Time", "Range", "Concentration, Ritual & Required Material", "Notes"
        ]
        self.spell_table.setColumnCount(len(headers))
        self.spell_table.setHorizontalHeaderLabels(headers)
        self.spell_table.verticalHeader().hide()
        self.spell_table.cellDoubleClicked.connect(self.show_spell_details)
        self.spell_table.resizeColumnsToContents()

        self.add_spell_button = QPushButton("Add Spell")
        self.add_spell_button.clicked.connect(self.handle_add_spell)

        self.del_spell_button = QPushButton("Delete Spell")
        self.del_spell_button.clicked.connect(self.handle_delete_spell)

        layout.addWidget(title)
        layout.addWidget(self.spell_table)
        layout.addWidget(self.add_spell_button)
        layout.addWidget(self.del_spell_button)

        return layout

    def handle_delete_spell(self):
        selection = self.spell_table.selectedItems()
        row = self.spell_table.row(selection[-1])
        self.spell_table.removeRow(row)

    def handle_add_spell(self):
        if self.add_spell_popup != None:
            self.add_spell_popup.show()
        spell_selector = SelectOneSpellList()
        all_spells = SpellModel.collection.items()
        spell_selector.populate_spells(all_spells)
        spell_selector.add_spell_signal.connect(self.add_spell)
        spell_selector.show()
        self.add_spell_popup = spell_selector

    def add_spell(self, spell:SpellModel):
        if self.spell_in_table(spell):
            return
        spell_row = SpellRow(spell)
        row = self.spell_table.rowCount()
        self.spell_table.insertRow(row)

        for col, item in enumerate(spell_row.items):
            if isinstance(item, QTableWidgetItem):
                self.spell_table.setItem(row, col, item)
            elif isinstance(item, QWidget):
                self.spell_table.setCellWidget(row, col, item)

        self.spell_table.resizeColumnsToContents()

        self.spell_table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.spell_table.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def spell_in_table(self, spell:SpellModel):
        for l in range(self.spell_table.rowCount()):
            spell_name = self.spell_table.item(l, 1).text()
            if spell_name == spell.name:
                return True

        return False

    def show_spell_details(self, row:int, column:int):
        if column == 5:
            return
        spell_name_item = self.spell_table.item(row, 1)
        if spell_name_item:
            spell_name = spell_name_item.text()
            window = WindowsManager().get_window("spell", spell_name)
            if not window:
                window_class = SpellModel.get_detail_windowclass()
                spell = SpellModel.collection.get_by_field("name", spell_name)
                window = window_class(spell)
                WindowsManager().register_window("spell", spell.name, window)
            window.show()
            window.activateWindow()



class SpellRow:
    def __init__(self, spell: SpellModel):
        self.spell = spell
        self.items = []
        self.create_items()

    def create_items(self):
        level_item = QTableWidgetItem(str(self.spell.level))
        name_item = QTableWidgetItem(self.spell.name)
        cast_time_item = QTableWidgetItem(self.spell.casting_time)
        range_item = QTableWidgetItem(self.spell.range)
        self.crm = self.create_checkbox_widget()
        note_item = QTableWidgetItem()

        self.items = [level_item, name_item, cast_time_item, range_item, self.crm, note_item]

    def create_checkbox_widget(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.checkboxes: list[QCheckBox] = []
        for i in range(3):
            cb = QCheckBox()
            cb.setEnabled(False)
            layout.addWidget(cb)
            layout.addWidget(QLabel(["C","R","M"][i]))
            self.checkboxes.append(cb)

        self.checkboxes[0].setChecked(self.spell.concentration)
        self.checkboxes[1].setChecked(self.spell.ritual)
        self.checkboxes[2].setChecked(self.spell.has_material_component())

        widget.setLayout(layout)
        return widget