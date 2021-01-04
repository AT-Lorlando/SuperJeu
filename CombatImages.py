import pygame
from os import path
from settings import *
bg = pygame.image.load(path.join(assets_folder,'map.png'))

skeleton_attack = path.join(skeleton_folder, 'sk_attack')
skeleton_dead = path.join(skeleton_folder, 'sk_dead')
skeleton_hit = path.join(skeleton_folder, 'sk_hit')

HealthScale=(60,10)
health =  [pygame.transform.scale(pygame.image.load(path.join(health_folder,str(k)+'.png')),HealthScale) for k in range(12)] 

SkeletonScale=(64,64)
skeletonsprite = pygame.transform.scale(pygame.image.load(path.join(skeleton_folder,'standing.png')),SkeletonScale)
SkeletonAttack = [pygame.transform.scale(pygame.image.load(path.join(skeleton_attack,str(k//2+1)+'.png')),SkeletonScale) for k in range(34)]
SkeletonHit = [pygame.transform.scale(pygame.image.load(path.join(skeleton_hit,str(k//2+1)+'.png')),SkeletonScale) for k in range(14)]
SkeletonDead = [pygame.transform.scale(pygame.image.load(path.join(skeleton_dead,str(k//2+1)+'.png')),SkeletonScale) for k in range(28)]

PlayerScale = (46,64)
char = pygame.transform.scale(pygame.image.load(path.join(champ_folder,'B1.png')),PlayerScale)
walkRight = [pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale) for k in range(9)]
walkLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale),True,False) for k in range(9)]
