from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov
from tcod import FOV_DIAMOND


if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap



class Engine:
    game_map: GameMap

    # def __init__(self, player: Actor):
    def __init__(self, player: str):
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except Exception:
                    pass # TODO

    def update_fov(self) -> None:
        raise NotImplementedError()

    def render(self, console: Console) -> None:
        self.game_map.render(console)