from Hex import *
import pygame
from settings import *
from CombatImages import *

class player(object):
    def __init__(self, playerX, playerY,name):
        self.name=name
        self.Xshift=0
        self.Yshift=0
        self.playerX = playerX
        self.playerY = playerY
        self.change = 5*GoldenX
        self.maxmovement=0
        self.movementpoints=0
        self.healthpoint=100
        self.faceleft=False
        self.poshex=Tile().set_object(self)
        self.animation=[False,False,False]#Dead #Attack #Hit 
        self.spells=[False,False,False,False] #
        self.spellsname=[]
        self.spellpos=Hex()
        self.activespell=None
        self.left = False
        self.right = False
        self.walkCount = 0
        self.maxmana=10
        self.mana=10
        self.countdown=0
        self.animator=[]
        self.ranged=False


    def draw(self,screen):
        pospix = (self.playerX - self.Xshift,self.playerY - self.Yshift)
        #Init ##self.animator=[(GobelinDeadflip,GobelinDead,16),(GobelinAttackflip,GobelinAttack,16),(GobelinHitflip,GobelinHit,8),(GobelinBomb,GobelinBomb,37)]
        #Init ##self.spellsanimations=[(GobelinAttackflip,GobelinAttack,16)]
        #Init ##self.static=[GobelinRight,GobelinLeft,18,Gobelinsprite,Gobelinsrpiteflip]
        for k in range(len(self.animation)):
            if self.animation[k]:
                if self.faceleft:
                    data=self.animator[k][0],self.animator[k][2]
                else:
                    data=self.animator[k][1],self.animator[k][2]
                self.animate(screen,self.animation,k,*data,pospix)
        
        if self.right:
            screen.blit(self.static[0][self.walkCount%self.static[2]],pospix)
            self.walkCount += 1
        elif self.left:
            screen.blit(self.static[1][self.walkCount%self.static[2]],pospix)
            self.walkCount += 1

        elif not (any(self.animation)or any(self.spells) or self.right or self.left) or self.ranged:              #Static
            if not self.faceleft:
                screen.blit(self.static[3], pospix)
            else:
                screen.blit(self.static[4], pospix)

        for k in range(len(self.spells)):
            if self.spells[k]:
                
                if self.faceleft:
                    data=self.spellsanimations[k][0],self.spellsanimations[k][2]
                else:
                    data=self.spellsanimations[k][1],self.spellsanimations[k][2]
                if self.ranged:
                    *a,x,y=self.spellpos
                    pospix=(x-self.spellsname[0].offsetx*3,y-self.spellsname[0].offsety*3)
                self.animate(screen,self.spells,k,*data,(pospix))
            
      
            
    def animate(self,screen,animalist,nanimation,playeranimation,count,position):
        if self.countdown==count:
            if nanimation!=0 or animalist!=self.animation:
                animalist[nanimation]=False
                self.countdown=0
        elif animalist[nanimation] and self.countdown<count:
            screen.blit(playeranimation[self.countdown],position)
            self.countdown += 1


    def deal_damage(self,damage):
        self.healthpoint-=damage
        #Scriptprint(self.name+ " hit, -"+str(damage)+" HP")
        if damage>0:
            self.animation[2]=True
        if self.healthpoint<=0:
            self.animation[0]=True
            self.healthpoint=0
        elif self.healthpoint>100:
            self.healthpoint=100



layout = Layout(orientation_pointy, (largeurHex, hauteurHex),(
    0+(0.5*size[0]-largeurHex*(Column-0.5)),
    0+(0.4*size[1]-hauteurHex*(1.5*Line-1)/2)
    ))


pospix = hex_to_pixel(layout, Hex(5,1))
man = player(pospix[0], pospix[1],"Archer")
man.poshex = Tile(Hex(5, 1)).set_object(man)
man.maxmana=6
man.mana=6
man.movementpoints=4
man.maxmovement=4
man.Xshift=Playercombathorizontalshift
man.Yshift=Playercombatverticalshift

skeleton = player(hex_to_pixel(layout,Hex(0, 4))[0],hex_to_pixel(layout,Hex(0, 4))[1],"Skeleton")
skeleton.poshex = Tile(Hex(0, 4)).set_object(skeleton)
skeleton.maxmovement=3
skeleton.Xshift=Skeletoncombathorizontalshift
skeleton.Yshift=Skeletoncombatverticalshift

gobelin = player(hex_to_pixel(layout,Hex(2, 3))[0],hex_to_pixel(layout,Hex(2, 3))[1],"Gobelin")
gobelin.poshex = Tile(Hex(2, 3)).set_object(gobelin)
gobelin.mana=2
gobelin.maxmana=2
gobelin.maxmovement=8
gobelin.Xshift=Gobelincombathorizontalshift
gobelin.Yshift=Gobelincombatverticalshift