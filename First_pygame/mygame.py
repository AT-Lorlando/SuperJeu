import pygame
import os
import random
import sys

#////////////////////////////////////////////////////////////////////
#INITIALIZE
pygame.init()
pygame.mixer.init()
WIDTH, HEIGTH  = 600, 600

level = 1
lives = 5
score = 0
#DEFINE COLORS
RED = (255,0,0)
GREEN = (0,128,0)
WHITE = (255,255,255)
BLACK = (0,0,0) 

main_font = pygame.font.SysFont("Blue Eyes.otf",30)
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("My First Game")

#BACKGROUND
bg = pygame.transform.scale(pygame.image.load(os.path.join("imgs","background.png")),(WIDTH,HEIGTH))
bgX, bgY = 0,0
bgX2, bgY2 = bg.get_width(), bg.get_height()
#/////////////////////////////////////////////////////////////////////
#PLAYER
class player(object):
    def __init__(self,playerX,playerY,width,height):
        self.playerX = playerX
        self.playerY = playerY
        self.width = width
        self.height = height
        self.change = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.standing = True
        self.walkCount = 0
        self.health = 5
        self.hitbox = (self.playerX + 7, self.playerY + 10, 30, 50)

        #SPRITE OF PLAYER
        self.walkRight = [pygame.transform.scale(pygame.image.load(os.path.join('imgs','img_sprite','R' + str(x) +'.png')),(self.width,self.height)) for x in range(1,10)]
        self.walkLeft = [pygame.transform.scale(pygame.image.load(os.path.join('imgs','img_sprite','L' + str(x) +'.png')),(self.width,self.height)) for x in range(1,10)]
        self.char = pygame.transform.scale(pygame.image.load('imgs/img_sprite/standing.png'),(self.width,self.height))

    def draw(self, screen):
        if self.walkCount +1 >=27:
            self.walkCount = 0
        if not (self.standing):
            if self.left:
                screen.blit(self.walkLeft[self.walkCount//3], (self.playerX,self.playerY))
                self.walkCount += 1
            elif self.right:
                screen.blit(self.walkRight[self.walkCount//3], (self.playerX,self.playerY))
                self.walkCount +=1
        else:
            if self.right:
                screen.blit(self.walkRight[0], (self.playerX, self.playerY))
            else:
                screen.blit(self.walkLeft[0], (self.playerX, self.playerY))
        
        #HEALTH_BAR OF PLAYER
        pygame.draw.rect(screen, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(screen, GREEN, (self.hitbox[0], self.hitbox[1] - 20, 50 - (10 * (5 - self.health)), 10))
        self.hitbox = (self.playerX + 7, self.playerY + 10, 30, 50)
#//////////////////////////////////////////////////////////////////
#ENEMY
class enemy(object):
    def __init__(self, enemyX, enemyY, width, height, end):
        self.enemyX = enemyX
        self.enemyY = enemyY
        self.width = width
        self.height = height
        self.end = end
        self.path = [0, self.end]
        self.walkCount = 0
        self.change = 3
        self.hitbox = (self.enemyX + 7, self.enemyY + 10 , 30, 50)
        self.health = 10
        self.visible = True

        #SPRITE OF ENEMY
        self.walkRight = [pygame.image.load(os.path.join('imgs','img_sprite','R' + str(x) + 'E' + '.png')) for x in range(1,12)]
        self.walkLeft  = [pygame.image.load(os.path.join('imgs','img_sprite','L' + str(x) + 'E' +'.png')) for x in range(1,12)]
    
    def draw(self,screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.change > 0:
                screen.blit(self.walkRight[self.walkCount //3], (self.enemyX, self.enemyY))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount //3], (self.enemyX, self.enemyY))
                self.walkCount += 1
            
            #HEALTH_BAR OF ENEMY
            pygame.draw.rect(screen, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, GREEN, (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.enemyX + 7, self.enemyY + 10, 30, 50)

    def move(self):
        if self.change > 0:
            if self.enemyX + self.change < self.path[1]:
                self.enemyX += self.change
            else:
                self.change = -self.change 
                self.walkCount = 0
        else:
            if self.enemyX - self.change > self.path[0]:
                self.enemyX += self.change
            else:
                self.change = -self.change
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
#///////////////////////////////////////////////////////////////////////////////////
#FIRED OR BULLETS
fireImg = pygame.transform.scale(pygame.image.load(os.path.join("imgs","fire.png")),(16,16))
class fired(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.change = 8 * facing

    def draw(self,screen):
        screen.blit(fireImg,(self.x,self.y))

def redraw_window():
    screen.blit(bg,(bgX,bgY))
    screen.blit(bg,(bgX2,0))

    man.draw(screen)
    goblin.draw(screen)

    #Draw text:
    text = main_font.render(f"Score: {score}", 1, RED)
    screen.blit(text, (390, 10))

    lives_label = main_font.render(f"LIVES: {lives}",1,RED)
    screen.blit(lives_label,(10,10))

    level_label = main_font.render(f"LEVEL: {level}",1,RED)  
    screen.blit(level_label,(WIDTH - level_label.get_width()-10, 10))

    #DRAW BULLET
    for bullet in bullets:
        bullet.draw(screen)
    #UPDATE
    pygame.display.update()

#////////////////////////////////////////////////////////////////////////////
#LOOP GAME
run = True
FPS = 30
clock = pygame.time.Clock()

shootLoop = 0
bullets = []
man = player(300,500,64,64)
goblin = enemy(100,500,64,64,500)
while run:
    redraw_window()
    clock.tick(FPS)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
    
    for bullet in bullets:
        if goblin.visible:
            if bullet.y  > goblin.enemyY and bullet.y  < goblin.enemyY + goblin.height:
                if bullet.x  > goblin.hitbox[0] and bullet.x  < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < WIDTH and bullet.x > 0:
            bullet.x += bullet.change
        else:
            bullets.pop(bullets.index(bullet))
        
    keys = pygame.key.get_pressed()
    #SHOOT
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(fired(man.playerX + man.width //2,man.playerY + man.height//2, facing))
        shootLoop = 1
    #MOVE TO LEFT
    if keys[pygame.K_LEFT] :
        man.playerX -= man.change
        man.left = True
        man.right = False
        man.standing = False
    #MOVE TO RIGHT
    elif keys[pygame.K_RIGHT] :
        if man.playerX > 2*WIDTH/3:
            man.playerX +=0
            bgX -= man.change # Move both background images back
            bgX2 -= man.change
            if bgX <= bg.get_width() * -1:  # If our bg is at the -width then reset its position
                bgX = bg.get_width()
        
            if bgX2 <= bg.get_width() * -1:
                bgX2 = bg.get_width()
        else:
            man.playerX += man.change
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if keys[pygame.K_UP] and man.playerY > man.change:
        man.playerY -= man.change
    if keys[pygame.K_DOWN] and man.playerY < HEIGTH - man.height:
        man.playerY += man.change 
   
    if not(man.isJump):
        #Press A to jump
        if keys[pygame.K_a]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.playerY -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

pygame.quit()
