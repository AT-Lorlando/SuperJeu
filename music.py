import pygame as pg
from settings import *

MUSIC=pg.mixer.music
VOLUME=[int(SETTINGS[4][10:-1])]

def swap_music(file):
    MUSIC.unload()
    MUSIC.fadeout(5000)
    MUSIC.load(file)
    MUSIC.set_volume(VOLUME[0]/100)
    MUSIC.play(loops=-1)

def save_music_lvl():
    SETTINGS[4]=f"MUSIC_LVL={VOLUME[0]}\n"
    with open('save/settings.txt','w') as options:
        options.write("".join(f'{optn}' for optn in SETTINGS))