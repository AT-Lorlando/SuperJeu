from pygame import event
from pygame.constants import KEYDOWN
from settings import *
from Game import *
import pygame as pg
from Mother_screen import *
from math import floor
from Accueil import Button


class Dialogue(Mother_screen):
    def __init__(self, game, npc,*text):
        super(Dialogue, self).__init__(game)
        self.tab = []
        self.sentence_index = 0
        self.npc = npc
        for sentence in text:
            self.tab.append(pg.font.SysFont("Blue Eyes.otf", 30).render(
                sentence, True, (255, 255, 255)))
        self.x = floor(WIDTH*0.25)
        self.y = floor(HEIGHT*0.1)
        self.rect = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.fond.fill((0, 0, 0, 100))
        self.screen = game.screen
        self.image_pos = (floor(WIDTH*0.25), floor(HEIGHT*0.1))
        self.image = pg.transform.scale(pg.image.load(path.join(
            assets_folder, 'dialogue_bg.png')), (floor(WIDTH*0.5), floor(HEIGHT*0.8)))
        self.player = None
        # Buttons

        
        self.next_button = Button(floor(WIDTH*0.6), floor(HEIGHT*0.8), pg.image.load(
            path.join(button_folder, "next.png")).convert(), pg.image.load(
            path.join(button_folder, "next_clicked.png")).convert(), "name",self.next)
        self.exit_button = Button(floor(WIDTH*0.3), floor(HEIGHT*0.8), pg.image.load(
            path.join(button_folder, "exit.png")).convert(), pg.image.load(
            path.join(button_folder, "exit_clicked.png")).convert(), "name",self.exit)
        self.buttons = [self.next_button, self.exit_button]
        self.down = False

    def run(self, background=None):
        self.running = True
        if not self.npc.quest:
            self.tab.append(pg.font.SysFont("Blue Eyes.otf", 30).render(
                "You finished the quest", True, (255, 255, 255)))
            self.sentence_index += 1
        while self.running:
            self.events()
            self.update(background)
            self.draw()
            pg.display.update()

    def update(self, background):
        mouse = pg.mouse.get_pressed()
        x, y = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse[0], (x, y))

        self.game.dt_update()
        if background:
            self.print_background(background)
        for i in range(self.sentence_index+1):
            self.screen.blit(
                self.tab[i], (floor(WIDTH*0.275), floor(HEIGHT*0.13 + i*30)))
        if self.down:
            for button in self.buttons:
                if button.is_clicked(mouse[0], (x, y)):
                    print("this", button.method)
                    button.method()
            self.down = False

        

    def events(self):
        # catch all events here

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_f:
                    self.next()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.down = True
                print("Click")

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

    def next(self):
        self.sentence_index += 1
        if self.sentence_index == len(self.tab)-1:
            self.buttons.remove(self.next_button)
            self.buttons.remove(self.exit_button)
            self.accept_button = Button(floor(WIDTH*0.6), floor(HEIGHT*0.8), pg.image.load(
                path.join(button_folder, "accept.png")).convert(), pg.image.load(
                path.join(button_folder, "accept_clicked.png")).convert(), "name", self.accept)
            self.decline_button = Button(floor(WIDTH*0.3), floor(HEIGHT*0.8), pg.image.load(
                path.join(button_folder, "decline.png")).convert(), pg.image.load(
                path.join(button_folder, "decline_clicked.png")).convert(), "name", self.decline)
            self.buttons.append(self.accept_button)
            self.buttons.append(self.decline_button)
        
    def exit(self):
        self.running = False

    def accept(self):
        self.npc.accept(self.player)
        self.running = False

    def decline(self):
        self.running = False

    def linkwith(self, player):
        self.player = player