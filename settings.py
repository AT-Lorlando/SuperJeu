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
room_folder = path.join(assets_folder, 'room')
champ_folder = path.join(assets_folder, 'character')
wall_folder = path.join(assets_folder, 'wall')
sprite_folder = path.join(assets_folder, 'img_sprite')
button_folder = path.join(assets_folder, 'buttons_img')

# game settings
WIDTH = 1920   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 120
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 180
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_ID = 2
FLOOR_ID = 1
#CORNER_ID = 3
VOID_ID = 0

# Player settings
PLAYER_SPEED = 800
