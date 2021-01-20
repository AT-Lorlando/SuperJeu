import pygame
from os import path
from settings import *
pygame.init()
size = pygame.display.list_modes()[PYGAMESIZE]
SHIFT=0.8
GoldenX=size[0]/1360
GoldenY=size[1]/768


scale=int(size[0]*SHIFT),int(size[1]*SHIFT)
bg = pygame.transform.scale(pygame.image.load(path.join(assets_folder,'test.png')),scale)

spell_thunder=path.join(spell_folder,'spell_thunder')
spell_sunburn=path.join(spell_folder,'spell_sunburn')
spell_bomb=path.join(spell_folder,'spell_bomb')
spell_heal=path.join(spell_folder,'spell_heal')
fighticons_folder=path.join(assets_folder,'fighticons')
rocks_folder=path.join(fighticons_folder,'rock')
end_button_folder=path.join(fighticons_folder,'turn_button')

def load(flip,folderpath,num,scale,rang):
    a,b=int(scale[0]*GoldenX),int(scale[1]*GoldenY)
    if flip:
        return [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(folderpath,str(k//num)+'.png')),(a,b)),True,False) for k in range(rang)]
    return [pygame.transform.scale(pygame.image.load(path.join(folderpath,str(k//num)+'.png')),(a,b))for k in range(rang)]

def loadJerem(flip,folderpath,letter,num,scale,rang):
    a,b=int(scale[0]*GoldenX),int(scale[1]*GoldenY)
    if flip:
        return [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(folderpath,letter+str(k//num)+'.png')),(a,b)),True,False) for k in range(rang)]
    return [pygame.transform.scale(pygame.image.load(path.join(folderpath,letter+str(k//num)+'.png')),(a,b))for k in range(rang)]

###Archer###

PlayerScale = (60,60)
Playersprite = loadJerem(False,hunter_folder,'B',1,PlayerScale,2)
PlayerRight = loadJerem(False,hunter_folder,'R',3,PlayerScale,9)
PlayerLeft =loadJerem(False,hunter_folder,'L',3,PlayerScale,9)

""" Playersprite = loadJerem(False,dark_wizard_folder,'B',1,PlayerScale,2)
PlayerRight = loadJerem(False,dark_wizard_folder,'R',3,PlayerScale,9)
PlayerLeft =loadJerem(False,dark_wizard_folder,'L',3,PlayerScale,9) """
""" 
Playersprite = loadJerem(False,sun_wizard_folder,'B',1,PlayerScale,2)
PlayerRight = loadJerem(False,sun_wizard_folder,'R',3,PlayerScale,9)
PlayerLeft =loadJerem(False,sun_wizard_folder,'L',3,PlayerScale,9) """

###Skeleton###
SkeletonScale=(64,64)
skeleton_attack = path.join(skeleton_folder, 'sk_attack')
skeleton_dead = path.join(skeleton_folder, 'sk_dead')
skeleton_hit = path.join(skeleton_folder, 'sk_hit')
skeleton_walk = path.join(skeleton_folder, 'sk_walk')
skeleton_shield = path.join(skeleton_folder, 'sk_shield')

Skeletonsprite=load(False,skeleton_folder,1,SkeletonScale,1)
Skeletonsrpiteflip=load(True,skeleton_folder,1,SkeletonScale,1)
SkeletonAttack=load(False,skeleton_attack,2,SkeletonScale,36)
SkeletonAttackflip=load(True,skeleton_attack,2,SkeletonScale,36)
SkeletonHit=load(False,skeleton_hit,2,SkeletonScale,16)
SkeletonHitflip=load(True,skeleton_hit,2,SkeletonScale,16)
SkeletonDead=load(False,skeleton_dead,2,SkeletonScale,30)
SkeletonDeadflip=load(True,skeleton_dead,2,SkeletonScale,30)
SkeletonShield = load(False,skeleton_shield,2,SkeletonScale,38)
SkeletonShieldflip = load(True,skeleton_shield,2,SkeletonScale,38)
SkeletonRight=load(False,skeleton_walk,2,SkeletonScale,26)
SkeletonLeft=load(True,skeleton_walk,2,SkeletonScale,26)

###Gobelin###
GobelinScale=(88,64)
gobelin_attack = path.join(gobelin_folder, 'gobelin_attack')
gobelin_dead = path.join(gobelin_folder, 'gobelin_dead')
gobelin_hit = path.join(gobelin_folder, 'gobelin_hit')
gobelin_walk = path.join(gobelin_folder, 'gobelin_walk')
gobelin_bomb = path.join(gobelin_folder, 'gobelin_bomb')

Gobelinsprite=load(False,gobelin_folder,1,GobelinScale,1)
Gobelinsrpiteflip=load(True,gobelin_folder,1,GobelinScale,1)
GobelinAttack=load(False,gobelin_attack,2,GobelinScale,16)
GobelinAttackflip=load(True,gobelin_attack,2,GobelinScale,16)
GobelinHit=load(False,gobelin_hit,2,GobelinScale,8)
GobelinHitflip=load(True,gobelin_hit,2,GobelinScale,8)
GobelinDead=load(False,gobelin_dead,4,GobelinScale,16)
GobelinDeadflip=load(True,gobelin_dead,4,GobelinScale,16)
GobelinBomb = load(False,gobelin_bomb,2,GobelinScale,38)
GobelinRight=load(False,gobelin_walk,2,GobelinScale,18)
GobelinLeft=load(True,gobelin_walk,2,GobelinScale,18)


#Spells
Spellscale=(64*3,64*2)
Spell_thunder=load(False,spell_thunder,2,Spellscale,20)
Spell_sunburn=load(False,spell_sunburn,2,Spellscale,18)
Spell_bomb=load(False,spell_bomb,2,Spellscale,20)
Spell_heal=load(False,spell_heal,2,Spellscale,24)



Spellbar= loadJerem(False,spell_folder,'spellbar',1,(558,70),1)[0]
SpelliconsScale=(50,50)
Spell_icons=load(False,spell_folder,1,SpelliconsScale,4)
Dialog = loadJerem(False,spell_folder,'dialog',1,(127,64),1)[0]
DialogIconsScale = (20,20)
Aim = loadJerem(False,spell_folder,'Aim',1,DialogIconsScale,1)[0]
Range= loadJerem(False,spell_folder,'Range',1,DialogIconsScale,1)[0]
Sword = loadJerem(False,spell_folder,'Sword',1,DialogIconsScale,1)[0]
Medicine = loadJerem(False,spell_folder,'Medicine',1,DialogIconsScale,1)[0]


heart = load(False,health_folder,1,(100,100),1)[0]

Rocks= load(False,rocks_folder,1,(64,61),3)



IconsScale=(40,40)
Icons = load(False,fighticons_folder,1,IconsScale,2)

End_button = load(False,end_button_folder,1,(90,50),4)

Playercombathorizontalshift=int(Playercombathorizontalshift*GoldenX)
Playercombatverticalshift=int(Playercombatverticalshift*GoldenY)

Skeletoncombathorizontalshift=int(Skeletoncombathorizontalshift*GoldenX)
Skeletoncombatverticalshift=int(Skeletoncombatverticalshift*GoldenY)

Gobelincombathorizontalshift=int(Gobelincombathorizontalshift*GoldenX)
Gobelincombatverticalshift=int(Gobelincombatverticalshift*GoldenY)