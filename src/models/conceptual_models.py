from PySide6.QtCore import Signal, QObject
import enum
from dataclasses import dataclass
from typing import Optional

class Dice(enum.StrEnum):
    D4 = "d4"
    D6 = "d6"
    D8 = "d8"
    D10 = "d10"
    D12 = "d12"
    D20 = "d20"
    D100 = "d100"

@dataclass
class Distance:
    value: float
    unit: str

    def __str__(self) -> str:
        if int(self.value) == self.value:
            return f"{self.value} {self.unit}"
        else:
            return f"{round(self.value, 3)} {self.unit}"

class WeaponPropertyType(enum.Enum):
    AMMUNITION = enum.auto()
    FINESSE = enum.auto()
    HEAVY = enum.auto()
    LIGHT = enum.auto()
    LOADING = enum.auto()
    REACH = enum.auto()
    SPECIAL = enum.auto()
    THROWN = enum.auto()
    TWO_HANDED = enum.auto()
    VERSATILE = enum.auto()

class WeaponType(enum.Enum):
    MELEE = enum.auto()
    RANGED = enum.auto()

@dataclass
class WeaponProperty:
    type: WeaponPropertyType
    ammunition_type: Optional[str] = None
    range_normal: Optional[Distance] = None
    range_max: Optional[Distance] = None
    special_text: Optional[str] = None
    versatile_damage: Optional[Dice] = None

    def describe(self) -> str:
        """Return a textual description of the property"""
        match self.type:
            case WeaponPropertyType.AMMUNITION:
                return f"munitions (portée {self.range_normal}/{self.range_max})"
            case WeaponPropertyType.SPECIAL:
                return f"spécial"
            case WeaponPropertyType.THROWN:
                return f"lancer (portée {self.range_normal}/{self.range_max})"
            case WeaponPropertyType.VERSATILE:
                return f"versatile ({self.versatile_damage})"
            case _:
                return f"{self.type.name.lower()}"

    def __str__(self) -> str:
        return self.describe()

class MoneyUnit(enum.Enum):
    PLATINIUM=({"en":"pp", "fr":"pp"},1000)
    GOLD=({"en":"gp", "fr":"po"},100)
    ELECTRUM=({"en":"ep", "fr":"pe"},50)
    SILVER=({"en":"sp", "fr":"pa"},10)
    COPPER=({"en":"cp", "fr":"pc"},1)

    def get_unit_from_text(cls, text) -> 'MoneyUnit':
        for u in cls:
            if text in u[0]:
                return u
        return None

class Caracteristic(QObject):
    class Caracteristics(enum.StrEnum):
        STRENGTH = "STRENGTH"
        DEXTERITY = "DEXTERITY"
        CONSTITUTION = "CONSTITUTION"
        INTELLIGENCE = "INTELLIGENCE"
        WISDOM = "WISDOM"
        CHARISMA = "CHARISMA"

    valueChanged = Signal(int, int)

    def __init__(self, name: str, val: int):
        super().__init__()
        self.name: str = name
        self.score: int = val
        self.mod: int = self.modificator_from_stat(val)

    def modificator_from_stat(self, val: int):
        return (val - 10) // 2

    def setValue(self, value: int) -> None:
        self.score = value
        self.mod = self.modificator_from_stat(self.score)
        self.valueChanged.emit(self.score, self.mod)

    def getValue(self) -> int:
        return self.score

    def getMod(self) -> int:
        return self.mod

    def connectOnValueChanged(self, fct):
        self.valueChanged.connect(fct)

class Ability(QObject):
    class Abilities(enum.Enum):
        Athletics = (Caracteristic.Caracteristics.STRENGTH, "Athletics")
        Acrobatics = (Caracteristic.Caracteristics.DEXTERITY, "Acrobatics")
        Sleight_of_Hand = (Caracteristic.Caracteristics.DEXTERITY, "Sleight of Hand")
        Stealth = (Caracteristic.Caracteristics.DEXTERITY, "Stealth")
        Arcana = (Caracteristic.Caracteristics.INTELLIGENCE, "Arcana")
        History = (Caracteristic.Caracteristics.INTELLIGENCE, "History")
        Investigation = (Caracteristic.Caracteristics.INTELLIGENCE, "Investigation")
        Nature = (Caracteristic.Caracteristics.INTELLIGENCE, "Nature")
        Religion = (Caracteristic.Caracteristics.INTELLIGENCE, "Religion")
        Animal_Handling = (Caracteristic.Caracteristics.WISDOM, "Animal Handling")
        Insight = (Caracteristic.Caracteristics.WISDOM, "Insight")
        Medicine = (Caracteristic.Caracteristics.WISDOM, "Medicine")
        Perception = (Caracteristic.Caracteristics.WISDOM, "Perception")
        Survival = (Caracteristic.Caracteristics.WISDOM, "Survival")
        Deception = (Caracteristic.Caracteristics.CHARISMA, "Deception")
        Intimidation = (Caracteristic.Caracteristics.CHARISMA, "Intimidation")
        Perfomance = (Caracteristic.Caracteristics.CHARISMA, "Perfomance")
        Persuasion = (Caracteristic.Caracteristics.CHARISMA, "Persuasion")

        @classmethod
        def abilities_by_carac(cls, carac: Caracteristic.Caracteristics):
            return [a for a in cls if a.value[0] == carac]

    onModifierChanged = Signal()

    def __init__(self, name: str, carac: Caracteristic, proficient: bool):
        super().__init__()
        self.name: str = name
        self.carac: Caracteristic = carac
        self.proficient: bool = proficient
        self.carac.valueChanged.connect(lambda value: self.onModifierChanged.emit())

    def get_mod(self, profiency_bonus) -> int:
        return self.carac.mod + profiency_bonus if self.proficient else self.carac.mod

    def get_passive_value(self, proficency_bonus) -> int:
        return 10 + self.get_mod(proficency_bonus)

    def setProficient(self, proficient: bool) -> None:
        self.proficient = proficient
        self.onModifierChanged.emit()

class Saving_Throw(Ability):
    def __init__(self, carac: Caracteristic, proficient: bool):
        super().__init__(f"Saving Throw", carac, proficient)


if __name__ == "__main__":
    dist = Distance(7.50, "m")
    print(f"Distance test: {dist}")
    assert dist.__str__() == "7.5 m"

    dist2 = Distance(3, "m")
    print(f"Distance test 2: {dist2}")
    assert dist2.__str__() == "3 m"

    w_prop = WeaponProperty(
        type=WeaponPropertyType.AMMUNITION,
        ammunition_type="arrows"
    )
    for type in WeaponPropertyType:
        ammunition_type = None
        range_normal = None
        range_max = None
        special_text = None
        versatile_damage = None

        match type:
            case WeaponPropertyType.AMMUNITION:
                ammunition_type = "arrows"
                range_normal = Distance(30, "m")
                range_max = Distance(90, "m")
            case WeaponPropertyType.SPECIAL:
                special_text = "Text spéciale pour arme"
            case WeaponPropertyType.THROWN:
                range_normal = Distance(6, "m")
                range_max = Distance(18, "m")
            case WeaponPropertyType.VERSATILE:
                versatile_damage = Dice.D10
        w_prop = WeaponProperty(
            type=type,
            ammunition_type=ammunition_type,
            range_normal=range_normal,
            range_max=range_max,
            special_text=special_text,
            versatile_damage=versatile_damage
        )
        print(w_prop)

