from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov
from tcod import FOV_DIAMOND


from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap



class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.player = player
        self.mouse_position = (0, 0)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except Impossible:
                    pass

    def update_fov(self) -> None:
        raise NotImplementedError()

    def render(self, console: Console) -> None:
        # self.game_map.render(console)
        self.game_map.render_center(console, (self.player.x, self.player.y))
        self.DEV_DEBUG()



    def DEV_DEBUG(self) -> None:
        """Used to display relevant info that isn't otherwise available to the player."""
        position_string = f'X: {str(self.player.x).rjust(4)} Y: {str(self.player.y).rjust(4)}'


        print(position_string, end='')
        print('\b' * len(position_string), end='', flush=True)
        print('\b' * len(position_string), end='', flush=True)
