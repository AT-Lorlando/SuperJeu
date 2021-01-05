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
        
        if man.left:
            screen.blit(PlayerLeft[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif self.right:
            screen.blit(PlayerRight[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            screen.blit(char, (relativeX, relativeY))

    def drawSkeleton(self, screen):
        relativeX = self.playerX - Skeletoncombathorizontalshift
        if self.faceleft:
            relativeX-=18
        relativeY = self.playerY - Skeletoncombatverticalshift
        
        if self.attackCount==34:
            self.attack=False
            self.attackCount=0
        elif self.attack and self.attackCount<34:
            if self.faceleft:
                screen.blit(SkeletonAttackflip[self.attackCount],(relativeX, relativeY))
            else:
                screen.blit(SkeletonAttack[self.attackCount],(relativeX, relativeY))
            self.attackCount += 1
        if self.hitcount==14:
            self.hit=False
            self.hitcount=0
            if self.healthpoint>1:
                self.healthpoint-=1
            else:
                self.dead=True
        elif self.hit and self.hitcount<14:
            if self.faceleft:
                screen.blit(SkeletonHitflip[self.hitcount],(relativeX, relativeY))
            else:
                screen.blit(SkeletonHit[self.hitcount],(relativeX, relativeY))
            self.hitcount += 1
        elif self.deadcount==28:
            return 8
            #self.dead=False
            #self.deadcount=0
        elif self.dead and self.deadcount<28:
            if self.faceleft:
                screen.blit(SkeletonDeadflip[self.deadcount],(relativeX, relativeY))
            else:
                screen.blit(SkeletonDead[self.deadcount],(relativeX, relativeY))
            
            self.deadcount += 1
        elif self.right:
            screen.blit(SkeletonRight[self.walkCount%24],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif self.left:
            screen.blit(SkeletonLeft[self.walkCount%24],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif not any ([self.dead,self.attack,self.hit]) and not self.dead:
            if not self.faceleft:
                screen.blit(skeletonsprite, (relativeX, relativeY))
            else:
                screen.blit(skeletonsrpiteflip, (relativeX, relativeY))



    
    def drawGobelin(self, screen):
        pospix = (self.playerX - Gobelincombathorizontalshift,self.playerY - Gobelincombatverticalshift)
        animator=[(GobelinDeadflip,GobelinDead,16),(GobelinAttackflip,GobelinAttack,16),(GobelinHitflip,GobelinHit,8),(GobelinBomb,GobelinBomb,38)]
        for k in range(4):
            if self.animation[k]:
                if self.faceleft:
                    data=animator[k][0],animator[k][2]
                    
                else:
                    data=animator[k][1],animator[k][2]
                print(animator[k][2])
                self.animate(screen,k,*data,pospix)
        """ if self.animation[0]:                                                   #Dead
            if self.faceleft:
                self.animate(screen,0,GobelinDeadflip,16,pospix)
            else:
                self.animate(screen,0,GobelinDead,16,pospix)
        elif self.animation[1]:                                                 #Attack
            if self.faceleft:
                self.animate(screen,1,GobelinAttackflip,16,pospix)
            else:
                self.animate(screen,1,GobelinAttack,16,pospix)
            
        elif self.animation[2]:                                                 #Hit
            if self.faceleft:
                self.animate(screen,2,GobelinHitflip,8,pospix)        
            else:
                self.animate(screen,2,GobelinHit,8,pospix)        
                             
        elif self.animation[3]:                                                 #Bomb
            self.animate(screen,3,GobelinBomb,38,pospix)
        """
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
        elif self.animation[nanimation] and self.countdown<38:
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

