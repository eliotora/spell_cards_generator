def modificator_from_stat(val: int):
    return  (val - 10) // 2


class Caracteristic(int):
    name:str
    score:int
    mod:int

    def __init__(self, name:str, val:int):
        self.name = name
        self.score = val
        self.mod = modificator_from_stat(val)

class Ability:
    name:str
    carac:Caracteristic
    proficient:bool

    def __init__(self, name:str, carac:Caracteristic, proficient:bool):
        self.name = name
        self.carac = carac
        self.proficient = proficient

    def get_mod(self, profiency_bonus) -> int:
        return self.carac.mod + profiency_bonus if self.proficient else self.carac.mod

    def get_passive_value(self, proficency_bonus) -> int:
        return 10 + self.get_mod(proficency_bonus)

class Saving_Throw(Ability):
    def __init__(self, carac:Caracteristic, proficient:bool):
        super().__init__(f"{carac.name} Saving Throw", carac, proficient)

class Distance:
    value: float
    unit: str

    def __init__(self, value:float, unit:str):
        self.value = value
        self.unit = unit

class Character:
    # Top part
    name:str
    background:str
    char_class:str
    species:str
    subclass:str
    lvl:int
    xp:int
    armor_class:int
    shield:bool
    current_hit_points:int
    temp_hit_points:int
    temp_hit_points_source:str
    max_hit_points:int
    max_hit_dice:int
    hit_dice_type:str
    spent_hit_dice:int
    death_saves:list[bool]

    # Stats
    proficiency_bonus:int
    caracs: list[Caracteristic]
    saving_throws: list[Saving_Throw]
    abilities: list[Ability]
    initiative: int
    speeds: list[Distance]
    size: str
    # passive_perception:

    