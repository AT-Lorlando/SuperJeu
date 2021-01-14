import pygame
from os import path
from settings import *
bg = pygame.image.load(path.join(assets_folder,'map.png'))



spell_thunder=path.join(spell_folder,'spell_thunder')
fighticons_folder=path.join(assets_folder,'fighticons')

def load(flip,folderpath,num,scale,rang):
    if flip:
        return [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(folderpath,str(k//num)+'.png')),scale),True,False) for k in range(rang)]
    return [pygame.transform.scale(pygame.image.load(path.join(folderpath,str(k//num)+'.png')),scale)for k in range(rang)]

HealthScale=(60,10)
Health = load(False,health_folder,1,HealthScale,11)

heart = pygame.transform.scale(pygame.image.load(path.join(health_folder,'heart.png')),(100,100))

IconsScale=64,64
Icons = load(False,fighticons_folder,1,IconsScale,2)


###Player###
PlayerScale = (46,64)
Playersprite = pygame.transform.scale(pygame.image.load(path.join(champ_folder,'B1.png')),PlayerScale)
PlayerRight = [pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale) for k in range(9)]
PlayerLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale),True,False) for k in range(9)]

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

Spellscale=(64,64)
Spell_thunder=load(False,spell_thunder,2,Spellscale,20)
