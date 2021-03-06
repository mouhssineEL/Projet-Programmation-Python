from pygame.locals import *
import pygame
from pygame import *
pygame.init()

screen_width = 1000
screen_height = 675

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Age Of INSA')

#font = pygame.font.SysFont('Constantia', 30)
#fdsgdf
background = transform.scale(image.load("../graphics/marron.jpg"), (1000, 675)).convert()

# define colours
bg = (204, 102, 0)
red = (255, 0, 0)
marron = (187, 174, 152)
black = (0, 0, 0)
white = (255, 255, 255)
yellow=(255, 255, 0)

# define global variable
clicked = False
counter = 0

screen.blit(background, (0, 0))

font = pygame.font.Font("../graphics/this.otf", 50)
textsurface = font.render("text", False, (0, 0, 0))


#mixer.music.load("sounds/menu music.wav")
#mixer.music.play(-1)


class button():
    # colours for button and text
    button_col = (204, 102, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 180
    height = 70


    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text



    def draw_button(self):


        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y +5))
        return action


muet = button(500, 180, 'Muet')
quit = button(500, 540, 'Quit')
on = button(500, 300, 'Soud On')
menu = button(500, 420, 'Menue')

def stings():
    from game_menu import menu_game

    run = True
    while run:

        screen.blit(background, (100, 0))


        if muet.draw_button():
            pygame.mixer.music.pause()
        if quit.draw_button():
            pygame.quit()
        if menu.draw_button():
            menu_game()
            #pygame.mixer.music.stop()
        if on.draw_button():
            pygame.mixer.music.unpause()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
