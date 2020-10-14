from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from exceptions import Impossible

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor):
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self) -> None:
        raise NotImplementedError()

class ActionWithDirection(Action):
    """Pre-movement action."""
    def __init__(self, entity: Actor, x: int, y: int) -> None:
        super().__init__(entity)
        self.x = x
        self.y = y

    @property
    def destination(self) -> Tuple[int, int]:
        return self.entity.x + self.x, self.entity.y + self.y

    @property
    def blocking_entity(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.destination)

    @property
    def target_actor(self) -> Actor:
        return self.engine.game_map.get_actor_at_location(*self.destination)

    def perform(self) -> None:
        raise not NotImplementedError()


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return None
        else:
            return MovementAction(self.entity, self.x, self.y).perform()


class MovementAction(ActionWithDirection):
    def perform(self):
        dest_x, dest_y = self.destination

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            raise Impossible # Destination out of bounds

        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise NotImplementedError() # Destination blocked by tile

        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            raise NotImplementedError() # Destination blocked by entity

        self.entity.move(self.x, self.y)

class MeleeAction(ActionWithDirection):
    pass

class InteractionAction(ActionWithDirection): # Åbne døre? Snakke med NPCs?
    pass