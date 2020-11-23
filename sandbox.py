from os import path
import pygame


pygame.init()

run =True
FPS = 60
WIDTH, HEIGTH  = 1097, 720
clock = pygame.time.Clock()

main_font = pygame.font.SysFont("Blue Eyes.otf",50)
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("First screen")
img_dir=path.join(path.dirname(__file__),'Jeu exemple' ,'imgs')
sprite_dir=path.join(img_dir , 'img_sprite')

bg=pygame.image.load(path.join(img_dir,"map.png")).convert_alpha()

run = True
while run :
    screen.blit(bg,(0,0))

    rect = screen.get_rect()
    f = pygame.font.Font(None, 20)
    # screen.fill((10, 10, 10))
    font_surface = main_font.render("   bar", True,(255, 255, 255))
    font_rect = font_surface.get_rect()
    print(font_rect)
    font_rect.topleft = rect.topleft
    screen.blit(font_surface, font_rect, font_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
    
    pygame.display.update()



