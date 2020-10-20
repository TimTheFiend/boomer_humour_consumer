from __future__ import annotations

from typing import Iterable, Iterator, Optional, Tuple, TYPE_CHECKING
import random
import numpy as np
from tcod.console import Console
from bearlibterminal import terminal

# TODO TEMP
from components.tile_types import floor, temp
from constants import (
    CSNL_WIDTH,
    CSNL_HEIGHT,
    CSNL_PLAY_AREA_WIDTH,
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

    def get_play_area(self, x: int, y: int):
        width = int(CSNL_PLAY_AREA_WIDTH / 2)
        height = int(CSNL_HEIGHT / 2)
        return slice(x - width, x + width), slice(y - height, y + height)

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

    def render_blt(self, blt: terminal):
        """The alternative way of printing tiles with BLT.
        Considering the way it's printed, we need to specifically point to the unicode value of the current tile, hence the [0]
        """
        from rendering import draw_character_stats_box
        ## CLEAN UP
        
        blt.clear_area(0, 0, CSNL_PLAY_AREA_WIDTH, CSNL_HEIGHT)
        map_render = self.get_play_area(40, 50)

        for x in range(CSNL_PLAY_AREA_WIDTH):
            for y in range(CSNL_HEIGHT):
                blt.put(x, y, 0xE000 + int(self.tiles[x, y]['light'][0]))

        entities_sorted = sorted(self.entities, key=lambda x: x.render_order.value)
        for entity in entities_sorted:
            blt.put_ext(entity.x, entity.y, 0xE000 + 2)

        draw_character_stats_box(blt)


    def render_center(self, console: Console, player_pos: Tuple[int, int]) -> None:
        """Render functions which follows the player.

        The player will always be at the center, except at the edges of the map.

        x_pos and y_pos is used to adjust for printing entities on console.

        args:
        player_pos = player position on the game map (x, y)
        """
        x, y = player_pos
        left_render = right_render = top_render = bottom_render = 0
        HALF_WIDTH = int(CSNL_WIDTH / 2)
        HALF_HEIGHT = int(CSNL_HEIGHT / 2)

        x_pos = 0
        y_pos = 0

        if 0 <= x <= HALF_WIDTH:
            # If the player is at the left-most wall
            left_render = 0  
            right_render = CSNL_WIDTH  
        elif (self.width - HALF_WIDTH) <= x <= self.width:
            # If the player is at the right-most wall
            left_render = self.width - CSNL_WIDTH  
            right_render = self.width
            x_pos = self.width - CSNL_WIDTH
        else:
            # If the player is in between values above
            left_render = x - HALF_WIDTH
            right_render = x + HALF_WIDTH
            x_pos = x - HALF_WIDTH

        if 0 <= y <= HALF_HEIGHT:
            # If the player is at the top wall
            top_render = 0  
            bottom_render = CSNL_HEIGHT  
        elif (self.height - HALF_HEIGHT) <= y <= self.height:
            # If the player is at the bottom wall
            top_render = self.height - CSNL_HEIGHT  
            bottom_render = self.height
            y_pos = self.height - CSNL_HEIGHT
        else:
            # If the player is in between the values above
            top_render = y - HALF_HEIGHT
            bottom_render = y + HALF_HEIGHT
            y_pos = y - HALF_HEIGHT

        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['light'][left_render:right_render, top_render:bottom_render]


        entities_sorted = sorted(self.entities, key=lambda _x: _x.render_order.value)
        for entity in entities_sorted:
            console.print(x=entity.x - x_pos, y=entity.y - y_pos, string=entity.char, fg=(255, 0, 0))
            # console.print(x=entity.x - player_x, y=entity.y - player_y, string=entity.char, fg=entity.color)