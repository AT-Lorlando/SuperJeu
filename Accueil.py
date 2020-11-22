
import pygame

class Button(pygame.sprite.Sprite) :
    def __init__(self,pos_x,pos_y,image,image_clicked) :
        super(Button, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.image_clicked=image_clicked
        self.print = image
        self.rect = image.get_size()
        self.clicked = False
        print("rect=",self.rect)

    def is_clicked(self,mouse,pos_mouse):
        return (mouse and self.pos_x < pos_mouse[0]< self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1]< self.pos_y + self.rect[1])

    def draw_clicked(self):
        self.print = self.image_clicked
    
    def draw_not_clicked(self):
        self.print = self.image
    
    def update(self,mouse,pos_mouse):
        if self.is_clicked(mouse,pos_mouse):
            self.draw_clicked()
            self.clicked = True
        else :
            self.draw_not_clicked()

    def draw(self,screen):
        screen.blit(self.print, (self.pos_x,self.pos_y))

def accueil(screen,bg,buttons,mouse,x,y,play,game_launch,exit):
    screen.blit(bg,(0,0)) #Background
    if play.clicked :
        if mouse[0] and not game_launch:
            buttons.update(mouse[0],(x,y))
            for button  in buttons:
                button.draw(screen)
        else:
            game_launch = True
            return "game"
    else:
        buttons.update(mouse[0],(x,y))
        for button  in buttons:
            button.draw(screen)
    
    if exit.clicked :
        if mouse[0] and not game_launch:
            buttons.update(mouse[0],(x,y))
            for button  in buttons:
                button.draw(screen)
        else:
            return "exit"
    else:
        buttons.update(mouse[0],(x,y))
        for button  in buttons:
            button.draw(screen)
    	

    pygame.display.update()