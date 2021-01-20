from pygame import event
from pygame.constants import KEYDOWN
from settings import *
from Game import *
import pygame as pg
from Mother_screen import *
from math import floor
from Accueil import Button


class Dialogue(Mother_screen):
    def __init__(self, game, npc, quest = None):
        super(Dialogue, self).__init__(game)
        self.tab = []
        self.quest = quest
        self.sentence_index = 0
        self.npc = npc
        self.text_to_print = ["I have nothing to say","Sorry"]
        self.info_message = []
        if self.quest:
            self.text_to_print = self.quest.text_dialogue
        for sentence in self.text_to_print:
            self.tab.append(text_to_screen(sentence))
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
        self.accept_button = Button(floor(WIDTH*0.6), floor(HEIGHT*0.8), pg.image.load(
            path.join(button_folder, "accept.png")).convert(), pg.image.load(
            path.join(button_folder, "accept_clicked.png")).convert(), "name", self.accept)
        self.decline_button = Button(floor(WIDTH*0.3), floor(HEIGHT*0.8), pg.image.load(
            path.join(button_folder, "decline.png")).convert(), pg.image.load(
            path.join(button_folder, "decline_clicked.png")).convert(), "name", self.decline)
        self.return_button = Button(floor(WIDTH*0.6), floor(HEIGHT*0.8), pg.image.load(
            path.join(button_folder, "return.png")).convert(), pg.image.load(
            path.join(button_folder, "return_clicked.png")).convert(), "name", self._return)

        self.buttons = [self.next_button, self.exit_button]
        self.down = False


    def run(self, background=None):
        self.running = True
        if self.quest:
            if self.quest in self.player.quest_list:
                self.sentence_index = len(self.text_to_print) - 1
                self.info_message = [text_to_screen(self.quest.goal, color=GREEN)]
                self.buttons = [self.exit_button, self.return_button]
            if self.quest.is_finished:
                self.tab = [(pg.font.SysFont("Blue Eyes.otf", 30).render(
                    "Thanks for the help!", True, (255, 255, 255)))]
                self.buttons = [self.exit_button]
                self.sentence_index = 0
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
        for i in range(len(self.info_message)):
            self.screen.blit(
                self.info_message[i], (floor(WIDTH*0.275), floor(HEIGHT*0.13 + (i+len(self.tab))*30)))
        if self.down:
            for button in self.buttons:
                if button.is_clicked(mouse[0], (x, y)):
                    button.method()
            self.down = False

        

    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_f:
                    self.next()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.down = True

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

    def next(self):
        self.sentence_index += 1
        if self.sentence_index == len(self.tab)-1:
            self.buttons = [self.accept_button, self.decline_button]
        
    def exit(self):
        self.running = False

    def accept(self):
        self.npc.accept(self.player)
        self.info_message = [text_to_screen(self.quest.goal, color=GREEN)]
        self.buttons = [self.exit_button, self.return_button]

    def decline(self):
        self.running = False

    def _return(self):
        if self.quest.is_complete(self.player):
            self.quest.congrats(self.player)
            self.info_message = []
            self.running = False
        else:
            self.info_message = [text_to_screen(self.quest.goal, color=GREEN),
                text_to_screen("The quest isn't finished yet", color=RED)]

    def linkwith(self, player):
        self.player = player