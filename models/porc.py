import pygame as pg
from animals import animal

class porc(animal):

    def __init__(self, tile, world):
        super().__init__(tile, world)
        self.world = world
        self.world.entities.append(self)
        image_animal = pg.image.load("../graphics/porc.png").convert_alpha()
        self.name = "porc"
        self.image = pg.transform.scale(image_animal, (image_animal.get_width(), image_animal.get_height()))
        self.tile = tile

        # pathfinding
        self.world.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()
        self.create_path()