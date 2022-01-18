import pygame as pg
from resource_manager import ResourceManager

class House:

    def __init__(self, pos, resource_manager):
        image = pg.image.load("../graphics/house.png")
        self.image = image
        self.name = "House"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = ResourceManager()
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["Wood"] += 1
            self.resource_manager.resources["Stone"] += 1
            self.resource_manager.resources["Gold"] += 1
            self.resource_cooldown = now

    def delete(self): self.image = None

    def get_name(self): return self.name
