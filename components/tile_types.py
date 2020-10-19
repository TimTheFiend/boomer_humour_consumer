from __future__ import annotations

from typing import Tuple

import numpy as np

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
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('\x91'),
        (255, 255, 255),
        (50, 50, 150)
    ),
    light=(
        ord('\x91'),
        (255,255,255),
        (200, 180, 50)
    ),
)
temp = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord('\x85'),
        (255, 255, 255),
        (50, 50, 150)
    ),
    light=(
        ord('\x85'),
        (255,255,255),
        (155, 155, 155)
    ),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(
        ord('█'),
        (255, 255, 255),
        (0, 0, 100)
    ),
    light=(
        ord('█'),
        (255,255,255),
        (130,110,50)
    ),
)