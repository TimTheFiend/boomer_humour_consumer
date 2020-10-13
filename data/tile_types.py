from typing import Tuple

import numpy as np


graphic_dt = np.dtype(
    [
        ('ch', str),
        ('fg', '3B'),
        ('bg', '3B'),
    ]
)

tile_dt = np.dtype(
    [
        ('walkable', np.bool),
        ('transparent', np.bool),
        ('dark', graphic_dt),
        ('light', graphic_dt),
    ]
)

def new_tile(
    *,
    walkable: int,
    transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# TODO make json for tile creation