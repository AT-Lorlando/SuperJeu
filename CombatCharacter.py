from Hex import *
import pygame
from settings import *
from CombatImages import *


class player(object):
    def __init__(self, playerX, playerY, width, heigth):
        self.playerX = playerX
        self.playerY = playerY
        self.width = width
        self.heigth = heigth
        self.change = 5
        self.attack=False
        self.attackCount = 0
        self.dead=False
        self.deadcount = 0
        self.hit=False
        self.hitcount=0
        
        self.left = False
        self.right = False
        self.walkCount = 0
        self.CenterX = self.width // 2
        self.CenterY = self.heigth // 2 + 8

    def drawPlayer(self, screen):
        relativeX = self.playerX - Playercombathorizontalshift
        relativeY = self.playerY - Playercombatverticalshift
        
        if man.left:
            screen.blit(walkLeft[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            screen.blit(char, (relativeX, relativeY))

    def drawSkeleton(self, screen):
        relativeX = self.playerX - Skeletoncombathorizontalshift
        relativeY = self.playerY - Skeletoncombatverticalshift
        
        if self.attackCount==34:
            self.attack=False
            self.attackCount=0
        elif self.attack and self.attackCount<34:
            screen.blit(SkeletonAttack[self.attackCount],(relativeX, relativeY))
            self.attackCount += 1
        if self.hitcount==14:
            self.hit=False
            self.hitcount=0
        elif self.hit and self.hitcount<14:
            screen.blit(SkeletonHit[self.hitcount],(relativeX, relativeY))
            self.hitcount += 1
        elif self.deadcount==28:
            self.dead=False
            self.deadcount=0
        elif self.dead and self.deadcount<28:
            screen.blit(SkeletonDead[self.deadcount],(relativeX, relativeY))
            self.deadcount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            print(8)
            #screen.blit(skeletonsprite, (relativeX, relativeY))

layout = Layout(orientation_pointy, (largeurHex, hauteurHex), (165, 165))
poshex = Hex(0, 1)
pospix = hex_to_pixel(layout, poshex)
man = player(pospix[0], pospix[1], 64, 64)
skeleton = player(hex_to_pixel(layout,Hex(0, 4))[0],hex_to_pixel(layout,Hex(0, 4))[1],64,64)



Characters=[man,skeleton]



