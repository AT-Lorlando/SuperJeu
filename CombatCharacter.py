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
        self.mouvementpoints=4
        self.healthpoint=10
        self.faceleft=False
        self.poshex=Tile().set_object(self)
        self.animation=[False,False,False,False]#Dead #Attack #Hit 
        self.spells=[False,False,False] #
        self.spellsname=[]
        self.spellpos=Hex(0,0)
        self.left = False
        self.right = False
        self.walkCount = 0

        self.countdown=0

    def drawPlayer(self, screen):
        relativeX = self.playerX - Playercombathorizontalshift
        relativeY = self.playerY - Playercombatverticalshift
        pospix=relativeX,relativeY
        spellsanimations=[(Spell_thunder,Spell_thunder,20)]
        
        

        if self.animation[2]:
            self.animation[2]=False
            pygame.time.delay(100)
        if self.left:
            screen.blit(PlayerLeft[self.walkCount%9],pospix)
            self.walkCount += 1
        elif self.right:
            screen.blit(PlayerRight[self.walkCount%9],pospix)
            self.walkCount += 1
        else:
            screen.blit(Playersprite, (relativeX, relativeY))

        for k in range(1):
            if self.spells[k]:
                
                if self.faceleft:
                    data=spellsanimations[k][0],spellsanimations[k][2]
                else:
                    data=spellsanimations[k][1],spellsanimations[k][2]
                
                self.animate2(screen,k,*data,self.spellpos)

    def drawSkeleton(self, screen):
        relativeX = self.playerX - Skeletoncombathorizontalshift
        if self.faceleft:
            relativeX-=18
        relativeY = self.playerY - Skeletoncombatverticalshift
        pospix = (relativeX,relativeY)
        animator=[(SkeletonDeadflip,SkeletonDead,30),(SkeletonAttackflip,SkeletonAttack,36),(SkeletonHitflip,SkeletonHit,16),(SkeletonShieldflip,SkeletonShield,38)]
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
                screen.blit(Skeletonsprite[0], pospix)
            else:
                screen.blit(Skeletonsrpiteflip[0], pospix)
    
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
                screen.blit(Gobelinsprite[0], pospix)
            else:
                screen.blit(Gobelinsrpiteflip[0], pospix)
            
    def animate(self,screen,nanimation,playeranimation,count,position):
        if self.countdown==count:
            if nanimation !=0:
                self.animation[nanimation]=False
                self.countdown=0
        elif self.animation[nanimation] and self.countdown<count:
            screen.blit(playeranimation[self.countdown],position)
            self.countdown += 1

    def animate2(self,screen,nanimation,playeranimation,count,position):
        if self.countdown==count:
            self.spells[nanimation]=False
            self.countdown=0
        elif self.spells[nanimation] and self.countdown<count:
            *a,x,y=position
            screen.blit(playeranimation[self.countdown],(x-self.spellsname[0].offsetx,y-self.spellsname[0].offsety))
            self.countdown += 1


    
    def deal_damage(self,damage):
        self.healthpoint-=damage
        if self.healthpoint<=0:
            self.animation[0]=True




