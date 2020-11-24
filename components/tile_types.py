from __future__ import annotations
import random
from typing import Tuple
from components.tile import Tile
import numpy as np

_wall = Tile(
{    "walkable": False,
    "transparent": False,
    "char": ["█", "p"],
    "light_fg": (255, 255, 255)}
)

graphic_dt = np.dtype(
    [
        ('ch', np.int32),  # Unicode
        ('fg', '3B'),
        ('bg', '3B'),
    ]
)

tile_dt = np.dtype(
    [
        ('walkable', np.bool),
        ('transparent', np.bool),
        ('dark', graphic_dt),
        ('light', graphic_dt)
    ]
)


def new_tile(
        *,  # Enforce the use of keywords so order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# TODO TEMPS

temp = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('@'),
        (255, 255, 255),
        (50, 50, 150)
    ),
    light=(
        ord('@'),
        (255,255,255),
        (155, 155, 155)
    ),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(
        random.choice((ord('█'), ord(' '))),
        (255, 255, 255),
        (0, 0, 100)
    ),
    light=(
        random.choice((ord('█'), ord(' '))),
        (255,255,255),
        (130,110,50)
    ),
)

door = new_tile(
    walkable=True,
    transparent=False,
    dark=(
        ord('█'),
        (135, 135, 135),
        (33, 33, 33)
    ),
    light=(
        ord('█'),
        (135, 135, 135),
        (143, 143, 143)
    ),
)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord(' '),
        (217, 148, 0),
        (217, 148, 0)
    ),
    light=(
        ord(' '),
        (217, 148, 0),
        (217, 148, 0)
    ),
)

ground = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord(','),
        (92, 63, 0),
        (97, 66, 0)
    ),
    light=(
        ord(','),
        (3, 176, 0),
        (97, 66, 0)
    ),
)

tree1 = new_tile(
    walkable=True, # False
    transparent=True,
    dark=(
        ord('♣'),
        (13, 161, 0),
        (97, 66, 0)
    ),
    light=(
        ord('♣'),
        (13, 161, 0),
        (97, 66, 0)
    ),
)

tree2 = new_tile(
    walkable=True, # False
    transparent=True,
    dark=(
        ord('♠'),
        (13, 161, 0),
        (97, 66, 0)
    ),
    light=(
        ord('♠'),
        (13, 161, 0),
        (97, 66, 0)
    ),
)

leaves = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('░'),
        (13, 161, 0),
        (97, 66, 0)
    ),
    light=(
        ord('░'),
        (13, 161, 0),
        (97, 66, 0)
    ),
)

deep_water = new_tile(
    walkable=False,
    transparent=True,
    dark=(
        ord('█'),
        (0, 0, 150),
        (0, 0, 150)
    ),
    light=(
        ord('█'),
        (0, 0, 150),
        (0, 0, 150)
    ),
)

shallow_water = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('█'),
        (0, 247, 255),
        (0, 247, 255)
    ),
    light=(
        ord('█'),
        (0, 247, 255),
        (0, 247, 255)
    ),
)

road = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('█'),
        (100, 50, 10),
        (100, 50, 10)
    ),
    light=(
        ord('█'),
        (100, 50, 10),
        (100, 50, 10)
    ),
)
