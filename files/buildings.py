import pygame as pg


class House1:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("../assets/graphics/building01.png")
        self.image = image
        self.name = "House1"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()
#
    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["Wood"] += 1
            self.resource_cooldown = now


    def delete(self): self.image = None

    def get_name(self): return self.name

class House2:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("../assets/graphics/building02.png")
        self.image = image
        self.name = "House2"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["Stone"] += 1
            self.resource_cooldown = now

    def delete(self): self.image = None

    def get_name(self): return self.name