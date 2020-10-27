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
    from generators.procedural_generation import generate_dungeon, generate_forest, place_tile

    player = copy.deepcopy(entity_factories.human)
    engine = Engine(player)


    map_height = DUNGEON_HEIGHT
    map_width = DUNGEON_WIDTH
    max_rooms = 1000
    max_trees = 100000
    max_rivers = 2
    room_min_size = 5
    room_max_size = 15

    # engine.game_map = generate_dungeon(
    #     map_width=map_width,
    #     map_height=map_height,
    #     max_rooms=max_rooms,
    #     room_min_size=room_min_size,
    #     room_max_size=room_max_size,
    #     engine=engine,
    # )

    engine.game_map = generate_forest(
        map_width=map_width,
        map_height=map_height,
        max_trees=max_trees,
        engine=engine,
    )


    return MainGameEventHandler(engine)

def main():
    TILESET = tcod.tileset.load_tilesheet(
        path=TILESET_PATH,
        columns=TILESET_COL,
        rows=TILESET_ROW,
        charmap=tcod.tileset.CHARMAP_CP437
    )
    handler = temp_startup()

    with tcod.context.new_terminal(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        tileset=TILESET,
        title='TEMP FUNNY NAME HERE',
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