from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
from generators import entity_factory
from components import tile_types


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
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Returns the inner area of the room.

        A 'slice' object is used to indicate how to "cut" up a collection,
        so what we return are the exact coordinates of where this 'RectangularRoom' is in te 'GameMap'

        Adds '+1' to take the walls of the room into account"""

        return slice(self.x1 +1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other:RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""

        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def generate_dungeon(
    *,
    map_width,
    map_height,
    max_rooms,
    room_min_size,
    room_max_size,
    engine: Engine,
) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)

    for i in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        # if len(rooms) == 0:
        #     # First room generated
        #     player.place(*new_room.center, dungeon)
        # else:
        #     for x, y in tunnel_between(rooms[-1].center, new_room.center):
        #         dungeon.tiles[x, y] = tile_types.floor

        #     center_of_last_room = new_room.

        # place_entities(new_room, dungeon, engine.game_world.current_floor)

        # dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        # dungeon.downstairs = center_of_last_room

        rooms.append(new_room)
    return dungeon