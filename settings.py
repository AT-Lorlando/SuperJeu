import pygame
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)



# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12

FPS = 60
TITLE = "First Pygame"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

walkRight = ['R' + str(x) + '.png' for x in range(1,11)]
walkLeft = ['L' + str(x) + '.png' for x in range(1,11)]
walkUp = ['U' + str(x) + '.png' for x in range(1,11)]
walkDown = ['D' + str(x) + '.png' for x in range(1,11)]

# Player settings
PLAYER_SPEED = 300
# Enemy settings
ENEMY_SPEED = 300
moveRight = ['RE1.png', 'RE2.png', 'RE3.png', 'RE4.png', 'RE5.png', 'RE6.png', 'RE7.png', 'RE8.png', 'RE9.png']
moveLeft = ['LE1.png', 'LE2.png', 'LE3.png', 'LE4.png', 'LE5.png', 'LE6.png', 'LE7.png', 'LE8.png', 'LE9.png']
# Gun settings
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
GUN_SPREAD = 5