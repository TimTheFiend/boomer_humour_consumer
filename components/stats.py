from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from components.base_component import BaseComponent
from components.dice import Dice, Roll
from constants import BASE_HP
from data.render_order import RenderOrder

import tcod

if TYPE_CHECKING:
    from entity import Actor


class Stats(BaseComponent):
    """`Actor` character stats.

    Ability properties are in all-caps because the normal abbreviation of `Strength` is the same as python's `String` type.
    """
    parent: Actor

    agility: int
    charisma: int
    constitution: int
    intelligence: int
    perception: int
    strength: int
    wisdom: int

    def __init__(
            self,
            *,
            stats: Dict
    ):
        for key, value in stats.items():
            setattr(self, key, value)


        # If the `Actor` is level 1, set min. max_hp as normal
        self.max_hp = BASE_HP + (self.CON * 2)

        self._hp = self.max_hp

    # region HP related
    @property
    def hp(self) -> int: return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

    # endregion HP Related

    # region Ability Properties
    @property
    def AGI(self) -> int: return self.agility

    @property
    def CHR(self) -> int: return self.charisma

    @property
    def CON(self) -> int: return self.constitution

    @property
    def INT(self) -> int: return self.intelligence

    @property
    def PER(self) -> int: return self.perception

    @property
    def STR(self) -> int: return self.strength

    @property
    def WIS(self) -> int: return self.wisdom
    # endregion Properties