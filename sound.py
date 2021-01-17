import pygame as pg
from settings import *
pg.init()

MUSIC=pg.mixer.music

explosionSound = pg.mixer.Sound("assets/sound/explosion_fire.wav")

def swap_music(file):
    MUSIC.unload()
    MUSIC.fadeout(5000)
    MUSIC.load(file)
    #MUSIC.set_volume(VOLUME[0]/100)
    MUSIC.play(loops=-1)