from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from data.render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.stats import Stats
    from components.inventory import Inventory
    from components.level import Level
    from game_map import GameMap

T = TypeVar('T', bound='Entity')

class Entity:
    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = '?',
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = '<Todd Howard>',
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if parent:
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def spawn(self: T, gamemap: GameMap, x: int, y: int):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place entity."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, 'parent'):
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, x: int, y: int) -> None:
        self.x += x
        self.y += y
        print(self.x, self.y)


class Actor(Entity):
    def __init__(
            self,
            *,
            gamemap: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = '?',
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = '<Actor Todd Howard>',
            ai_cls: Type[BaseAI],
            stats: Stats,
            inventory: Inventory,
            # equipment: Equipment,
            # fighter: Fighter,
            level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )
        # Setting `Ai`
        self.ai: Optional[BaseAI] = ai_cls(self)

        # Setting `Stats`
        self.stats = stats
        self.stats.parent = self
        # Setting `Inventory`
        self.inventory = inventory
        self.inventory.parent = self
        # Setting `Level`
        self.level = level
        self.level.parent = self
        # TODO

class Item(Entity):
    pass