from settings import *
from Game import *
import pygame as pg
from Mother_screen import *
from math import floor

class Dialogue(Mother_screen):
    def __init__(self, game, *text):
        super(Dialogue, self).__init__(game)
        self.tab = []
        self.sentence_index = 0
        for sentence in text:
            self.tab.append(pg.font.SysFont("Blue Eyes.otf", 30).render(
                sentence, True, (255, 255, 255)))
        self.x = floor(WIDTH*0.25)
        self.y = floor(HEIGHT*0.1)
        self.rect = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.fond.fill((0, 0, 0, 100))
        self.screen = game.screen
        self.image_pos = (floor(WIDTH*0.25), floor(HEIGHT*0.1))
        self.image = pg.transform.scale(pg.image.load(path.join(assets_folder, 'dialogue_bg.png')), (floor(WIDTH*0.5), floor(HEIGHT*0.8)))

    def print_text(self, text):
        pass

#     clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 48)
# string = "A long time ago"
# windowSurface.fill(BLACK)
# for i in range(len(string)):
#     text = font.render(string[i], True, (0, 128, 0))
#     windowSurface.blit(text,(400 + (font.size(string[:i])[0]), 300))
#     pygame.display.update()
#     clock.tick(2)

    def run(self, background=None):
        self.running = True
        while self.running:
            self.game.dt_update()
            if background:
                self.print_background(background)
            for i in range(self.sentence_index+1):
                self.screen.blit(self.tab[i],(floor(WIDTH*0.275), floor(HEIGHT*0.13 + i*30)))
            if self.sentence_index == len(self.tab):
                pass
                #Bouton Decline / Accept
            else:
                pass
                #Bouton Next Dialogue
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_f:
                    self.next()
            
    def next(self):
        self.sentence_index += 1