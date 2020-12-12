#!/usr/bin/python
import os
import pygame
import sys
from pygame.locals import *

# set window size
width = 640
height = 500
# barre
height_barre = 10
y_center = 120
ybarre = y_center - height_barre/2
# slider
slider_center = y_center
witdh_slider = 20
height_slider = 120
y_slider = slider_center - height_slider / 2
nb_division = 11

# initilaise pygame
pygame.init()
windowSurfaceObj = pygame.display.set_mode((width, height))  # ,1,16
redColor = pygame.Color(255, 0, 0)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)

# text font
main_font = pygame.font.SysFont("Blue Eyes.otf", 30)

# starting position
x = 100
pygame.draw.rect(windowSurfaceObj, whiteColor, Rect(
    0, ybarre, width, height_barre))  # barre curseur
pygame.draw.rect(windowSurfaceObj, redColor, Rect(
    x, y_slider, witdh_slider, height_slider))  # curseur
pygame.display.update(pygame.Rect(0, 0, width, height))  # background

s = 0
while s == 0:
    button = pygame.mouse.get_pressed()
    if button[0] != 0:
        pos = pygame.mouse.get_pos()
        if y_slider < pos[1] < y_slider + height_slider:
            y = pos[1]
            x = pos[0]

        a = x - 5
        if a < 0:
            a = 0
        if x >= width - witdh_slider:
            x = width - witdh_slider
        # pygame.draw.rect(windowSurfaceObj, blackColor, Rect(
        #    0, 0, width, height))  # background black
        pygame.draw.rect(windowSurfaceObj, whiteColor, Rect(
            0, ybarre, width, height_barre))  # barre curseur
        pygame.draw.rect(windowSurfaceObj, redColor, Rect(
            x, y_slider, witdh_slider, height_slider))  # curseur

        # value of the slider
        value = str(int(x // (width/nb_division)))
        # print(value)

        # text
        font_surface = main_font.render(value, True, whiteColor)
        windowSurfaceObj.blit(font_surface, (100, 200))

    # update
    pygame.display.update()

    # check for ESC key pressed, or pygame window closed, to quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
