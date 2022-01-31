
import pygame as pg
import random
import noise
from .settings import TILE_SIZE
from .buildings import House1, House2,barrack
from .workers import Worker
class World:

    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.perlin_scale = grid_length_x/2

        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()


        self.temp_tile = None
        self.examine_tile = None

        self.index = 0
        self.path = None
        self.dest = None
        self.numero = 0
        self.units = None
        self.okay = None
        self.collision_matrix = self.create_collision_matrix()
        #to add building and units and workers
        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.unit = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]



    def update(self, camera):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()


        if mouse_action[2] and mouse_action[0]:
            self.examine_tile = None
            self.hud.examined_tile = None
            self.okay = None

        self.temp_tile = None
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }
                ###############################################
                ##    sont des test pour ajouter les maisons,ave cle test si y a pas
                ##    de collision
                ################################################
                if mouse_action[0] and not collision:
                    if self.hud.selected_tile["name"] == "House1":
                        ent = House1(render_pos, self.resource_manager)
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "barrack":
                        ent = barrack(render_pos, self.resource_manager)
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "House2":
                        ent = House2(render_pos, self.resource_manager)
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent

                    #self.collision_matrix[[grid_pos[1]][grid_pos[0]]] = 0


                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud.selected_tile = None

        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.can_place_tile(grid_pos):
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                building = self.buildings[grid_pos[0]][grid_pos[1]]
                worker = self.workers[grid_pos[0]][grid_pos[1]]
                unit = self.unit[grid_pos[0]][grid_pos[1]]
                if mouse_action[0] and collision:
                    self.examine_tile = grid_pos
                if mouse_action[0] and (worker is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = worker
                if mouse_action[0] and (building is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building
                if mouse_action[0] and (unit is not None):
                    self.hud.examined_tile = unit
                    self.pos = grid_pos
                    self.okay = 1

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos =  self.world[x][y]["render_pos"]
                # draw world tiles
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline() #"""""""""""""""""nkin aytit izayd ors is tsha
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)
                tile1 = self.world[x][y]["tile1"]
                if tile1 != "":
                    screen.blit(self.tiles[tile1],
                                (self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 (self.tiles[tile1].get_height() ) + camera.scroll.y))

                # draw buildings
                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image,
                                    (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                     render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)
                #draw workers
                worker = self.workers[x][y]
                if worker is not None:
                    screen.blit(worker.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(worker.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, y + render_pos[1] - (worker.image.get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)
        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))


        return world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])
        t = random.randint(1, 50)
        r = random.randint(1, 50)
        """perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)

        if (perlin >= 100) or (perlin <= -100):
            tile = "tree"
        else: """

        if t == 1:
                tile1 = "castle"
        else:
                tile1 = ""
        if r == 1:
                tile = "tree"
        elif r == 2:
                tile = "rock"
        else:
                tile = ""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "tile1": tile1,
            "collision": False if tile == "" else True
        }


        return out
    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range (self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y




    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def load_images(self):

        block = pg.image.load("../graphics/block1111111111111.png").convert_alpha()
        # read images
        building1 = pg.image.load("../graphics/building01.png").convert_alpha()
        #barrack = pg.image.load("../graphics/barrack1.png").convert_alpha()
        building2 = pg.image.load("../graphics/building02.png").convert_alpha()
        tree = pg.image.load("../graphics/tree.png").convert_alpha()
        rock = pg.image.load("../graphics/rock.png").convert_alpha()
        castle = pg.image.load("../graphics/castle.png").convert_alpha()
        images = {
            "barrack": barrack,
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock,
            "block": block,
            "castle": castle
        }

        return images

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False
    def get_map(self): return self.world
    def get_map_size_x(self): return self.grid_length_x
    def get_map_size_y(self): return self.grid_length_y
