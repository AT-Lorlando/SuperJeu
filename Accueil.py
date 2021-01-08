import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, image_clicked, name):
        super(Button, self).__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.image_clicked = image_clicked
        self.print = image
        self.rect = image.get_size()
        self.clicked = False
        self.name = name

    def is_clicked(self, mouse, pos_mouse):
        return (mouse and self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1])

    def draw_clicked(self):
        self.print = self.image_clicked

    def draw_not_clicked(self):
        self.print = self.image

    def update(self, mouse, pos_mouse):
        if self.is_clicked(mouse, pos_mouse):
            self.draw_clicked()
            self.clicked = True
        else:
            self.draw_not_clicked()

    def draw(self, screen):
        screen.blit(self.print, (self.pos_x, self.pos_y))

    def is_over(self, pos_mouse):
        return self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1]


def accueil(screen, bg, buttons, mouse, x, y, play, game_launch, exit, main_font, dialogue, options, resume):
    screen.blit(bg, (0, 0))  # Background

    buttons.update(mouse[0], (x, y))
    for button in buttons:
        button.draw(screen)
        # print(button.name)

    if play.clicked:
        if mouse[0] and not game_launch:
            buttons.update(mouse[0], (x, y))
            for button in buttons:
                button.draw(screen)
        else:
            game_launch = True
            return "game_launch"

    if exit.clicked:
        if mouse[0] and not game_launch:
            buttons.update(mouse[0], (x, y))
            for button in buttons:
                button.draw(screen)
        else:
            return "exit"

    if options.clicked:
        if mouse[0] and not game_launch:
            buttons.update(mouse[0], (x, y))
            for button in buttons:
                button.draw(screen)
        else:
            return "options"

    if resume.clicked:
        if mouse[0] and not game_launch:
            buttons.update(mouse[0], (x, y))
            for button in buttons:
                button.draw(screen)
        else:
            return "resume"

    if play.is_over((x, y)):
        print_text(screen, main_font, x, y, "Create a game", dialogue)

    if exit.is_over((x, y)):
        print_text(screen, main_font, x, y, "Exit the game", dialogue)

    if options.is_over((x, y)):
        print_text(screen, main_font, x, y, "Open the options panel", dialogue)

    if play.is_over((x, y)):
        print_text(screen, main_font, x, y, "Load a game", dialogue)


def print_text(screen, main_font, x, y, text, dialogue):

    font_surface = main_font.render(text, True, (255, 255, 255))
    font_size = [font_surface.get_rect()[2], font_surface.get_rect()[3]]
    dialogue = pg.transform.scale(dialogue, (font_size[0]+15, font_size[1]+20))
    screen.blit(dialogue, (x-40, y+20))
    screen.blit(font_surface, (x-35, y+40))
