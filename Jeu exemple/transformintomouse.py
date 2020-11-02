import pygame
import os
import random
import sys

pygame.init()
class player(object):
    def __init__(self,playerX,playerY,width,heigth):
        self.playerX = playerX
        self.playerY = playerY
        self.width = width
        self.heigth = heigth
        self.change = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount =0
    def draw(self, screen):
        if self.walkCount +1 >=27:
            self.walkCount = 0
        if man.left:
            screen.blit(walkLeft[self.walkCount//3], (self.playerX,self.playerY))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount//3], (self.playerX,self.playerY))
            self.walkCount +=1
        else:
            screen.blit(char, (self.playerX,self.playerY))


WIDTH, HEIGTH  = 600, 600

level = 1
lives = 5
RED = (255,0,0)
main_font = pygame.font.SysFont("Blue Eyes.otf",30)
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("Sprite and Animation")

#IMAGE
walkRight = [pygame.image.load('imgs/img_sprite/R1.png'), pygame.image.load('imgs/img_sprite/R2.png'), pygame.image.load('imgs/img_sprite/R3.png'), pygame.image.load('imgs/img_sprite/R4.png'), pygame.image.load('imgs/img_sprite/R5.png'), pygame.image.load('imgs/img_sprite/R6.png'), pygame.image.load('imgs/img_sprite/R7.png'), pygame.image.load('imgs/img_sprite/R8.png'), pygame.image.load('imgs/img_sprite/R9.png')]
walkLeft = [pygame.image.load('imgs/img_sprite/L1.png'), pygame.image.load('imgs/img_sprite/L2.png'), pygame.image.load('imgs/img_sprite/L3.png'), pygame.image.load('imgs/img_sprite/L4.png'), pygame.image.load('imgs/img_sprite/L5.png'), pygame.image.load('imgs/img_sprite/L6.png'), pygame.image.load('imgs/img_sprite/L7.png'), pygame.image.load('imgs/img_sprite/L8.png'), pygame.image.load('imgs/img_sprite/L9.png')]
char = pygame.image.load('imgs/img_sprite/standing.png')
#BACKGROUND
bg = pygame.image.load(os.path.join("imgs","background2.png"))
indicator= pygame.image.load(os.path.join("imgs","goto.png"))


def redraw_window():
    screen.blit(bg,(0,0))
    man.draw(screen)


    #Draw text:
    lives_label = main_font.render(f"LIVES: {lives}",1,RED)
    level_label = main_font.render(f"LEVEL: {level}",1,RED)
    screen.blit(lives_label,(10,10))
    screen.blit(level_label,(WIDTH - level_label.get_width()-10, 10))
     #pygame.draw.rect(screen,(255,0,255),(100,100,100,100))
    pygame.display.update()

run = True
FPS = 27
clock = pygame.time.Clock()

def goto(x,y):
	screen.blit(indicator,(x,y))
	run  = False
	if man.playerX-x>0:
		xflag=1			#goleft
		man.left=True
	else:
		xflag=-1				#goright
		man.right=False
	if man.playerY-y>0:
		yflag=1				#godown
	else:
		yflag=+1			#goup
	xdist=(man.playerX-x)*xflag
	ydist=(man.playerY-y)*yflag
	length=max(xdist,ydist)//man.change
	print(length)
	xsteps=xdist//length
	ysteps=ydist//length
	for count in range(length+1):
		clock.tick(FPS)

		man.playerX -= xsteps*xflag
		man.playerY -= ysteps*yflag
		redraw_window()

	run  = True
	man.left = False
	man.right = False


man = player(200,200,64,64)
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
        
    keys = pygame.key.get_pressed()
    mouse= pygame.mouse.get_pressed()

    x,y=pygame.mouse.get_pos()
    if mouse[2]:	#Right click
    	x,y=pygame.mouse.get_pos()
    	goto(x,y)
    	
    """
    if keys[pygame.K_LEFT] and man.playerX > man.change:
        man.playerX -= man.change
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.playerX < WIDTH - man.change - man.width:
        man.playerX += man.change
        man.left = False
        man.right = True
    else:
        man.left = False
        man.right = False


    if keys[pygame.K_UP] and man.playerY > man.change:
        man.playerY -= man.change
    if keys[pygame.K_DOWN] and man.playerY < HEIGTH - man.change - man.heigth:
        man.playerY += man.change
        
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
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
    """
    redraw_window()




pygame.quit()