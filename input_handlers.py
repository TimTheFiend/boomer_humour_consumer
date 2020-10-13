from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING, Union

import tcod.event


from actions import Action


if TYPE_CHECKING:
    from engine import Engine

ActionOrEventHandler = Union[Action, 'BaseEventHandler']


class BaseEventHandler(tcod.event.EventDispatch[ActionOrEventHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f'{self!r} cannot handle actions.'
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit(0)


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # TODO
            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        if action is None:
            return False

        # todo

    def ev_mousemotion(self, event) -> None:
        #todo
        pass

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrEventHandler]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key == tcod.event.K_SPACE:
            print('AAAAAAAAAAAAAAAAAAAAAAAA')