import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import random
from random import randrange

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'sprites')
       
        self.map = Map(path.join(game_folder, 'map.txt'))

        #player
        self.player_img = pygame.image.load(path.join(img_folder, 'D1.png')).convert_alpha()
        self.player_img_left = [pygame.image.load(path.join(img_folder, img)).convert_alpha()for img in walkLeft]
        self.player_img_right = [pygame.image.load(path.join(img_folder, img)).convert_alpha() for img in walkRight]
        self.player_img_up = [pygame.image.load(path.join(img_folder, img)).convert_alpha() for img in walkUp]
        self.player_img_down = [pygame.image.load(path.join(img_folder, img)).convert_alpha() for img in walkDown]
     
        #enemy
        self.enemy_img = pygame.image.load(path.join(img_folder, 'standing.png')).convert_alpha()
        self.enemy_img_left = [pygame.image.load(path.join(img_folder, img)).convert_alpha()for img in moveLeft]
        self.enemy_img_right = [pygame.image.load(path.join(img_folder, img)).convert_alpha() for img in moveRight]      
        #bullet
        self.bullet_img = pygame.image.load(path.join(img_folder, 'bullet.png')).convert_alpha()
        #wall
        self.wall_img1 = pygame.image.load(path.join(img_folder, 'y-1.png')).convert_alpha()
        self.wall_img2 = pygame.image.load(path.join(img_folder, 'img-3.png')).convert_alpha()

    def generate_enemy(self, num):
        
        with open("map.txt") as file:
            lines = file.readlines()

        #create enemy in random     
        pos = []
        for _ in range(num):
            while True:
                x, y = randrange(0, len(lines[0])), randrange(0, len(lines))
                if lines[y][x] == '.' and [x,y] not in pos:
                    pos.append([x,y])
                    break                

        for p in pos:
            Enemy(self, p[0], p[1])


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.generate_enemy(5)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, 1)
                if tile == '2':
                    Wall(self, col, row, 2)
                if tile == 'P':
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)
    

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            # catch all events here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
            self.update()
            self.draw()
            
    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for hit in hits:
            hit.kill()
    
    def draw(self):
        pygame.display.set_caption(TITLE)
        self.screen.fill(BGCOLOR)
       
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip() 

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))           

        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))  
        

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()