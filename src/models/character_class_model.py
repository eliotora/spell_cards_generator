from dataclasses import dataclass
from collections.abc import Callable
from PySide6.QtCore import Signal
from src.models.conceptual_models import Dice, Saving_Throw, Ability, Caracteristic
from src.models.item_model import Item
from enum import Enum
from math import floor
from pyparsing import Word, alphas, alphanums, Group, Forward, oneOf, Suppress

from src.models.spell_model import SpellModel


class SpellSlotEvolution(Enum):
    FULLCASTER = {
        1: {1: 2},
        2: {1: 3},
        3: {1: 4, 2: 2},
        4: {1: 4, 2: 3},
        5: {1: 4, 2: 3, 3: 2},
        6: {1: 4, 2: 3, 3: 3},
        7: {1: 4, 2: 3, 3: 3, 4: 1},
        8: {1: 4, 2: 3, 3: 3, 4: 2},
        9: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
        10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
        11: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
        12: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
        13: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
        14: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
        15: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
        16: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
        17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
        18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
        19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
        20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
    }
    HALFCASTER = {
        1: {},
        2: {1:2},
        3: {1:3},
        4: {1:3},
        5: {1:4, 2:2},
        6: {1:4, 2:2},
        7: {1:4, 2:3},
        8: {1:4, 2:3},
        9: {1:4, 2:3, 3:2},
        10: {1:4, 2:3, 3:2},
        11: {1:4, 2:3, 3:3},
        12: {1:4, 2:3, 3:3},
        13: {1:4, 2:3, 3:3, 4:1},
        14: {1:4, 2:3, 3:3, 4:1},
        15: {1:4, 2:3, 3:3, 4:2},
        16: {1:4, 2:3, 3:3, 4:2},
        17: {1:4, 2:3, 3:3, 4:3, 5:1},
        18: {1:4, 2:3, 3:3, 4:3, 5:1},
        19: {1:4, 2:3, 3:3, 4:3, 5:2},
        20: {1:4, 2:3, 3:3, 4:3, 5:2},
    }
    THIRDCASTER = {
        1: {},
        2: {},
        3: {1:2},
        4: {1:3},
        5: {1:3},
        6: {1:3},
        7: {1:4, 2:2},
        8: {1:4, 2:2},
        9: {1:4, 2:2},
        10: {1:4, 2:3},
        11: {1:4, 2:3},
        12: {1:4, 2:3},
        13: {1:4, 2:3, 3:2},
        14: {1:4, 2:3, 3:2},
        15: {1:4, 2:3, 3:2},
        16: {1:4, 2:3, 3:3},
        17: {1:4, 2:3, 3:3},
        18: {1:4, 2:3, 3:3},
        19: {1:4, 2:3, 3:3, 4:1},
        20: {1:4, 2:3, 3:3, 4:1},
    }
    WARLOCK = {
        1: {1:1},
        2: {1:2},
        3: {2:2},
        4: {2:2},
        5: {3:2},
        6: {3:2},
        7: {4:2},
        8: {4:2},
        9: {5:2},
        10: {5:2},
        11: {5:3},
        12: {5:3},
        13: {5:3},
        14: {5:3},
        15: {5:3},
        16: {5:3},
        17: {5:4},
        18: {5:4},
        19: {5:4},
        20: {5:4},
    }

@dataclass
class ClassFeature:
    name: str
    description: str


@dataclass
class ClassFeatureWithUses:
    max_uses: int
    current_uses: int
    max_uses_func: Callable
    on_short_rest: Signal
    on_long_rest: Signal

    def add_uses(self, uses_to_add:int):
        self.current_uses = self.current_uses + uses_to_add if self.current_uses + uses_to_add <= self.max_uses else self.max_uses

    def set_uses(self, uses:int):
        self.current_uses = uses if uses <= self.max_uses else self.max_uses

    def set_uses_to_max(self):
        self.current_uses = self.max_uses

@dataclass
class SpellCastingFeature:
    spell_slot_evolution: SpellSlotEvolution
    max_minor_spells: dict[int,int]
    spellcasting_carac : Caracteristic.Caracteristics
    spellcasting_focus_type: str
    max_spell_nbr : Callable
    spell_filter : Callable


class MaxSpellNbr(Enum):
    def _lvlplusmod(carac: Caracteristic) -> Callable[[int], int]:
        return lambda lvl: lvl + carac.getMod()

    def _halflvlplusmod(carac: Caracteristic) -> Callable[[int], int]:
        return lambda lvl: lvl//2 + carac.getMod()

    def _spellperlevel(evol: dict[int, int]):
        return lambda lvl: evol.get(lvl)

    SpellPerLevel = _spellperlevel
    LevelPlusMod = _lvlplusmod
    HalfLevelPlusMod = _halflvlplusmod

def spell_filter_factory(filter: dict[str, dict|str]) -> Callable[[SpellModel], bool]:
    """
    json in ast format to boolean function
    ex:

    """
    node_type = filter["type"]

    class ComparatorEnum(Enum):
        class wrapper:
            def __init__(self, f):
                self.f = f

            def __call__(self, *args, **kwargs):
                return self.f(*args, **kwargs)
        EQ = wrapper(lambda x,y : x.__eq__(y))
        LT = wrapper(lambda x,y : x.__lt__(y))
        LE = wrapper(lambda x,y : x.__le__(y))
        GT = wrapper(lambda x,y : x.__gt__(y))
        GE = wrapper(lambda x,y : x.__ge__(y))
        IN = wrapper(lambda x,y : x in y)

    if node_type == "compare":
        print(filter["compare_type"], ComparatorEnum[filter["compare_type"]], filter["key"], filter["value"])
        compare_fun = ComparatorEnum[filter["compare_type"]].value
        key = filter["key"]
        value = filter["value"]
        if SpellModel.__annotations__[key] == list:
            return lambda ctx: any([compare_fun(e, value) for e in getattr(ctx, key)])
        else:
            return lambda ctx: compare_fun(getattr(ctx, key), value)

    if node_type == "NOT":
        inner_fun = spell_filter_factory(filter["value"])
        return lambda ctx: not inner_fun(ctx)

    if node_type == "AND":
        left_fun = spell_filter_factory(filter["left"])
        right_fun = spell_filter_factory(filter["right"])
        return lambda ctx: left_fun(ctx) and right_fun(ctx)

    if node_type == "OR":
        left_fun = spell_filter_factory(filter["left"])
        right_fun = spell_filter_factory(filter["right"])
        return lambda ctx: left_fun(ctx) or right_fun(ctx)

# 2 aspects: Liste des choix pour préparer / liste des choix pour apprendre
# Nombre de sorts max
# Spell Connus / lvl: Barde, Ensorceleur, Occultiste, Rôdeur, Rodeur (arcanique), Guerrier (occulte)
# Spell préparé par sous class hors max
# List étendue par sous classe
# Mod + Niveau : Clerc, Druide, Magicien
# Mod + Niveau/2 (round down): Artificier, Paladin
# Grimoire


@dataclass
class CharacterClass:
    name: str
    health_dice: Dice
    profiencies: list[str]
    saving_throws_profiencies: list[Caracteristic.Caracteristics]
    skills_profiencies_choice: tuple[int, list[Ability]]
    starting_equipement: list[list[Item]]
    class_features: dict[int, list[ClassFeature]]


