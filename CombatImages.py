import pygame
from os import path
from settings import *
bg = pygame.image.load(path.join(assets_folder,'map.png'))

skeleton_attack = path.join(skeleton_folder, 'sk_attack')
skeleton_dead = path.join(skeleton_folder, 'sk_dead')
skeleton_hit = path.join(skeleton_folder, 'sk_hit')
skeleton_walk = path.join(skeleton_folder, 'sk_walk')

gobelin_attack = path.join(gobelin_folder, 'gobelin_attack')
gobelin_dead = path.join(gobelin_folder, 'gobelin_dead')
gobelin_hit = path.join(gobelin_folder, 'gobelin_hit')
gobelin_walk = path.join(gobelin_folder, 'gobelin_walk')
gobelin_bomb = path.join(gobelin_folder, 'gobelin_bomb')

HealthScale=(60,10)
health =  [pygame.transform.scale(pygame.image.load(path.join(health_folder,str(k)+'.png')),HealthScale) for k in range(12)] 

SkeletonScale=(64,64)
skeletonsprite = pygame.transform.scale(pygame.image.load(path.join(skeleton_folder,'standing.png')),SkeletonScale)
skeletonsrpiteflip = pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(skeleton_folder,'standing.png')),SkeletonScale),True,False)
SkeletonAttack = [pygame.transform.scale(pygame.image.load(path.join(skeleton_attack,str(k//2)+'.png')),SkeletonScale) for k in range(36)]
SkeletonAttackflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(skeleton_attack,str(k//2)+'.png')),SkeletonScale),True,False) for k in range(36)]
SkeletonHit = [pygame.transform.scale(pygame.image.load(path.join(skeleton_hit,str(k//2)+'.png')),SkeletonScale) for k in range(16)]
SkeletonHitflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(skeleton_hit,str(k//2)+'.png')),SkeletonScale),True,False) for k in range(16)]
SkeletonDead = [pygame.transform.scale(pygame.image.load(path.join(skeleton_dead,str(k//2)+'.png')),SkeletonScale) for k in range(30)]
SkeletonDeadflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(skeleton_dead,str(k//2)+'.png')),SkeletonScale),True,False) for k in range(30)]
SkeletonRight = [pygame.transform.scale(pygame.image.load(path.join(skeleton_walk,str(k//2)+'.png')),SkeletonScale) for k in range(26)]
SkeletonLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(skeleton_walk,str(k//2)+'.png')),SkeletonScale),True,False) for k in range(26)]

PlayerScale = (46,64)
char = pygame.transform.scale(pygame.image.load(path.join(champ_folder,'B1.png')),PlayerScale)
PlayerRight = [pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale) for k in range(9)]
PlayerLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale),True,False) for k in range(9)]

GobelinScale=(88,64)
Gobelinsprite = pygame.transform.scale(pygame.image.load(path.join(gobelin_folder,'standing.png')),GobelinScale)
Gobelinsrpiteflip = pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(gobelin_folder,'standing.png')),GobelinScale),True,False)
GobelinAttack = [pygame.transform.scale(pygame.image.load(path.join(gobelin_attack,str(k//2)+'.png')),GobelinScale) for k in range(16)]
GobelinAttackflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(gobelin_attack,str(k//2)+'.png')),GobelinScale),True,False) for k in range(16)]
GobelinHit = [pygame.transform.scale(pygame.image.load(path.join(gobelin_hit,str(k//2)+'.png')),GobelinScale) for k in range(8)]
GobelinHitflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(gobelin_hit,str(k//2)+'.png')),GobelinScale),True,False) for k in range(8)]
GobelinDead = [pygame.transform.scale(pygame.image.load(path.join(gobelin_dead,str(k//4)+'.png')),GobelinScale) for k in range(16)]
GobelinDeadflip = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(gobelin_dead,str(k//4)+'.png')),GobelinScale),True,False) for k in range(16)]
GobelinBomb = [pygame.transform.scale(pygame.image.load(path.join(gobelin_bomb,str(k//2)+'.png')),GobelinScale) for k in range(38)]
GobelinRight = [pygame.transform.scale(pygame.image.load(path.join(gobelin_walk,str(k//2)+'.png')),GobelinScale) for k in range(18)]
GobelinLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(gobelin_walk,str(k//2)+'.png')),GobelinScale),True,False) for k in range(18)]
