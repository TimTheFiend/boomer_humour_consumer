from __future__ import annotations

from bearlibterminal import terminal

from constants import (
    CSNL_WIDTH as total_width,
    CSNL_HEIGHT as total_height,
    CSNL_CHARACTER_STATS_WIDTH as box_width,
    CSNL_CHARACTER_STATS_HEIGHT as box_height,
)
## VERY TEMP
from tileset_quick_access import Tileset



X_POS = total_width - box_width + 1

def draw_player_info(blt: terminal):
    """Draws HP box, requires `player` entity.
    
    Clears the area it operates in, and redraws it.
    """
    left_side_width = int(box_width / 2) - 1

    MAX_HP = 30  # Temp var that acts as standin for player.max_hp
    CURRENT_HP = 14  # temp var that acts as standin for player.hp

    MAX_MANA = 30
    CURRENT_MANA = 2

    LVL_TEMP = 4
    XP_TEMP = 224
    XP_TO_LVL_TEMP = 350
    ## Cleaning up
    blt.clear_area(X_POS, 1, left_side_width, box_height - 1)
    
    ## Level
    blt.print(X_POS, 1, f'Level:{str(LVL_TEMP).ljust(3)}')
    ## Bar length is calculated
    bar_width_hp = int(float(CURRENT_HP) / MAX_HP * left_side_width)
    bar_width_mp = int(float(CURRENT_MANA) / MAX_MANA * left_side_width)
    xp_width_mp = int(float(XP_TEMP) / XP_TO_LVL_TEMP * left_side_width)
    ## Health Points
    blt.print(X_POS, 2, f"[bkcolor=red]{' ' * (left_side_width)}")
    blt.print(X_POS, 2, f"[bkcolor=green]{' ' * bar_width_hp}")
    blt.print(X_POS, 2, f"[color=black]HP: {str(CURRENT_HP).ljust(3)}/{str(MAX_HP).ljust(3)}", width=left_side_width, height=1, align=blt.TK_ALIGN_LEFT)
    ## Mana Points
    blt.print(X_POS, 3, f"[bkcolor=white]{' ' * (left_side_width)}")
    blt.print(X_POS, 3, f"[bkcolor=blue]{' ' * bar_width_mp}")
    blt.print(X_POS, 3, f"[color=black]MP: {str(CURRENT_MANA).ljust(3)}/{str(MAX_MANA).ljust(3)}", width=left_side_width, height=1, align=blt.TK_ALIGN_LEFT)
    # Experience Points
    blt.print(X_POS, 4, f"[bkcolor=purple]{' ' * (left_side_width)}")
    blt.print(X_POS, 4, f"[bkcolor=yellow]{' ' * xp_width_mp}")
    blt.print(X_POS, 4, f"[color=black]XP: {str(XP_TEMP).ljust(4)}/{str(XP_TO_LVL_TEMP).ljust(4)}", width=left_side_width, height=1, align=blt.TK_ALIGN_LEFT)



def draw_character_stats_box(blt: terminal):
    """Draws the right-side character "screen".
    
    Only needs to be called once.
    """
    from constants import TILE_INFO
    ## STILL VERY TEMP
    tileset = Tileset(TILE_INFO)


    starting_point_x = total_width - box_width
    character_box_width = total_width - starting_point_x

    ## Top box divided
    for i in range(box_height):
        blt.put(starting_point_x + int(character_box_width / 2), i, tileset[186])

    ## Vertical box drawn
    for i in range(total_height):
        blt.put(starting_point_x, i, tileset[186])
        blt.put(total_width - 1, i, tileset[186])

    ## Horizontal box drawn
    for X_POS in range(starting_point_x, 100):
        blt.put(X_POS, 0, tileset[205])
        blt.put(X_POS, box_height, tileset[205])
        blt.put(X_POS, total_height - 1, tileset[205])

    ## Connecting vertical and horizontal
    blt.put(starting_point_x,   0,                  tileset[201])  # Top right connector
    blt.put(starting_point_x,   box_height,         tileset[204])  # Mid right connector
    blt.put(starting_point_x,   total_height - 1,   tileset[200])  # Bot right connector
    blt.put(total_width - 1,    0,                  tileset[184])  # Top left connector
    blt.put(total_width - 1,    box_height,         tileset[185])  # Mid left connector
    blt.put(total_width - 1,    total_height - 1,   tileset[188])  # Bot left connector


    blt.put(starting_point_x + int(character_box_width / 2), box_height, tileset[202])

    blt.print(starting_point_x, 0, "Player Name Goes Here", width=character_box_width, height=1, align=blt.TK_ALIGN_CENTER)
    draw_player_info(blt)

