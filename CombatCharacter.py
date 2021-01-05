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
        
        self.healthpoint=10
        self.faceleft=False
        self.poshex=Hex(0,0)
        self.animation=[False,False,False,False]#Dead #Hit #Bomb
        
        self.left = False
        self.right = False
        self.walkCount = 0

        self.countdown=0

    def drawPlayer(self, screen):
        relativeX = self.playerX - Playercombathorizontalshift
        relativeY = self.playerY - Playercombatverticalshift
        pospix=relativeX,relativeY
        
        if man.left:
            screen.blit(PlayerLeft[self.walkCount%9],pospix)
            self.walkCount += 1
        elif self.right:
            screen.blit(PlayerRight[self.walkCount%9],pospix)
            self.walkCount += 1
        else:
            screen.blit(char, (relativeX, relativeY))

    def drawSkeleton(self, screen):
        relativeX = self.playerX - Skeletoncombathorizontalshift
        if self.faceleft:
            relativeX-=18
        relativeY = self.playerY - Skeletoncombatverticalshift
        pospix = (relativeX,relativeY)
        animator=[(SkeletonDeadflip,SkeletonDead,30),(SkeletonAttackflip,SkeletonAttack,36),(SkeletonHitflip,SkeletonHit,16),(SkeletonShield,SkeletonShield,38)]
        for k in range(4):
            if self.animation[k]:
                if self.faceleft:
                    data=animator[k][0],animator[k][2]
                else:
                    data=animator[k][1],animator[k][2]
                self.animate(screen,k,*data,pospix)
        
        if self.right:
            screen.blit(SkeletonRight[self.walkCount%24],pospix)
            self.walkCount += 1
        elif self.left:
            screen.blit(SkeletonLeft[self.walkCount%24],pospix)
            self.walkCount += 1

        elif not (any(self.animation) or self.right or self.left):              #Static
            if not self.faceleft:
                screen.blit(skeletonsprite, pospix)
            else:
                screen.blit(skeletonsrpiteflip, pospix)
    
    def drawGobelin(self, screen):
        pospix = (self.playerX - Gobelincombathorizontalshift,self.playerY - Gobelincombatverticalshift)
        animator=[(GobelinDeadflip,GobelinDead,16),(GobelinAttackflip,GobelinAttack,16),(GobelinHitflip,GobelinHit,8),(GobelinBomb,GobelinBomb,37)]
        for k in range(4):
            if self.animation[k]:
                if self.faceleft:
                    data=animator[k][0],animator[k][2]
                else:
                    data=animator[k][1],animator[k][2]
                self.animate(screen,k,*data,pospix)
        
        if self.right:
            screen.blit(GobelinRight[self.walkCount%18],pospix)
            self.walkCount += 1
        elif self.left:
            screen.blit(GobelinLeft[self.walkCount%18],pospix)
            self.walkCount += 1

        elif not (any(self.animation) or self.right or self.left):              #Static
            if not self.faceleft:
                screen.blit(Gobelinsprite, pospix)
            else:
                screen.blit(Gobelinsrpiteflip, pospix)
            
    def animate(self,screen,nanimation,playeranimation,count,position):
        if self.countdown==count:
            if nanimation !=0:
                self.animation[nanimation]=False
                self.countdown=0
        elif self.animation[nanimation] and self.countdown<count:
            screen.blit(playeranimation[self.countdown],position)
            self.countdown += 1
        

layout = Layout(orientation_pointy, (largeurHex, hauteurHex), (165, 165))

pospix = hex_to_pixel(layout, Hex(5,1))
man = player(pospix[0], pospix[1], *PlayerScale)
man.poshex = Hex(5, 1)

skeleton = player(hex_to_pixel(layout,Hex(0, 4))[0],hex_to_pixel(layout,Hex(0, 4))[1],*SkeletonScale)
skeleton.poshex = Hex(0, 4)

gobelin = player(hex_to_pixel(layout,Hex(2, 3))[0],hex_to_pixel(layout,Hex(2, 3))[1],*GobelinScale)
gobelin.poshex = Hex(2, 3)

Characters=[man,skeleton,gobelin]

