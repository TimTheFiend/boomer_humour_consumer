from __future__ import annotations

from typing import Iterable, Iterator, Optional, Tuple, TYPE_CHECKING
import random
import numpy as np
from tcod.console import Console


# TODO TEMP
from components.tile_types import floor, wall, ground, tree1, shallow_water
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

        self.tiles = np.full((width, height), fill_value=tree1, order='F')  # TODO TEMP

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
        """Render functions which follows the player.

        The player will always be at the center, except at the edges of the map.

        x_pos and y_pos is used to adjust for printing entities on console.

        args:
        player_pos = player position on the game map (x, y)
        """
        x, y = player_pos
        left_render = right_render = top_render = bottom_render = 0
        HALF_WIDTH = int(CONSOLE_WIDTH / 2)
        HALF_HEIGHT = int(CONSOLE_HEIGHT / 2)

        x_pos = 0
        y_pos = 0

        if 0 <= x <= HALF_WIDTH:
            # If the player is at the left-most wall
            left_render = 0  
            right_render = CONSOLE_WIDTH  
        elif (self.width - HALF_WIDTH) <= x <= self.width:
            # If the player is at the right-most wall
            left_render = self.width - CONSOLE_WIDTH  
            right_render = self.width
            x_pos = self.width - CONSOLE_WIDTH
        else:
            # If the player is in between values above
            left_render = x - HALF_WIDTH
            right_render = x + HALF_WIDTH
            x_pos = x - HALF_WIDTH

        if 0 <= y <= HALF_HEIGHT:
            # If the player is at the top wall
            top_render = 0  
            bottom_render = CONSOLE_HEIGHT  
        elif (self.height - HALF_HEIGHT) <= y <= self.height:
            # If the player is at the bottom wall
            top_render = self.height - CONSOLE_HEIGHT
            bottom_render = self.height
            y_pos = self.height - CONSOLE_HEIGHT
        else:
            # If the player is in between the values above
            top_render = y - HALF_HEIGHT
            bottom_render = y + HALF_HEIGHT
            y_pos = y - HALF_HEIGHT
        # print(len(self.tiles))

        
        console.tiles_rgb[0:CONSOLE_WIDTH, 0:CONSOLE_HEIGHT] = self.tiles['light'][left_render : right_render, top_render : bottom_render]


        # for x in range(self.width):
        #     for y in range(self.height):
        #         console.print(x, y, string=self.tiles[x, y].char, fg=(255,255,255))

        entities_sorted = sorted(self.entities, key=lambda _x: _x.render_order.value)
        for entity in entities_sorted:
            console.print(x=entity.x - x_pos, y=entity.y - y_pos, string=entity.char, fg=(255, 0, 0))
            # console.print(x=entity.x - player_x, y=entity.y - player_y, string=entity.char, fg=entity.color)


