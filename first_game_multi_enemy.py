import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

#create the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#Background
background = pygame.image.load('imgs/background.png')

#Background Sound
mixer.music.load('sound/background.wav')
mixer.music.play(-1) 


#Title and Icon
pygame.display.set_caption("Baby Dragon")
icon = pygame.image.load('imgs/dragon_red.png')
pygame.display.set_icon(icon)

#score_value
score_value = 0
font = pygame.font.Font('Blue Eyes.otf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,0,0))
    screen.blit(score,(x,y))

#Game over text
game_over_font = pygame.font.Font('Blue Eyes.otf',64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text,(350,250))


#Player
playerImg = pygame.image.load('imgs/blue_dragon.png')
playerX = 400
playerY = SCREEN_HEIGHT - 70
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('imgs/plane.png'))
    enemyX.append(random.randint(0,SCREEN_WIDTH-64))
    enemyY.append(random.randint(0,int(SCREEN_HEIGHT/3)))
    enemyX_change.append(2) 
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#fire
#Ready_state- Can't see the fire on screen.
fireImg = pygame.image.load('imgs/fire.png')
fireX = 0
fireY = 480 
fireY_change = 5
fire_state = "ready"

def fire_fire(x,y):
    global fire_state
    fire_state = "fire"
    screen.blit(fireImg,(x+16,y+10))

def isCollision(enemyX,enemyY,fireX,fireY):
    distance = math.sqrt(math.pow(enemyX-fireX,2)+math.pow(enemyY - fireY,2))
    if distance < 30:
        return True
    else: 
        return False

#Game Loop
running = True
while running:

    #RGB -red,green,blue
    screen.fill((0,255,255))
    #backgroundimage
    screen.blit(background,(0,0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False

        #Move of player
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                playerX_change = -2
            if event.key ==pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                fire_sound = mixer.Sound('sound/laser.wav')
                fire_sound.play()
                if fire_state == "ready":
                    fireX = playerX
                    fire_fire(fireX,fireY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 
    
    #Checking the boundaries of player and enemy
    #Player mouvement
    playerX += playerX_change
    if playerX <= 0:
        playerX =0
    elif playerX >= SCREEN_WIDTH - 64: #64 is width of image of player
        playerX = SCREEN_WIDTH -64

    #Enemy mouvement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >= playerY-50:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= SCREEN_WIDTH - 64: 
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],fireX,fireY)
        if collision:
            collision_sound = mixer.Sound('sound/explosion.wav')
            collision_sound.play()
            fireY = 480
            fire_state = "ready"
            score_value +=1
            enemyX[i] = random.randint(0,SCREEN_WIDTH-64)
            enemyY[i] = random.randint(0,int(SCREEN_HEIGHT/3))
        
        enemy(enemyX[i],enemyY[i],i)
        
    #fire mouvement
    if fireY <=0:
        fireY = 480
        fire_state = "ready"
    if fire_state == "fire":
        fire_fire(fireX,fireY)
        fireY -= fireY_change  
    
    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()