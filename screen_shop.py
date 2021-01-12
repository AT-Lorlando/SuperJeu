import pygame as pg
import sys
from os import path
from shop import *
from settings import HEIGHT, WIDTH, assets_folder
from Mother_screen import *


class Screen_shop(Mother_screen):
    def __init__(self, screen, game, ID):
        super(Screen_shop, self).__init__(game)
        self.screen = screen
        # 180 is the argument to change the blur
        self.fond.fill((0, 0, 0, 180))
        self.shop = SHOP_DICT[ID]
        self.player_inventory = None
        self.animation = None
        self.image = None
        self.image_pos = (0, 0)
        self.handled = None
        self.copy = None
        self.money = 0
        self.main_font = pg.font.SysFont("Blue Eyes.otf", 50)
        self.fond_coin = pg.image.load(
            path.join(assets_folder, "coin.png"))
        self.fond_coin = pg.transform.scale(self.fond_coin, (30, 30))
        self.origin = None

    def update(self, player):
        self.mouse = pg.mouse.get_pressed()
        self.pos_mouse = pg.mouse.get_pos()
        self.player_inventory.update(self.mouse, self.pos_mouse)
        self.shop.inv.update(self.mouse, self.pos_mouse)

        self.take_item(self.player_inventory)
        self.take_item(self.shop.inv)

        if self.handled != None:
            self.handled.pos_x = self.pos_mouse[0] - self.handled.rect[0]/2 - 5
            self.handled.pos_y = self.pos_mouse[1] - self.handled.rect[1]/2 - 5
            self.handled.update(self.mouse, self.pos_mouse)
        if not self.mouse[0] and self.handled:
            # find the case clicked
            over_case = None
            for case in self.player_inventory.inventory + self.shop.inv.inventory:
                if self.is_over(case):
                    over_case = case
                    break
            if self.is_over(self.player_inventory) and over_case != None and over_case.item == None:
                self.player_inventory.add(over_case, self.handled)
                if self.origin != self.player_inventory.name:
                    self.buy(self.handled, player)
            elif self.is_over(self.shop.inv) and over_case != None and over_case.item == None:
                self.shop.inv.add(over_case, self.handled)
                if self.origin != self.shop.inv.name:
                    self.sell(self.handled, player)
            else:
                self.copy.item = self.handled
                self.handled = None

        if not self.mouse[0]:
            self.handled = None

    def draw(self, player):
        # self.screen.blit(self.shop.fond, (self.shop.inv.pos_x,self.shop.inv.pos_y))  # fond
        # , WIDTH/4-(self.shop.inv.inventory[0].rect[0]/2)*self.shop.inv.width, HEIGHT/2-(
        self.shop.draw(self.screen)
        # self.shop.inv.inventory[1].rect[1]/2)*self.shop.inv.width)  # shop
        self.player_inventory.draw(
            self.screen)  # , WIDTH/4-(self.player_inventory.inventory[0].rect[0]/2)*self.player_inventory.width, HEIGHT/2-(self.player_inventory.inventory[1].rect[1]/2)*self.player_inventory.width)  # player inv
        if self.handled != None:
            self.handled.draw(self.screen)
        font_surface = self.main_font.render(
            str(player.money), True, (255, 255, 255))
        # WIDTH - font_surface.get_size()[1])
        self.screen.blit(
            font_surface, (WIDTH - font_surface.get_size()[0], 0))
        self.screen.blit(
            self.fond_coin, (WIDTH - (font_surface.get_size()[0] + self.fond_coin.get_size()[0] + 5), 0))

    def take_item(self, inv):
        if not self.handled:
            for case in inv.inventory:
                if case.item != None:
                    if case.item.is_clicked(self.mouse, self.pos_mouse):
                        self.handled = case.item
                        self.copy = case
                        self.origin = inv.name
                        case.remove()

    def buy(self, item, player):
        player.money -= item.price
        print("You buy", item.name)

    def sell(self, item, player):
        player.money += item.price

    def is_over(self, target):
        return target.pos_x < self.pos_mouse[0] < target.pos_x + target.rect[0] and target.pos_y < self.pos_mouse[1] < target.pos_y + target.rect[1]

    def run(self, background, player):
        self.player_inventory = player.inv
        player.inv.pos_x = WIDTH/4 - \
            (self.player_inventory.inventory[0].rect[0]/2) * \
            self.player_inventory.width

        player.inv.pos_y = HEIGHT/2 - \
            (self.player_inventory.inventory[1].rect[1]/2) * \
            self.player_inventory.width

        self.shop.inv.pos_x = 3*WIDTH/4 - \
            (self.player_inventory.inventory[0].rect[0]/2) * \
            self.player_inventory.width

        self.shop.inv.pos_y = HEIGHT/2 - \
            (self.player_inventory.inventory[1].rect[1]/2) * \
            self.player_inventory.width

        if self.animation:
            for img in self.animation:
                self.screen.blit(background, (0, 0))
                self.screen.blit(self.fond, (0, 0))
                self.screen.blit(img, self.image_pos)
                pg.display.flip()
                time.sleep(.03)
        self.running = True
        self.money = player.money
        while self.running:
            self.game.dt_update()
            self.print_background(background)
            self.events()
            self.update(player)            # player_inventory.draw(self.screen)
            self.draw(player)
            pg.display.update()
