from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
from game_map import GameMap
import entity_factory
import tile_types

import tcod

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Returns the center of the room as (x, y) coordinates"""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.x2) / 2)