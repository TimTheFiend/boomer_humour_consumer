from __future__ import annotations

import random
import time
from copy import deepcopy

from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from game_map import GameMap
from generators import entity_factories
from components import tile_types


if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

def dungeon_cellular_simple(dungeon, start_floor_chance=0.55, smooth_level=3):
    # dungeon = [[tile_types.tree1 for x in range(dungeon.width)] for y in range(dungeon.height)]

    # Randomly fill all-but-border cells by floor with start_floor_chance probability
    for y, _ in enumerate(dungeon.tiles):  # Ignores the outer rows/cols
        for x, __ in enumerate(_):
            chance = random.random()
            if chance <= start_floor_chance:
                if random.randint(0, 100) > 75:
                    dungeon.tiles[y][x] = tile_types.ground
                else:
                    dungeon.tiles[y][x] = tile_types.leaves

    # Sequentially smooth the map smooth_level times
    for _ in range(smooth_level):
        dungeon = _smooth_map(dungeon)

    return dungeon

def _smooth_map(M2):
    # Already replaced cells must not affect current so we need a copy of the original map
    M = deepcopy(M2)
    for y, line in enumerate(M2.tiles[1: -1]):
        for x, _ in enumerate(line[1: -1]):
            true_x = x + 1
            true_y = y + 1
            # Check the number of walls in ORIGINAL map
            number_of_walls = sum(
                cell == tile_types.tree1 or cell == tile_types.tree2
                for cell in [
                    M.tiles[true_y][true_x],
                    M.tiles[true_y+1][true_x],
                    M.tiles[true_y-1][true_x],
                    M.tiles[true_y][true_x+1],
                    M.tiles[true_y+1][true_x+1],
                    M.tiles[true_y-1][true_x+1],
                    M.tiles[true_y][true_x-1],
                    M.tiles[true_y+1][true_x-1],
                    M.tiles[true_y-1][true_x-1],
                ]
            )
            # And set them in smoothed map

            if number_of_walls >= 5:
                if random.randint(0, 100) > 50:
                    M2.tiles[true_y][true_x] = tile_types.tree1
                else:
                    M2.tiles[true_y][true_x] = tile_types.tree2
            elif number_of_walls < 5 and random.randint(0, 100) > 20:
                M2.tiles[true_y][true_x] = tile_types.ground
            else:
                M2.tiles[true_y][true_x] = tile_types.leaves

            # M2.tiles[true_y][true_x] = (
            #     tile_types.tree1 if number_of_walls >= 5 else tile_types.ground
            # )
    return M2

def forest(
    *,
    map_width,
    map_height,
    engine: Engine,
):
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    player.place(25, 25, dungeon)

    print("f start")
    start_time = time.time()
    dungeon = dungeon_cellular_simple(dungeon, start_floor_chance=0.55, smooth_level=1)

    print(len(dungeon.gamemap.entities))
    print(time.time()-start_time)
    return dungeon