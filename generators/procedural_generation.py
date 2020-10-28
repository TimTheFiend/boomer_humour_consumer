from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from game_map import GameMap
from generators import entity_factories
from components import tile_types


if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class River:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
        return slice(self.x1 + 1, self.x2 - 1), slice(self.y1 + 1, self.y2 - 1)
    
    @property
    def outer(self) -> Tuple[slice, slice]:
        """Returns the outer area of the room.
        
        This essentially means that we find the wall"""
        return slice(self.x1, self.x2), slice(self.y1, self.y2)

    @property
    def door(self) -> Tuple[int, int]:
        x = 0
        y = 0
        if random.random() < 0.5:
            x = random.randint(self.x1 +1, self.x2 -2)
            y = random.choice((self.y1, self.y2 -1))
        
        else:
            y = random.randint(self.y1 +1, self.y2 -2)
            x = random.choice((self.x1, self.x2 -1))

        return x,y

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
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)

    player.place(25, 25, dungeon)

    for i in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
            
        # for x in range(new_room.x1, new_room.x2):
        #     for y in range(new_room.y1, new_room.y2):
        #         dungeon.tiles[x, y] = tile_types.wall

        dungeon.tiles[new_room.outer] = tile_types.wall
        dungeon.tiles[new_room.inner] = tile_types.floor
        dungeon.tiles[new_room.door] = tile_types.door     

        new_room.outer

        if len(rooms) == 0:
            # First room generated
            player.place(*new_room.center, dungeon)
        # else:
        #     for x, y in tunnel_between(rooms[-1].center, new_room.center):
        #         dungeon.tiles[x, y] = tile_types.floor

        #     center_of_last_room = new_room.

        # place_entities(new_room, dungeon, engine.game_world.current_floor)

        # dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        # dungeon.downstairs = center_of_last_room

        rooms.append(new_room)
    return dungeon

def generate_forest(
    *,
    map_width,
    map_height,
    tree_chance, #density - %
    engine: Engine,
) -> GameMap:    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    player.place(25, 25, dungeon)

    for x in range(map_width):
        for y in range(map_height):
            if random.randint(0, 100) < tree_chance:
                new_tree = Tree(x, y)
                dungeon.tiles[x, y] = random.choice((tile_types.tree1, tile_types.tree2))

            if random.randint(0, 100) < int(tree_chance / 4):
                dungeon.tiles[x, y] = tile_types.leaves    

    # ville gøre dette til en funktion men jeg er for dum til at få det til at virke

    noisemap = tcod.noise.Noise(
        dimensions=2,
        algorithm=tcod.NOISE_SIMPLEX,
        implementation=tcod.noise.TURBULENCE,
        hurst=0.7,
        lacunarity=3.8,
        octaves=4,
    )

    ogrid = [
        np.arange(map_width, dtype=np.float32,),
        np.arange(map_height, dtype=np.float32,),
    ]

    ogrid[0] *= 0.05
    ogrid[1] *= 0.05

    hm_height = noisemap.sample_ogrid(ogrid)
    tcod.heightmap_normalize(hm_height, 0.0, 1.0)

    max_rivers = random.randint(4, 6)
    max_roads = 5
    print(max_rivers)

    for rivers in range(max_rivers):

        temp_cost = []
        for x in range(map_width):
            temp_row = []
            for y in range(map_height):
                tile = hm_height[x, y]
                value = 0
                if 0.0 <= tile <= 0.1:
                    value = 1
                if 0.1 <= tile <= 0.2:
                    value = 2
                if 0.2 <= tile <= 0.3:
                    value = 3
                if 0.3 <= tile <= 0.4:
                    value = 4
                if 0.4 <= tile <= 0.5:
                    value = 5
                if 0.5 <= tile <= 0.6:
                    value = 6
                if 0.6 <= tile <= 0.7:
                    value = 7
                if 0.7 <= tile <= 0.8:
                    value = 8
                if 0.8 <= tile <= 0.9:
                    value = 9
                if 0.9 <= tile <= 1.0:
                    value = 10
                
                temp_row.append(value)
            temp_cost.append(temp_row)

        cost = np.array(temp_cost, dtype=np.int8, order='F')
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=10,)
        
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((0, random.randint(0, map_height -1)))

        # path = pathfinder.path_to((map_width -1, random.randint(0, map_height -1)))[:].tolist()
        path = pathfinder.path_to((map_width -1, random.randint(0, map_height -1)))[:].tolist()
        for i, j in path:
            if dungeon.tiles[i, j] == tile_types.shallow_water or dungeon.tiles[i, j] == tile_types.deep_water:
                break
            dungeon.tiles[i, j] = tile_types.shallow_water

    # TODO
    # roads
    # samme pathfinding som når man laver en flod, men på et tidspunkt skal tile_type tjekkes, hvis tile_type er en anden road, koster det færre point at lave en road

    for roads in range(max_roads):
        temp_cost = []
        for x in range(map_width):
            temp_row = []
            for y in range(map_height):
                tile = hm_height[x, y]
                value = 0
                if 0.0 <= tile <= 0.1:
                    value = 2
                if 0.1 <= tile <= 0.2:
                    value = 3
                if 0.2 <= tile <= 0.3:
                    value = 4
                if 0.3 <= tile <= 0.4:
                    value = 5
                if 0.4 <= tile <= 0.5:
                    value = 6
                if 0.5 <= tile <= 0.6:
                    value = 7   
                if 0.6 <= tile <= 0.7:
                    value = 8
                if 0.7 <= tile <= 0.8:
                    value = 9
                if 0.8 <= tile <= 0.9:
                    value = 10
                if 0.9 <= tile <= 1.0:
                    value = 11

                if dungeon.tiles[x, y] == tile_types.road:
                    value = 1

                if dungeon.tiles[x, y] == tile_types.shallow_water or dungeon.tiles[x, y] == tile_types.deep_water:
                    value = 15

                temp_row.append(value)
            temp_cost.append(temp_row)

        cost = np.array(temp_cost, dtype=np.int8, order='F')
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=10,)
        
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((30, 30))

        path = pathfinder.path_to((random.randint(0, map_width -1,), random.randint(0, map_height -1)))[:].tolist()

        for i, j in path:
            dungeon.tiles[i, j] = tile_types.road

    # TODO
    # placer huse, lav veje mellem husene
    # optimer koden (den er MEGET langsom(mange loops, go figure))
    # placer søer

    return dungeon

def place_tile(engine:Engine):   
    from components.tile import Tile                
    width = 80
    height = 60
    values = {
    "walkable": False,
    "transparent": False,
    "char": ["█", "p"],
    "light_fg": (255, 255, 255)
    }

    player = engine.player  
    dungeon = GameMap(engine, width, height, entities=[player])
    player.place(1, 1, dungeon)

    for x in range(width):
        for y in range(height):
            dungeon.tiles[x, y] = Tile(values)
    return dungeon
