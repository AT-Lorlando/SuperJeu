from os import path
import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (170, 110, 0)
YELLOW = (255, 255, 0)

# Folder
game_folder = path.dirname('.')
dungeon_folder = path.join(game_folder, 'dungeon')
assets_folder = path.join(game_folder, 'assets')

champ_folder = path.join(assets_folder, 'character')
spell_folder = path.join(assets_folder, 'spell')
dark_wizard_folder = path.join(champ_folder, 'dark_wizard')
sun_wizard_folder = path.join(champ_folder, 'sun_wizard')
hunter_folder = path.join(champ_folder, 'archer')

explode_folder = path.join(champ_folder, 'explode')

button_folder = path.join(assets_folder, 'buttons_img')
map_folder = path.join(assets_folder, 'map_background')

# wall_folder = path.join(assets_folder, 'wall')
sprite_folder = path.join(assets_folder, 'img_sprite')
item_folder = path.join(assets_folder, 'items')
# portal_folder = path.join(assets_folder, 'portal')
# room_folder = path.join(assets_folder, 'room')

# Tiles Folder
tile_folder = path.join(assets_folder, 'tiles')
deco_folder = path.join(tile_folder, 'deco')
floor_folder = path.join(tile_folder, 'floor')
house_folder = path.join(tile_folder, 'house')
npc_folder = path.join(tile_folder, 'npc')
portal_folder = path.join(tile_folder, 'portal')
wall_folder = path.join(tile_folder, 'wall')


# game settings
WIDTH = 1080   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 720  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 120
TITLE = "Superjeu"
BGCOLOR = DARKGREY

TILESIZE = 96
CHARACTER_SIZE = 60
ITEM_SIZE = 40

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

VOID_ID = 0
FLOOR_ID = 10
WALL_ID = 11
NPC_ID = 12

QUEST_ID = 112
SHOP_ID = 212
CHEST_ID = 912

SPAWN_ID = 13
DOOR_ID = 14
STAIR_ID = 15
COLLECTABLE_ID = 16
MOB_ID = 17

HOUSE_ID = 52
WATER_ID = 53

# Player settings
PLAYER_SPEED = 600
RANGE = 25
LAYER_NUMBER = 10

STAGE_SIZE_TAB = [1,2,3,3,3,4,4,4,5]
ZOOM_VALUE = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.5, 5]

def resize(img, size, y=0):
    return pg.transform.scale(img, (size, y)) if y else pg.transform.scale(img, (size, size))