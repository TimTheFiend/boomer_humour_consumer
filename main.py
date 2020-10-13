from __future__ import annotations

import tcod

from constants import (
    CONSOLE_HEIGHT,
    CONSOLE_WIDTH,
    TILESET_PATH,
    TILESET_ROW,
    TILESET_COL,
)


def temp_startup():
    from generators import entity_factories
    foo = entity_factories.human
    bar = getattr(foo, 'stats')
    print(getattr(foo, 'stats'))
    print(bar.agility)
    print(foo.name)



def main():
    TILESET = tcod.tileset.load_tilesheet(path=TILESET_PATH, columns=TILESET_COL, rows=TILESET_ROW, charmap=tcod.tileset.CHARMAP_CP437)

    temp_startup()

    with tcod.context.new_terminal(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        tileset=TILESET,
        title='TEMP FUNNY NAME HERE',
        vsync=True,
    ) as context:
        console = tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT, order='F')


if __name__ == '__main__':
    main()