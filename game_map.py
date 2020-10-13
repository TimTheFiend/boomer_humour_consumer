from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor, Item


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

        self.tiles = np.full((width, height), fill_value=None, order='F')

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) # TODO
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Item)
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
        return 0 <= x <= self.width and 0 <= y <= self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0 : self.width, 0 : self.height] = self.tiles