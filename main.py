from __future__ import annotations

import tcod

from constants import (
    CONSOLE_HEIGHT,
    CONSOLE_WIDTH,
    TILESET_PATH,
    TILESET_ROW,
    TILESET_COL,
    # TEMP
    DUNGEON_HEIGHT,
    DUNGEON_WIDTH,
)


def temp_startup():
    from generators import entity_factories
    import copy
    from engine import Engine
    from game_map import GameMap
    from input_handlers import MainGameEventHandler
    player = copy.deepcopy(entity_factories.human)
    engine = Engine(player)

    engine.game_map = GameMap(engine, DUNGEON_WIDTH, DUNGEON_HEIGHT)
    # engine.game_map = GameMap(engine, DUNGEON_WIDTH, DUNGEON_HEIGHT)
    # engine.game_map = GameMap(engine, CONSOLE_WIDTH, CONSOLE_HEIGHT)
    engine.player.place(100, 100, engine.game_map)

    return MainGameEventHandler(engine)

def main():
    TILESET = tcod.tileset.load_tilesheet(path=TILESET_PATH, columns=TILESET_COL, rows=TILESET_ROW, charmap=tcod.tileset.CHARMAP_CP437)

    handler = temp_startup()

    with tcod.context.new_terminal(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        tileset=TILESET,
        title='TEMP FUNNY NAME HERE',
        # sdl_window_flags=tcod.context.SDL_WINDOW_MAXIMIZED,
        vsync=True,
    ) as context:
        console = tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT, order='F')

        while True:
            console.clear()
            handler.on_render(console=console)
            context.present(console)
            for event in tcod.event.wait():
                context.convert_event(event)
                handler = handler.handle_events(event)


if __name__ == '__main__':
    main()