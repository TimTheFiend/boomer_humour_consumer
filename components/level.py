from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from components.dice import Dice, Roll

if TYPE_CHECKING:
    from entity import Actor
    from components.stats import Stats


class Level(BaseComponent):
    parent: Actor

    def __init__(
        self,
        level: int = 1,
        exp: int = 0,
        level_up_base: int = 0,  # Todo better naming
        level_up_factor: int = 0,  # todo better naming
        exp_gained: int = 0,
    ):
        self.level = level
        self.exp = exp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.exp_gained = exp_gained

    @property
    def exp_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        return self.exp > self.exp_to_next_level
        # TODO better naming

    def gain_exp(self, value: int) -> None:
        # todo
        pass

    def level_up(self) -> None:
        self.exp -= self.exp_to_next_level
        self.level += 1

    # TODO make better
    def ability_increase_agility(self, modifier: Dice) -> None:
        value = Roll.roll(modifier)
        print(f"Agility increased by {value}")
        self.parent.stats.agility += value