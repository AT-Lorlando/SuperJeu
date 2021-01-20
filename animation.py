
import pygame as pg

class Animation():
    def __init__(self, game, pos, tab, colorkey = None, frame_rate=12):
        self.game = game
        self.frame_rate = frame_rate
        self.time_since_anime = 0
        self.actual_frame = 0
        self.pos = pos
        self.colorkey = None
        if colorkey:
            self.colorkey = colorkey
        # self.rect = pg.Rect(0,0,pos)
        self.image_tab = tab
        self.to_kill = False

    def draw(self):
        this_image = self.image_tab[self.actual_frame]
        if self.colorkey:
            this_image.set_colorkey(self.colorkey)
        self.game.screen.blit(this_image, self.pos)

    def update(self):
        now = pg.time.get_ticks()
        if(now > self.time_since_anime + self.frame_rate):
            self.time_since_anime = now
            self.actual_frame += 1
            if self.actual_frame >= len(self.image_tab):
                self.game.animation_tab.remove(self)