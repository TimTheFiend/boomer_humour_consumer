from __future__ import annotations

from typing import Iterable, Iterator, Optional, Tuple, TYPE_CHECKING
import random
import numpy as np
from tcod.console import Console

# TODO TEMP
from components.tile_types import floor, temp
from constants import (
    CONSOLE_WIDTH,
    CONSOLE_HEIGHT,
)


from entity import Actor, Item

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
        self,
        engine: Engine,
        width: int,
        height: int,
        entities: Iterable[Entity] = (),
    ):
        self.engine = engine
        self.width = width
        self.height = height

        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=floor, order='F')  # TODO TEMP
        for x, line in enumerate(self.tiles):
            for y, cell in enumerate(line):
                if random.random() < 0.1:
                    self.tiles[x, y] = temp
        # self.tiles = np.full((width, height), fill_value=None, order='F')

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor)
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Item) and entity.is_alive
        )

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == x
                and entity.y == y
            ):
                return entity
        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['light']

        entities_sorted = sorted(self.entities, key=lambda x: x.render_order.value)
        for entity in entities_sorted:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    def render_center(self, console: Console, player_pos: Tuple[int, int]) -> None:
        x, y = player_pos
        x1 = x2 = y1 = y2 = 0
        HALF_WIDTH = int(CONSOLE_WIDTH / 2)
        HALF_HEIGHT = int(CONSOLE_HEIGHT / 2)

        player_x = 0
        player_y = 0

        # player_y = 0

        if 0 <= x <= HALF_WIDTH:
            x1 = 0  # The player is close to the left-most wall
            x2 = CONSOLE_WIDTH  # The player is close to the left-most wall
        elif (self.width - HALF_WIDTH) <= x <= self.width:
            x1 = self.width - CONSOLE_WIDTH  # The player is close to the rightmost wall
            x2 = self.width
            player_x = self.width - CONSOLE_WIDTH
        else:
            x1 = x - HALF_WIDTH
            x2 = x + HALF_WIDTH
            player_x = x - HALF_WIDTH

            # player_y = max(0, y - (y - HALF_HEIGHT))
            # player_x = x - HALF_WIDTH

        if 0 <= y <= HALF_HEIGHT:
            y1 = 0  # The player is close to the left-most wall
            y2 = CONSOLE_HEIGHT  # The player is close to the left-most wall
        elif (self.height - HALF_HEIGHT) <= y <= self.height:
            y1 = self.height - CONSOLE_HEIGHT  # The player is close to the rightmost wall
            y2 = self.height
            player_y = self.height - CONSOLE_HEIGHT
        else:
            y1 = y - HALF_HEIGHT
            y2 = y + HALF_HEIGHT
            player_y = y - HALF_HEIGHT

        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['light'][x1:x2, y1:y2]


        entities_sorted = sorted(self.entities, key=lambda _x: _x.render_order.value)
        for entity in entities_sorted:
            console.print(x=entity.x - player_x, y=entity.y - player_y, string=entity.char, fg=(255, 0, 0))
            # console.print(x=entity.x - player_x, y=entity.y - player_y, string=entity.char, fg=entity.color)