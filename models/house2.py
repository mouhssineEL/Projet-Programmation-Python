import pygame as pg
from buildings  import House




class House2(House):

    def __init__(self, pos, resource_manager):
        super().__init__(pos, resource_manager)
        image = pg.image.load("../graphics/building02.png")
        self.image = image
        self.name = "House2"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

        House.update(self)


