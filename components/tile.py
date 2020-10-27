from __future__ import annotations
from typing import Tuple, Dict
from random import choice


class Tile:
    walkable: bool
    transparent: bool
    char: str
    light_fg: Tuple[int,int,int]
    # light_bg: Tuple[int,int,int]
    # dark_fg: Tuple[int,int,int]
    # dark_bg: Tuple[int,int,int]
    
    def __init__(self, values:Dict):
        for key, value in values.items():
            if key == "char":
                setattr(self, key, choice(value))
                continue
            setattr(self, key, value)

