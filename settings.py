from os import path

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (170, 110, 0)
YELLOW = (255, 255, 0)

#Folder
game_folder = path.dirname('.')
dungeon_folder = path.join(game_folder, 'dungeon')
assets_folder = path.join(game_folder, 'assets')

champ_folder = path.join(assets_folder, 'character')
dark_wizard_folder = path.join(champ_folder, 'dark_wizard')
sun_wizard_folder = path.join(champ_folder, 'sun_wizard')
hunter_folder = path.join(champ_folder, 'archer')

explode_folder = path.join(champ_folder, 'explode')

button_folder = path.join(assets_folder, 'buttons_img')
map_folder = path.join(assets_folder, 'map_background')

# wall_folder = path.join(assets_folder, 'wall')
sprite_folder = path.join(assets_folder, 'img_sprite')
# portal_folder = path.join(assets_folder, 'portal')
# room_folder = path.join(assets_folder, 'room')

#Tiles Folder
tile_folder = path.join(assets_folder, 'tiles')
deco_folder = path.join(tile_folder, 'deco')
floor_folder = path.join(tile_folder, 'floor')
house_folder = path.join(tile_folder, 'house')
npc_folder = path.join(tile_folder, 'npc')
portal_folder = path.join(tile_folder, 'portal')
wall_folder = path.join(tile_folder, 'wall')




# game settings
WIDTH = 1920   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 200
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 96
CHARACTER_SIZE = 60
    
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

VOID_ID = 0
FLOOR_ID = 10
WALL_ID = 11
SHOP_ID = 12
SPAWN_ID = 13
DOOR_ID = 14
STAIR_ID = 15
NPC_ID = 51
HOUSE_ID = 52
WATER_ID = 53

# Player settings
PLAYER_SPEED = 600
RANGE = 25

ZOOM_VALUE = [0.1,0.2,0.3,0.4,0.5,0.6,0.8,1,1.2,1.4,1.6,1.8,2,2.2,2.4,2.6,2.8,3,3.5,5]
