"""All things related to Dice rolling is in this file.

`Dice` is an Enum that contains the different type of commonly used dice used in RPGS,
while `Roll` contains the methods needed for rolling the `Dice`.
"""
from __future__ import annotations

from enum import Enum
from random import randint
from typing import List, Tuple

class Dice(Enum):
    """Enum that holds the different types of dice that are commonly used in tabletop RPGs."""
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20

class Roll:
    @staticmethod
    def roll(die: Dice, no_of_dice: int = 1) -> int:
        """Rolls the selected `Dice`-type, `no_of_dice` (default 1) number of times, and returns the total sum."""
        rolls_value = 0
        for i in range(no_of_dice):
            rolls_value += randint(1, die.value)

        return rolls_value

    @staticmethod
    def roll_multiple(dice_and_no_rolls: Tuple[Tuple[Dice, int]]) -> int:
        """Rolls multiple `Dice` `x` number of times, and returns the total sum of all rolls.

        Ex. `Roll.roll_multiple(((Dice.D20, 4), (Dice.D8, 2)))`
        """
        rolls_value = 0

        for roll in dice_and_no_rolls:
            die, no_of_dice = roll
            rolls_value += Roll.roll(die, no_of_dice)
        return rolls_value

    @staticmethod
    def roll_percentage():
        """Rolls two `D10`s that returns a value between 1, and 100.

        One die is multiplied with 10 to use as `tens`(Die result 1 is between 0-9, 2 = 10-19, [..] and 9 = 90-99)
        The other is the digit in the `ones` position, which is always between 1, and 10.

        The two results are then added together, `1` is subtracted from `tens` so we can get numbers between 0-9, multiplied with ten
        and added with `ones` to get a percentage roll.
        100 is the highest value, achieved by getting two `10` results, 1 being the lowest by getting two `1`s.
        """
        tens = randint(1, Dice.D10.value)
        ones = randint(1, Dice.D10.value)
        return (tens - 1) * 10 + ones

for i in range(3):
    Roll.roll_percentage()