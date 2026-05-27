from PySide6.QtCore import QObject, Signal
import enum
from .conceptual_models import Distance, Caracteristic, Ability, Saving_Throw, MoneyUnit
from .item_model import Weapon, Item, MagicItem
from .character_class_model import CharacterClass, ClassFeature

from src.models.feat_model import FeatModel

def create_dynamic_model(class_name: str, attributes: dict):
    namespace = {}

    for name, typ in attributes.items():
        private_name = f"_{name}"
        signal_name = f"{name}_changed"

        namespace[signal_name] = Signal(typ)

        def getter(self):
            return getattr(self, private_name)

        def setter(self, value):
            if value != getattr(self, private_name):
                setattr(self, private_name, value)
                getattr(self, signal_name).emit(value)

        namespace[name] = property(getter, setter)

    return type(class_name, (QObject,), namespace)

from typing import TypeVar, Generic

T = TypeVar("T")


class signaledProperty(QObject, Generic[T]):
    changed = Signal(object)

    def __init__(self, value: T = None):
        super().__init__()
        self._value: T = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        if new_value != self._value:
            self._value = new_value
            self.changed.emit(new_value)

    def __repr__(self):
        return f"Parameter({self._value!r})"


class Character(QObject):
    _proficiencies = [0] + [2 for _ in range(1,5)] + [3 for _ in range(5,9)] + [4 for _ in range(9,13)] + [5 for _ in range(13,17)] + [6 for _ in range(17,21)]

    def __init__(
        self,
        name: str = "",
        background: str = "",
        char_class: str = "",
        species: str = "",
        subclass: str = "",
        lvl: int = 1,
        xp: int = 0,
        armor_class: int = 10,
        shield: bool = False,
        current_hit_points: int = 1,
        temp_hit_points: int = 0,
        max_hit_points: int = 1,
        hit_dice_type: str = "d6",
        spent_hit_dice: int = 0,
        death_saves: list[bool] = [],
        caracs: dict[Caracteristic.Caracteristics, Caracteristic] = None,
        proficiencies: dict[str, bool] = {a: False for a in Ability.Abilities},
        speeds: list[Distance] = Distance(9, "m"),
        size: str = "M",
        inspiration: bool = False,
        trainings: signaledProperty[dict[str]] = {},
        class_features: list[str] = [],
        species_traits: list[str] = [],
        feats: list[FeatModel] = [],
        appearance: str = "",
        backstory_personnality: str = "",
        languages: list[str] = [],
        equipement: list[Item] = [],
        attunements: list[MagicItem] = [],
        money: dict[MoneyUnit, int] = {m : 0 for m in MoneyUnit}
    ):
        super().__init__()

        self.name = signaledProperty[str](name)
        self.background = signaledProperty[str](background)
        self.char_class = signaledProperty[CharacterClass](char_class)
        self.species = signaledProperty[str](species)
        self.subclass = signaledProperty[str](subclass)
        self.lvl = signaledProperty[int](lvl)
        self.proficiency_bonus = signaledProperty[int](self._proficiencies[lvl])
        self.xp = signaledProperty[int](xp)
        self.armor_class = signaledProperty[int](armor_class)
        self.shield = signaledProperty[bool](shield)
        self.current_hit_points = signaledProperty[int](current_hit_points)
        self.temp_hit_points = signaledProperty[int](temp_hit_points)
        self.max_hit_points = signaledProperty[int](max_hit_points)
        self.max_hit_dice = signaledProperty[int](
            self.lvl
        )  # Nbr of max hit dices is the total level of character
        self.hit_dice_type = signaledProperty[int](hit_dice_type)
        self.spent_hit_dice = signaledProperty[int](spent_hit_dice)
        self.death_saves = signaledProperty[list[bool]](death_saves)
        if caracs == None:
            self.caracs = signaledProperty[
                dict[Caracteristic.Caracteristics, Caracteristic]
            ]({c: Caracteristic(c, 10) for c in Caracteristic.Caracteristics})
        else:
            self.caracs = signaledProperty[
                dict[Caracteristic.Caracteristics, Caracteristic]
            ](caracs)
        self.saving_throws = signaledProperty[dict[Caracteristic.Caracteristics, Saving_Throw]](
            {
                k: Saving_Throw(c, proficiencies.get(f"{c.name} Saving Throw", False))
                for k,c in self.caracs.value.items()
            }
        )
        self.abilities = signaledProperty[dict[Ability.Abilities, Ability]](
            {
                a: Ability(a.value[1], self.caracs.value[a.value[0]], proficiencies[a])
                for a in Ability.Abilities
            }
        )
        self.caracs.value[Caracteristic.Caracteristics.DEXTERITY].valueChanged.emit(
            self.caracs.value[Caracteristic.Caracteristics.DEXTERITY].getValue(),
            self.caracs.value[Caracteristic.Caracteristics.DEXTERITY].getMod()
        )

        self.speeds = signaledProperty[list[Distance]](speeds)
        self.size = signaledProperty[str](size)
        self.inspiration = signaledProperty[bool](inspiration)

        self.trainings: signaledProperty[dict[str]] = trainings
        self.class_features: list[ClassFeature] = class_features
        self.species_traits: list[signaledProperty[str]] = species_traits
        self.feats : list[signaledProperty[FeatModel]] = feats

        # SpellCasting TODO

        # Appearance and others
        self.appearance: signaledProperty[str] = appearance
        self.backstory_personnality: signaledProperty[str] = backstory_personnality
        self.languages: signaledProperty[list[str]] = languages
        self.equipement: signaledProperty[list[Item]] = equipement

        self.maximum_attunements: signaledProperty[int] = 3
        self.attunements: signaledProperty[list[MagicItem]] = attunements


        money = {k: signaledProperty(i) for k, i in money.items()}
        self.money: dict[MoneyUnit, signaledProperty[int]] = money

        self._setSignals()

    def _setSignals(self):
        self.shield.changed.connect(lambda shield: self.setArmorClass(self.armor_class.value + 2 if shield else self.armor_class.value - 2))
        self.lvl.changed.connect(lambda lvl: self.setProficiencyBonus(self._proficiencies[lvl]))
        self.lvl.changed.connect(self.update_hit_dice)
        self.caracs.value[Caracteristic.Caracteristics.DEXTERITY].connectOnValueChanged(self.setInitiative)

    def setInitiative(self, value: int):
        self.initiative = value

    def update_hit_dice(self, lvl: int):
        self.max_hit_dice.value = lvl

    def setLvl(self, lvl: int) -> None:
        self.lvl.value = int(lvl)

    def setShield(self, shield: bool):
        self.shield.value = shield

    def setName(self, name: str):
        self.name.value = name

    def setBackground(self, background: str):
        self.background.value = background

    def setClass(self, char_class: str):
        self.char_class.value = char_class

    def setSpecies(self, species: str):
        self.species.value = species

    def setSubclass(self, subclass: str):
        self.subclass.value = subclass

    def setXp(self, xp: int):
        self.xp.value = xp

    def setArmorClass(self, ac: int):
        self.armor_class.value = ac

    def setCurrentHitPoints(self, hp: int):
        self.current_hit_points.value = hp

    def setTempHitPoints(self, temp_hp: int):
        self.temp_hit_points.value = temp_hp

    def setMaxHitPoints(self, max_hp: int):
        self.max_hit_points.value = max_hp

    def setMaxHitDice(self, max_dice: int):
        self.max_hit_dice.value = max_dice

    def setSpentHitDice(self, spent: int):
        self.spent_hit_dice.value = spent

    # TODO: Death saves
    def setProficiencyBonus(self, bonus: int):
        self.proficiency_bonus.value = bonus

    def setInitiative(self, value:int , mod: int):
        self.initiative = mod

    def setSpeeds(self, speed: str):
        self.speeds = [
            Distance(s.split(" ")[0], s.split(" ")[1]) for s in speed.split(", ")
        ]

    def setSize(self, size: str):
        self.size = size

    def setInspiration(self, inspiration:bool):
        self.inspiration.value = inspiration

    def computeArmorClass(self):
        ac = 10 + self.caracs.value[Caracteristic.Caracteristics.DEXTERITY].getMod()
        if self.shield.value == True: ac += 2
        self.setArmorClass(ac)

    def isProficientWith(self, item:Weapon): #TODO: Tools and Armor
        types = item.type
        for t in types:
            if t in self.trainings:
                return self.trainings[t].value

        if item.name in self.trainings:
            return self.trainings[t].value

        return False