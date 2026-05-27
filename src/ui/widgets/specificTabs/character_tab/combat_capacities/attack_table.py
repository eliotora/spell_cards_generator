from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QPushButton, QTableWidgetItem
from PySide6.QtCore import Qt
from src.models.item_model import Weapon, WeaponType
from src.models.character_model import Character, signaledProperty
from src.models.conceptual_models import Caracteristic, WeaponPropertyType
from src.models.spell_model import SpellModel
class AttackTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.attacks = []
        layout = self.create_layout()
        self.setLayout(layout)

    def create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5,5,5,5)

        label = QLabel("WEAPONS & DAMAGE CANTRIPS")
        self.table = QTableWidget()
        headers = ["Name", "Atk Bonus / DC", "Damages & Type", "Notes"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().hide()
        # self.table.cellDoubleClicked.connect() TODO
        self.table.resizeColumnsToContents

        self.add_attack_button = QPushButton("Add Attack")
        # self.add_attack_button.clicked.connect(self.handle_add_spell)

        self.del_attack_button = QPushButton("Delete Attack")
        # self.del_attack_button.clicked.connect(self.handle_delete_spell)

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.table)
        layout.addWidget(self.add_attack_button)
        layout.addWidget(self.del_attack_button)

        return layout

    def add_attack(self, attack_source:Weapon|SpellModel, char:Character):
        attack_row = AttackRow(attack_source, char)
        self.attacks.append(attack_row)
        row = self.table.rowCount()
        self.table.insertRow(row)

        for col, item in enumerate(attack_row.items):
            self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

    def attack_in_table(self, attack_source:Weapon|SpellModel):
        for r in range(self.table.rowCount()):
            attack_name = self.table.item(r, 1).text()
            if attack_name == attack_source.name:
                return True


class AttackRow:
    def __init__(self, attack_source:Weapon|SpellModel, char:Character):
        self.char = char
        self.items: list[QTableWidgetItem] = []
        self.attack_source = attack_source
        self.makeConnections()

        # Col 1: Name
        name = attack_source.name

        # Col 2 + 3: Bonus / DC + Dmg
        attack_bonus, dmg = self.get_bonus_dmg()

        # Col 4: Notes
        note = "" #TODO

        self.create_items(name, attack_bonus, dmg, note)

    def makeConnections(self):
        if isinstance(self.attack_source, Weapon):
            if self.attack_source.weapon_type == WeaponType.MELEE:
                if any([p.type==WeaponPropertyType.FINESSE for p in self.attack_source.properties]):
                    self.char.caracs.value[Caracteristic.Caracteristics.STRENGTH].connectOnValueChanged(self.onCaracChanged)
                    self.char.caracs.value[Caracteristic.Caracteristics.DEXTERITY].connectOnValueChanged(self.onCaracChanged)
                else:
                    self.char.caracs.value[Caracteristic.Caracteristics.STRENGTH].connectOnValueChanged(self.onCaracChanged)
            elif self.attack_source.weapon_type == WeaponType.RANGED:
                self.char.caracs.value[Caracteristic.Caracteristics.DEXTERITY].connectOnValueChanged(self.onCaracChanged)

    def get_bonus_dmg(self) -> tuple[str, str]:
        if isinstance(self.attack_source, Weapon):
            proficient = True # TODO: Chercher les maîtrises correspondantes
            if self.attack_source.weapon_type == WeaponType.MELEE:
                if any([p.type==WeaponPropertyType.FINESSE for p in self.attack_source.properties]):
                    strengh = self.char.caracs.value[Caracteristic.Caracteristics.STRENGTH]
                    dex = self.char.caracs.value[Caracteristic.Caracteristics.DEXTERITY]
                    carac = strengh if strengh.getValue() > dex.getValue() else dex
                else:
                    carac = self.char.caracs.value[Caracteristic.Caracteristics.STRENGTH]
            elif self.attack_source.weapon_type == WeaponType.RANGED:
                carac = self.char.caracs.value[Caracteristic.Caracteristics.DEXTERITY]

            attack_bonus = carac.getMod()
            if proficient: attack_bonus += self.char.proficiency_bonus.value
            attack_bonus = f"+{attack_bonus}" if attack_bonus >= 0 else str(attack_bonus)

            dmg = f"{self.attack_source.damage_dice[0]}{self.attack_source.damage_dice[1]}{"+" if carac.getMod() >= 0 else ""}{carac.getMod()} {self.attack_source.damage_type}"

        print(attack_bonus, dmg)

        return attack_bonus, dmg

    def create_items(self, name, attack_bonus, dmg, note):
        name_item = QTableWidgetItem(name)
        bonus_dd_item = QTableWidgetItem(attack_bonus)
        dmg_item = QTableWidgetItem(dmg)
        note_item = QTableWidgetItem(note)

        self.items = [name_item, bonus_dd_item, dmg_item, note_item]

    def onCaracChanged(self, value:int, mod:int) -> None:
        attack_bonus, dmg = self.get_bonus_dmg()

        self.items[1].setText(attack_bonus)
        self.items[2].setText(dmg)







