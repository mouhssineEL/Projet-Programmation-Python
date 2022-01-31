import pygame as pg
from buildings  import House


class castle(House):

    def __init__(self, pos, resource_manager):
        super().__init__(pos, resource_manager)
        image = pg.image.load("../graphics/castle.png")
        self.image = image
        self.name = "castle"
        self.resource_manager = 0

        House.update(self)

