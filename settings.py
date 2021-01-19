from os import path

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
MEDIUMGREY = (60, 60, 60)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (170, 110, 0)
YELLOW = (255, 255, 0)
BLUE=(0,0,255)

#Folder
game_folder = path.dirname('.')
dungeon_folder = path.join(game_folder, 'dungeon')
assets_folder = path.join(game_folder, 'assets')
room_folder = path.join(assets_folder, 'room')
champ_folder = path.join(assets_folder, 'character')
dark_wizard_folder = path.join(champ_folder, 'dark_wizard')
sun_wizard_folder = path.join(champ_folder, 'sun_wizard')
hunter_folder = path.join(champ_folder, 'archer')
explode_folder = path.join(champ_folder, 'explode')
skeleton_folder = path.join(champ_folder, 'skeleton')
gobelin_folder = path.join(champ_folder, 'gobelin')
wall_folder = path.join(assets_folder, 'wall')
sprite_folder = path.join(assets_folder, 'img_sprite')
button_folder = path.join(assets_folder, 'buttons_img')
portal_folder = path.join(assets_folder, 'portal')
bullet_forder = path.join(assets_folder,'bullet_img')
health_folder = path.join(assets_folder,'healthbar')
spell_folder = path.join(assets_folder,'spell')

# game settings
WIDTH = 800  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 600  # 16 * 48 or 32 * 24 or 64 * 12
PYGAMESIZE=6
FPS = 120
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 75
    
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

VOID_ID = 0
FLOOR_ID = 1
WALL_ID = 2
#CORNER_ID = 3
SHOP_ID = 6
SPAWN_ID = 7
DOOR_ID = 8
STAIR_ID = 9

# Player settings
PLAYER_SPEED = 600
RANGE = 25

ZOOM_VALUE = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3.5, 5]

#Enemy settings
ENEMY_SPEED = 600

#Bullets settings
BULLET_SPEED = 450
BULLET_LIFETIME = 1000
BULLET_RATE = 150
GUN_SPREAD = 5

#Combat Settings
Playercombathorizontalshift=24
Playercombatverticalshift=32

Skeletoncombathorizontalshift=24
Skeletoncombatverticalshift=38

Gobelincombathorizontalshift=44
Gobelincombatverticalshift=40

largeurHex = 35
hauteurHex = 40


# Loading things modified by user :
with open("assets/save/settings.txt") as options:
    SETTINGS=[line for line in options]