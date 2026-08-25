from dataclasses import dataclass
import enum
from typing import Union

from src.models.base.translated_text import TranslatedText

class Dice(enum.StrEnum):
    D4 = "d4"
    D6 = "d6"
    D8 = "d8"
    D10 = "d10"
    D12 = "d12"
    D20 = "d20"
    D100 = "d100"

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

class MoneyQuantity:
    def __init__(self, quantity: float, base_unit: MoneyUnit = MoneyUnit.COPPER):
        self.quantity = int(quantity * base_unit.value[1])

    def __str__(self) -> str:
        for unit in sorted(MoneyUnit, key=lambda x: x.value[1], reverse=True):
            if self.quantity % unit.value[1] == 0:
                return f"{self.quantity // unit.value[1]} {unit.value[0]["fr"]}"
        return f"{self.quantity} {MoneyUnit.COPPER.value[0]["fr"]}"

    def __eq__(self, other: 'MoneyQuantity'):
        return self.quantity == other.quantity

    def __add__(self, other: Union[int,'MoneyQuantity']):
        if isinstance(other, MoneyQuantity):
            return MoneyQuantity(self.quantity + other.quantity)
        elif isinstance(other, int):
            return MoneyQuantity(self.quantity + other)
        else:
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__.__name__} and {other.__class__.__name__}")


class Caracteristic(enum.Enum):
    STR = TranslatedText(by_lang={"fr": "Force", "en": "Strength"})
    DEX = TranslatedText(by_lang={"fr": "Dextérité", "en": "Dexterity"})
    CON = TranslatedText(by_lang={"fr": "Constitution", "en": "Constitution"})
    INT = TranslatedText(by_lang={"fr": "Intelligence", "en": "Intelligence"})
    WIS = TranslatedText(by_lang={"fr": "Sagesse", "en": "Wisdom"})
    CHA = TranslatedText(by_lang={"fr": "Charisme", "en": "Strength"})

@dataclass
class CaracteristicInstance:
    carac: Caracteristic
    value: int

    def __str__(self) -> str:
        return f"{self.carac.value.for_lang("fr")}: {self.value}"

    def __lt__(self, other: Union["CaracteristicInstance", int]):
        if isinstance(other, self.__class__):
            other_v = other.value
        else:
            other_v = other

        return self.value < other_v

    def get_value(self) -> int:
        return self.value

    def carac_text(self) -> str:
        return self.carac.value.for_lang("fr")

    @property
    def mod(self) -> int:
        return (self.value - 10) // 2


class Skills(enum.Enum): # TODO: Rendre dynamique? Ajout sourcé de Skill?
    @dataclass
    class Skill:
        name: TranslatedText
        carac: Caracteristic

    Acrobatics=Skill(name=TranslatedText(by_lang={"fr": "Acrobaties", "en": "Acrobatics"}), carac=Caracteristic.DEX)
    AnimalHandling=Skill(name=TranslatedText(by_lang={"fr": "Dressage", "en": "Animal Handling"}), carac=Caracteristic.WIS)
    Arcana=Skill(name=TranslatedText(by_lang={"fr": "Arcane", "en": "Arcana"}), carac=Caracteristic.INT)
    Athletics=Skill(name=TranslatedText(by_lang={"fr": "Athlétisme", "en": "Athletics"}), carac=Caracteristic.STR)
    Deception=Skill(name=TranslatedText(by_lang={"fr": "Tromperie", "en": "Deception"}), carac=Caracteristic.CHA)
    History=Skill(name=TranslatedText(by_lang={"fr": "Histoire", "en": "History"}), carac=Caracteristic.INT)
    Insight=Skill(name=TranslatedText(by_lang={"fr": "Intuition", "en": "Insight"}), carac=Caracteristic.WIS)
    Intimidation=Skill(name=TranslatedText(by_lang={"fr": "Intimidation", "en": "Intimidation"}), carac=Caracteristic.CHA)
    Investigation=Skill(name=TranslatedText(by_lang={"fr": "Investigation", "en": "Investigation"}), carac=Caracteristic.INT)
    Medicine=Skill(name=TranslatedText(by_lang={"fr": "Médecine", "en": "Medicine"}), carac=Caracteristic.WIS)
    Nature=Skill(name=TranslatedText(by_lang={"fr": "Nature", "en": "Nature"}), carac=Caracteristic.INT)
    Perception=Skill(name=TranslatedText(by_lang={"fr": "Perception", "en": "Perception"}), carac=Caracteristic.WIS)
    Performance=Skill(name=TranslatedText(by_lang={"fr": "Performance", "en": "Performance"}), carac=Caracteristic.CHA)
    Persuasion=Skill(name=TranslatedText(by_lang={"fr": "Persuasion", "en": "Persuasion"}), carac=Caracteristic.CHA)
    Religion=Skill(name=TranslatedText(by_lang={"fr": "Religion", "en": "Religion"}), carac=Caracteristic.INT)
    SleightofHand=Skill(name=TranslatedText(by_lang={"fr": "Escamotage", "en": "Sleight of Hand"}), carac=Caracteristic.DEX)
    Stealth=Skill(name=TranslatedText(by_lang={"fr": "Discrétion", "en": "Stealth"}), carac=Caracteristic.DEX)
    Survival=Skill(name=TranslatedText(by_lang={"fr": "Survie", "en": "Survival"}), carac=Caracteristic.WIS)
