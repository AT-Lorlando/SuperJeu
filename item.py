import pygame

class Item(pygame.sprite.Sprite) :
    def __init__(self,image,pos_x,pos_y,name) :
        super(Item, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = image.get_size()
        self.centerx = pos_x + self.rect[0]/2
        self.centery = pos_y + self.rect[1]/2
        self.image = image
        self.print = image
        self.name = name
    
    # Is true if the mouse is over the sprite
    def is_over(self,pos_mouse) :
        return self.pos_x < pos_mouse[0]< self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1]< self.pos_y + self.rect[1]
    
    #Is true if the user click on the sprite
    def is_clicked(self,mouse,pos_mouse):
        return (mouse and self.pos_x < pos_mouse[0]< self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1]< self.pos_y + self.rect[1])


    def update(self,mouse,pos_mouse):
        #If you click on the item, it will follows the cursor and becomes bigger
        if self.is_clicked(mouse,pos_mouse):
            self.pos_x=pos_mouse[0] - self.rect[0]/2
            self.pos_y=pos_mouse[1] - self.rect[1]/2
            self.print=pygame.transform.scale(self.image,(self.rect[0]+5,self.rect[1]+5))
        else :
            self.print = self.image

    #Draw the image at the position given
    def draw(self,screen):
        screen.blit(self.print, (self.pos_x,self.pos_y))

class Stuff(Item) :
    def __init__(self,STR,DEX,CON,INT,WIS,CHA) :
        super(Stuff, self).__init__()
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        
class Consumable(Item):
    def __init__(self,health):
        super(Stuff, self).__init__()
        self.health = health #