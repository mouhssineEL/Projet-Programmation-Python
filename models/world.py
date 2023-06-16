from .Ressource import Ressource
from .Tile import Tile
from models.Definitions import TILE_SIZE
from .map import *
from .AI import *
from .camera import Camera
from .chat import *
import random
from .players import *
#from players import AxeThrower
#from players import Scout

class World:
    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):

        self.resource_manager = resource_manager
        self.ressources = {
            "bush": [],
            "tree": [],
            "rock": [],
            "gold": []
        }

        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.perlin_scale = grid_length_x / 5
        self.array_tiles = randomMap()
        self.map_tiles = pygame.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world(self.array_tiles)
        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.selected_units = []
        self.selected_resource = None

        self.iaworkers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.camera = Camera(self.width, self.height)
        self.temp_tile = None
        self.examine_tile = None
        self.collision_matrix = self.create_collision_matrix()

        self.nbrHouse = 0
        self.nbrpnj = 0

        Villager(self.world[6][27], self, self.camera, "player", self.resource_manager)
        AxeThrower(self.world[4][25], self, self.camera, "player", self.resource_manager)
        # ajout Towncenter ENNEMI
        castel([6, 25], self, self.camera, self.resource_manager, "player")

        castel([15, 5], self, self.camera, self.resource_manager, "enemy")

        AxeThrower(self.world[32][34], self, self.camera, "player", self.resource_manager)
        AxeThrower(self.world[35][34], self, self.camera, "enemy", self.resource_manager)


    def is_on_a_tick(self, start_timer, time_to_wait):
        return (pygame.time.get_ticks() - start_timer) > time_to_wait

    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0

        return collision_matrix

    def update(self, camera):

        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.selected_tile = None

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

                if mouse_action[0] and not collision:
                    if self.hud.selected_tile["name"] == "Towncenter":
                        Towncenter(grid_pos, self, self.camera, self.resource_manager, "player")

                        Towncenter.coordonne = [grid_pos[0], grid_pos[1]]

                    elif self.hud.selected_tile["name"] == "House":
                        House(grid_pos, self, self.camera, self.resource_manager, "player")

                        self.nbrHouse += 4

                    elif self.hud.selected_tile["name"] == "Barracks":
                        Barracks(grid_pos, self, self.camera, self.resource_manager, "player")

                        Barracks.coordonne = [grid_pos[0], grid_pos[1]]

                    elif self.hud.selected_tile["name"] == "castel":
                        castel(grid_pos, self, self.camera, self.resource_manager, "player")

                        castel.coordonne = [grid_pos[0], grid_pos[1]]

                    elif self.hud.selected_tile["name"] == "Stable":
                        Stable(grid_pos, self, self.camera, self.resource_manager, "player")

                        Stable.coordonne = [grid_pos[0], grid_pos[1]]

                    elif self.hud.selected_tile["name"] == "SmallWall":
                        SmallWall(grid_pos, self, self.camera, self.resource_manager, "player")


                    elif self.hud.selected_tile["name"] == "SmallWall1":
                        SmallWall1(grid_pos, self, self.camera, self.resource_manager, "player")


                    elif self.hud.selected_tile["name"] == "SmallWall2":
                        SmallWall2(grid_pos, self, self.camera, self.resource_manager, "player")




                    elif self.hud.selected_tile["name"] == "Archer" and self.nbrpnj <= self.nbrHouse:
                        Archer(self.world[7][27], self,
                               self.camera, "player", self.resource_manager)

                        self.nbrpnj += 1

                    elif self.hud.selected_tile["name"] == "AxeThrower" and self.nbrpnj <= self.nbrHouse:
                        ent = AxeThrower(self.world[Barracks.coordonne[0] + 1][Barracks.coordonne[1] + 1], self,
                                         self.camera, "player", self.resource_manager)

                        self.nbrpnj += 1

                    elif self.hud.selected_tile["name"] == "Villager" and self.nbrpnj <= self.nbrHouse:
                        Villager(self.world[Towncenter.coordonne[0] + 1][Towncenter.coordonne[1] + 1], self,
                                 self.camera, "player", self.resource_manager)

                        self.nbrpnj += 1

                    elif self.hud.selected_tile["name"] == "Scout" and self.nbrpnj <= self.nbrHouse:
                        Scout(self.world[Stable.coordonne[0] + 1][Stable.coordonne[1] + 1], self, self.camera, "player",
                              self.resource_manager)

                        self.nbrpnj += 1

                    elif self.hud.selected_tile["name"] == "Clubman" and self.nbrpnj <= self.nbrHouse:
                        Scout(self.world[Barracks.coordonne[0] + 1][Barracks.coordonne[1] + 1], self, self.camera,
                                "player", self.resource_manager)

                        self.nbrpnj = +1

                    elif self.hud.selected_tile["name"] == "upgrade":
                        if self.hud.age < 1:
                            self.hud.age += 1
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.world[grid_pos[0]][grid_pos[1]]["entity"] = True
                    self.hud.selected_tile = None

        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                if grid_pos[0] < self.grid_length_x and grid_pos[1] < self.grid_length_y:
                    selected_tile = self.world[grid_pos[0]][grid_pos[1]]
                    selected_building = self.buildings[grid_pos[0]][grid_pos[1]]
                if mouse_action[0] and ((selected_tile is not None) or (selected_building is not None)):
                    self.examine_tile = grid_pos
                    if selected_building is not None:
                        self.hud.examined_tile = selected_building
                    elif selected_tile["tile"]:
                        self.selected_resource = selected_tile

    def draw(self, screen, camera):
        screen.blit(self.map_tiles, (camera.scroll.x, camera.scroll.y))
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):

                render_pos = self.world[x][y]["render_pos"]

                # draw worker
                worker = self.workers[x][y]
                if worker is not None:
                    if worker.team == "enemy":
                        pygame.draw.polygon(screen, (255, 0, 0), worker.iso_poly, 2)
                    if worker.selected: pygame.draw.polygon(screen, (255, 255, 255), worker.iso_poly, 2)

                    screen.blit(worker.image, (
                        worker.pos_x + self.map_tiles.get_width() / 2 + camera.scroll.x - 48,
                        worker.pos_y - worker.image.get_height() + camera.scroll.y))
                    if worker.health <= 0:
                        worker.delete()


                building = self.buildings[x][y]

                if building is not None:
                    screen.blit(building.image,
                                (render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x + 8,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y - 4))


                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x + 8,
                                     y + render_pos[1] - (
                                             building.image.get_height() - TILE_SIZE) + camera.scroll.y - 4) for
                                    x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 2)


                other = self.world[x][y]

                if other["tile"] != "":
                    screen.blit(self.tiles[other["tile"]],
                                (render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x + 8,
                                 render_pos[1] - (
                                             self.tiles[other["tile"]].get_height() - TILE_SIZE) + camera.scroll.y - 4))

                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(self.tiles[other["tile"]]).outline()
                            mask = [(x + render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x + 8,
                                     y + render_pos[1] - (
                                             self.tiles[other["tile"]].get_height() - TILE_SIZE) + camera.scroll.y - 4)
                                    for
                                    x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 2)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.map_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pygame.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self, array_tiles):

        def adjacent_tiles(w, t):
            return [w[t["grid"][0] + 1][t["grid"][1]] if (t["grid"][0] + 1) < MAP_SIZE else None,  # tile bas gauche
                    w[t["grid"][0]][t["grid"][1] + 1] if (t["grid"][1] + 1) < MAP_SIZE else None,  # tile bas droite
                    w[t["grid"][0] - 1][t["grid"][1]] if (t["grid"][0] - 1) >= 0 else None,  # tile haut gauche
                    w[t["grid"][0]][t["grid"][1] - 1] if (t["grid"][1] - 1) >= 0 else None,  # tile haut droite
                    w[t["grid"][0] - 1][t["grid"][1] - 1] if (t["grid"][0] - 1) >= 0 and (
                                t["grid"][1] - 1) >= 0 else None,  # tile haut
                    w[t["grid"][0] + 1][t["grid"][1] + 1] if (t["grid"][0] + 1) > MAP_SIZE and (
                                t["grid"][1] - 1) > MAP_SIZE else None,  # tile bas
                    w[t["grid"][0] - 1][t["grid"][1] + 1] if (t["grid"][0] + 1) >= 0 and (
                                t["grid"][1] - 1) > MAP_SIZE else None,  # tile droite
                    w[t["grid"][0] + 1][t["grid"][1] - 1] if (t["grid"][0] + 1) > MAP_SIZE and (
                                t["grid"][1] - 1) >= 0 else None]  # tile gauche

        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile["render_pos"]
                self.map_tiles.blit(self.tiles[array_tiles[grid_x, grid_y]],
                                    (render_pos[0] + (self.map_tiles.get_width()) / 2, render_pos[1]))

        for grid_x in range(self.grid_length_x):
            for grid_y in range(self.grid_length_y):
                world[grid_x][grid_y]["adj_tiles"] = adjacent_tiles(world, world[grid_x][grid_y])

        return world

    def grid_to_world(self, grid_x,
                      grid_y):
        rien = Ressource(0, "")
        tile1 = Tile(grid_x, grid_y, 0, rien, 0)

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 500)
        perlin = 5

        if grid_y > 3:
            if ((perlin >= 15) or (perlin <= -35)) and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                grid_x - 1, grid_y - 1] != "water" and self.array_tiles[grid_x - 2, grid_y - 2] != "water":
                tile1 = "tree"
            else:

                if 1 < r < 10 and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                    grid_x, grid_y - 1] != "water" and self.array_tiles[grid_x - 4, grid_y - 4] != "water":
                    tile1 = "tree"
                elif 11 < r < 15 and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                    grid_x, grid_y - 1] != "water" and self.array_tiles[grid_x - 4, grid_y - 4] != "water":
                    tile1 = "flower"
                elif 20 < r < 25 and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                    grid_x - 1, grid_y - 1] != "water" and self.array_tiles[grid_x - 4, grid_y - 4] != "water":
                    tile1 = "bush"
                elif 30 < r < 32 and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                    grid_x - 1, grid_y - 1] != "water" and self.array_tiles[grid_x - 4, grid_y - 4] != "water":
                    tile1 = "gold"
                elif 32 < r < 34 and self.array_tiles[grid_x, grid_y] != "water" and self.array_tiles[
                    grid_x - 1, grid_y - 1] != "water" and self.array_tiles[grid_x - 4, grid_y - 4] != "water":
                    tile1 = "rock"
                else:
                    tile1 = ""

        else:
            tile1 = ""

        if grid_y == 0 and grid_x == 0:
            tile1 = "gold"

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile1,
            "collision": False if tile1 == "" and self.array_tiles[grid_x, grid_y] != "water" else True,
            "entity": False,
            "adj_tiles": None
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):
        Towncenter = pygame.image.load("Buildings/Towncenter.png").convert_alpha()
        grass = pygame.image.load("assets/t_grass.png").convert_alpha()
        water = pygame.image.load("assets/t_water.png").convert_alpha()
        tree = pygame.image.load("assets/tree.png").convert_alpha()
        bush = pygame.image.load("assets/bush.png").convert_alpha()
        gold = pygame.image.load("assets/Gold.png").convert_alpha()
        rock = pygame.image.load("assets/Gold.png").convert_alpha()
        house = pygame.image.load("Buildings/House.png").convert_alpha()
        flower = pygame.image.load("assets/flower.png").convert_alpha()

        return {"Towncenter": Towncenter, "grass": grass, "water": water, "tree": tree, "bush": bush, "gold": gold,
                "rock": rock, "House": house, "flower": flower}

    def mouse_to_grid(self, x, y, scroll):

        world_x = x - scroll.x - self.map_tiles.get_width() / 2
        world_y = y - scroll.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x

        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)
        return (world_bounds and not mouse_on_panel)
