
import pygame as pg


class Camera:

    def __init__(self, width, height):

        self.width = width
        self.height = height
# position de camera au debut du jeu
        self.scroll = pg.Vector2(-1900, -1080)
        self.dx = 0
        self.dy = 0
#vitesse de mouvement
        self.speed = 15

    def update(self):

        mouse_pos = pg.mouse.get_pos()

        # x movement
        if mouse_pos[0] > self.width * 0.97:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:
            self.dx = self.speed
        else:
            self.dx = 0

        # y movement
        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.05:
            self.dy = self.speed
        else:
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy
