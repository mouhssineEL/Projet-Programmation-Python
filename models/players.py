from pathlib import Path
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from .Definitions import *


class Personnage:

    def __init__(self, tile, world, camera, team):
        self.health = 100
        self.attack_damage = 10
        self.basevie = 100
        self.team = team
        self.world = world
        self.world.entities.append(self)
        self.camera = camera
        self.world.world[tile["grid"][0]][tile["grid"][1]]["entity"] = True
        self.tile = tile
        self.tile["entity"] = True
        self.dest_tile = self.tile

        self.image = pygame.image.load(Path('models/Sprites/Archer/Walk/Archerwalk001.png')).convert_alpha()
        self.temp = 0
        self.en_attack = False
        self.moveright_animation = False
        self.moveleft_animation = False
        self.movestraight_animation = False
        self.moveback_animation = False
        self.stand_ground = True

        self.sprites = []
        self.current_sprite = 0
        self.d = 0
        self.avancement = 0
        self.world.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.pos_x = tile["render_pos"][0]
        self.pos_y = tile["render_pos"][1]
        self.selected = False
        self.ia_selected = False
        self.is_attacked = False

        self.selected_enemies = []
        self.selection_box = pygame.Rect(self.pos_x + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x - 15,
                                         self.pos_y - self.image.get_height() + self.camera.scroll.y, 30, 80)
        iso_poly = self.tile["iso_poly"]  # coord isometrique
        self.iso_poly = None
        self.mouse_to_grid(0, 0, self.camera.scroll)
        self.create_path(tile["grid"][0], tile["grid"][1])
        self.path_index = 0
        self.grids = []
        self.last_click = {"tick": 0, "type": -1}
        self.last_attack = 0
        self.bar_color = (111, 210, 46)

    def movestraight(self):
        self.movestraight_animation = True

    def moveleft(self):
        self.moveleft_animation = True

    def moveright(self):
        self.moveright_animation = True

    def moveback(self):
        self.moveback_animation = True

    def attacking(self):
        self.en_attack = True

    def standground(self):
        self.stand_ground = True

    #Animation

    def charge_images_for_animation(self, first_frame, last_frame, type_animation):
        self.sprites = []

        end_name = self.type_perso + type_animation
        end_name = end_name.capitalize()
        general_path = "models/Sprites/" + self.type_perso + "/" + type_animation + "/" + end_name

        for frame_nb in range(first_frame, last_frame + 1):
            self.sprites.append(
                pygame.image.load(Path(general_path + '0' + ('0' if frame_nb < 10 else '') + str(frame_nb) + '.png')))

    # Animation immobile

    def animation_stand_ground(self):
        self.standground()
        self.charge_images_for_animation(1, 15, "Stand")

    # Animations déplacement

    def animation_walk_back(self):
        self.moveright()
        self.charge_images_for_animation(40, 50, "Walk")

    def animation_walk_left(self):
        self.moveleft()
        self.charge_images_for_animation(21, 30, "Walk")

    def animation_walk_top_left(self):
        self.moveleft()
        self.charge_images_for_animation(31, 40, "Walk")

    def animation_walk_bottom_left(self):
        self.moveleft()
        self.charge_images_for_animation(11, 20, "Walk")

    def animation_walk_straight(self):
        self.movestraight()
        self.charge_images_for_animation(1, 10, "Walk")

    # Animations attaque

    def animation_attack_straight(self):
        self.attacking()
        self.charge_images_for_animation(1, 15, "Attack")

    #################################################
    ########## DEPLACEMENTS
    #################################################

    # Pathfinding

    def create_path(self, x, y):
        searching_for_path = True
        while searching_for_path:
            self.dest_tile = self.world.world[x][y]
            if not self.dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
            elif self.tile != None and (self.tile in self.dest_tile["adj_tiles"]):
                break
            elif self.dest_tile["entity"] or self.dest_tile["tile"]:
                if self.close_tile(self.dest_tile) != None:
                    self.dest_tile = self.close_tile(self.dest_tile)
                    self.create_path(self.dest_tile["grid"][0], self.dest_tile["grid"][1])
                break
            else:
                break

    # Trouver une tile à côté d'une destination (utile en cas de collision)

    def close_tile(self, t):
        for adj_tile in t["adj_tiles"]:
            if adj_tile != None:
                if not adj_tile["collision"]:
                    return adj_tile;
        return None;

    # Change la tile du personnage

    def change_tile(self, new_tile):
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"] = False
        self.world.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.workers[new_tile[0]][new_tile[1]] = self
        self.tile = self.world.world[new_tile[0]][new_tile[1]]
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"] = True

    # Repartition des directions (utile pour les animations)

    def direction(self, grid_start, grid_dest):
        dx = grid_start[0] - grid_dest[0]
        dy = grid_start[1] - grid_dest[1]
        direction = 0

        if (2 > dx > 1 and dy < 0):
            print("Direction en haut")
            direction = 15

        if (25 > dx > 10 and 25 > dy > 10):
            print("Direction en bas à droite , dx = ", dx, " et dy = ", dy)
            direction = 5
        elif (dx > 0 and (-30 < dy < -6)):
            print("Direction en haut à droite , dx = ", dx, " et dy = ", dy)
            direction = 1

        elif (dx < 0 and dy > 0):
            print("Direction en bas à gauche")
            direction = 7

        elif (dx < 0 and dy < 0):
            print("Direction en haut à gauche")
            direction = 10

        elif (dx > 0 and dy <= 1):
            print("Direction à droite")
            direction = 3
        elif (dx < 0 and dy <= 1):
            print("Direction à gauche")
            direction = 9
        elif (dy > 0 and dx <= 1):
            print("Direction bas")
            direction = 6
        elif (dy < 0 and dx <= 1):
            print("Direction Haut")
            direction = 12

        return direction

    #################################################
    ########## FONCTIONS D'ATTAQUE
    #################################################

    def go_attack(self):
        pygame.mixer.init()
        enemy = self.selected_enemies[0]
        enemy_pos = enemy.tile["grid"]

        if self.world.world[enemy_pos[0]][enemy_pos[1]]["entity"]:  # si la tile cible n'a plus d'entité dessus
            # self.selected_enemies.pop(0) #on supprime l'ennemi de la liste de cibles
            if self.selected_enemies:  # s'il reste des ennemis dans la liste de cibles
                # new_enemy_pos = self.selected_enemies[0].tile["grid"]
                s = 0
                if self.dest_tile == self.tile:
                    if s == 0:
                        pygame.mixer.init()
                        #SOUND['swordFight'].play(3)
                        s = 1
                    self.create_path(enemy_pos[0], enemy_pos[1])  # on attaque le prochain ennemi de la liste

        if self.tile in enemy.tile["adj_tiles"] and self.world.world[enemy_pos[0]][enemy_pos[1]]["entity"]:

            if enemy.health > 0:
                if self.world.is_on_a_tick(self.last_attack, 1000):
                    print(enemy.health)
                    self.last_attack = pygame.time.get_ticks()
                    enemy.health = enemy.health - self.attack_damage

            if enemy.health <= 0:
                pygame.mixer.init()
                print("dead")
                #SOUND["death"].play()
                self.en_attack = False

                if self.selected_enemies != []:
                    new_enemy_pos = self.selected_enemies[0].tile["grid"]
                    self.create_path(new_enemy_pos[0], new_enemy_pos[1])

            self.is_attacked = False
            self.en_attack = False

    def hit_back(self):
        for t in self.tile["adj_tiles"]:
            if t:
                if self.world.workers[t["grid"][0]][t["grid"][1]]:
                    possible_enemy = self.world.workers[t["grid"][0]][t["grid"][1]]
                    if possible_enemy.team == "enemy":
                        self.selected_enemies.append(self.world.workers[t["grid"][0]][t["grid"][1]])

    #################################################
    ########## REPERAGE DE LA SOURIS
    #################################################

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.world.map_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    #################################################
    ########## SUPPRESSION DE L'UNITE
    #################################################

    def delete(self):
        self.world.entities.remove(self)
        self.world.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"] = False
        del self

    #################################################
    ########## UPDATES
    #################################################

    # Update barre de vie

    def update_healthbarre(self, surface):

        bar_position = [self.pos_x + 4830 + self.camera.scroll.x, self.pos_y - 35 + self.camera.scroll.y, self.health,
                        5]

        back_bar_color = (60, 63, 60)
        back_bar_position = [self.pos_x + 4830 + self.camera.scroll.x, self.pos_y - 35 + self.camera.scroll.y,
                             self.basevie, 5]

        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, self.bar_color, bar_position)

    # Update animations

    def update_animation(self, speed):
        if self.moveright_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.moveright_animation = False

        elif self.moveleft_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.moveleft_animation = False

        elif self.movestraight_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.movestraight_animation = False

        elif self.en_attack == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.en_attack = False

        self.image = self.sprites[int(self.current_sprite)]

    # Update générale

    def update(self, camera):
        # Updating mouse position and action and the grid_pos

        mx, my = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()
        grid_pos = self.mouse_to_grid(mx, my, self.camera.scroll)

        self.selection_box.update(self.pos_x + self.world.map_tiles.get_width() / 2 + camera.scroll.x - 15,
                                  self.pos_y - self.image.get_height() + camera.scroll.y, 30, 80)

        # Selection polygon
        pos_poly = [self.pos_x + self.world.map_tiles.get_width() / 2 + camera.scroll.x,
                    self.pos_y - self.image.get_height() + camera.scroll.y + 78]
        self.iso_poly = [(pos_poly[0], pos_poly[1] - 46), (pos_poly[0] + 94, pos_poly[1]),
                         (pos_poly[0], pos_poly[1] + 46), (pos_poly[0] - 94, pos_poly[1])]

        # collision matrix (for pathfinding and buildings)
        self.world.collision_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 0
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["collision"] = True

        # update des animations
        self.update_animation(0.2)
        self.animation_stand_ground()

        # pour selectionner les unités
        if self.selection_box.collidepoint(mx, my):
            if mouse_action[0]:
                click = pygame.time.get_ticks()
                if self.world.is_on_a_tick(self.last_click["tick"], 400):
                    if not self.selected:
                        self.last_click["tick"] = click
                        self.last_click["type"] = 0
                        self.selected = True
                        self.world.selected_units.append(self)
                    else:
                        self.last_click["tick"] = click
                        self.last_click["type"] = 0
                        self.selected = False
                        self.world.selected_units.remove(self)

                        # si une unité est sélectionnée et qu'on fait un clic droit
        if (self.selected and self.team == "player") or (self.ia_selected and self.team == "enemy"):

            if mouse_action[2]:
                self.last_click["tick"] = pygame.time.get_ticks()
                self.last_click["type"] = 0
                # print(grid_pos[0], grid_pos[1])

                if self.team == "player":
                    self.selected_enemies = [unit for unit in self.world.selected_units if
                                             unit.team != "player" and unit.health > 0]  # on regarde s'il y a des ennemis sélectionés par le joueur
                    self.world.selected_units.remove(self)
                    self.selected = False

                else:  # même raisonnement mais pour l'IA : les unités "sélectionnées" ne sont pas les mêmes donc on utilise ia_selected_units
                    self.selected_enemies = [unit for unit in self.world.ia_selected_units if unit.team != self.team]
                    self.world.ia_selected_units.remove(self)
                    self.ia_selected = False

                if self.selected_enemies:  # si on a des cibles, on les attaque
                    first_enemy_pos = self.selected_enemies[0].tile["grid"]
                    self.create_path(first_enemy_pos[0], first_enemy_pos[1])  # go bagarre
                    print(first_enemy_pos[0], first_enemy_pos[1])
                    # print(self.selected_enemies)

                else:  # pour aller à un endroit e où on a cliqué

                    self.create_path(grid_pos[0], grid_pos[1])

        if self.type_perso == "Villager":
            self.update_farm()

        if self.selected_enemies:
            self.go_attack()
            if self.selected_enemies[0].health <= 0:
                del self.selected_enemies[0]

        # if self.is_attacked :
        #    self.hit_back()

        if self.path_index <= len(self.path) - 1:
            self.animation_walk_straight()
            new_pos = self.path[self.path_index]
            new_real_pos = self.world.world[new_pos[0]][new_pos[1]]["render_pos"]

            if self.avancement < 1:
                self.avancement += (1 / 135) * 5
                self.avancement = round(self.avancement, 3)
            else:
                self.avancement = 1

            self.pos_x = round(lerp(self.tile["render_pos"][0], new_real_pos[0], self.avancement), 3)
            self.pos_y = round(lerp(self.tile["render_pos"][1], new_real_pos[1], self.avancement), 3)

            if self.pos_x == new_real_pos[0] and self.pos_y == new_real_pos[1]:
                # update position in the world
                self.world.collision_matrix[self.tile["grid"][1]][
                    self.tile["grid"][0]] = 1  # Free the last tile from collision
                self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"] = False
                self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["collision"] = False

            if self.pos_x == new_real_pos[0] and self.pos_y == new_real_pos[1]:  # update position in the world
                self.change_tile(new_pos)
                self.path_index += 1
                self.avancement = 0
        else:
            self.movestraight_animation = False
            self.animation_stand_ground()


class Archer(Personnage):
    def __init__(self, tile, world, camera, team, resource_manager):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Archer"
        self.health = 2
        self.basevie = 35
        self.attack_damage = 3
        self.costfood = 50
        self.training_time_in_sec = 30
        self.rateoffire = 1.4
        self.range = 5
        self.speed = 1.2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.type_perso)
        # ANIMATION IMAGE WALK
        self.charge_images_for_animation(1, 15, "Stand")
        self.image = self.sprites[self.current_sprite]

class AxeThrower(Personnage):
    def __init__(self, tile, world, camera, team, resource_manager):
        super().__init__(tile, world, camera, team)
        self.type_perso = "AxeThrower"
        self.basevie = 50
        self.health = 50
        self.attack_damage = 5
        self.costfood = 50
        self.training_time_in_sec = 28
        self.rateoffire = 1.5
        self.speed = 1.2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.type_perso)
        # ANIMATION IMAGE WALKING

        self.charge_images_for_animation(1, 15, "Stand")
        self.image = self.sprites[self.current_sprite]


class Scout(Personnage):
    def __init__(self, tile, world, camera, team, resource_manager):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Scout"
        self.basevie = 150
        self.health = 150
        self.attack = 8
        self.costfood = 90
        self.training_time_in_sec = 30
        self.rateoffire = 1.5
        self.speed = 2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.type_perso)
        # ANIMATION IMAGE WALKING

        self.sprites.append(pygame.image.load(Path('models/Sprites/Scout/Walk/Scoutwalk001.png')))
        self.image = self.sprites[self.current_sprite]


class Villager(Personnage):
    def __init__(self, tile, world, camera, team, resource_manager):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Villager"
        self.basevie = 25
        self.health = 25
        self.attack_damage = 3
        self.costfood = 50
        self.training_time_in_sec = 20
        self.rateoffire = 1.5
        self.speed = 1.1

        self.was_farming = False
        self.was_attacking = False
        self.is_farming = False
        self.selected_resource = None

        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.type_perso)

        # ANIMATION IMAGE WALKING

        self.sprites = []
        self.charge_images_for_animation(1, 15, "Stand")
        self.image = self.sprites[self.current_sprite]

    def update_farm(self):


        if self.is_farming and self.selected_resource and (self.tile in self.selected_resource["adj_tiles"]):
            resource_type = self.selected_resource["tile"]


            if resource_type == "bush":
                self.world.resource_manager.resources["food"] = self.world.resource_manager.resources["food"] + 10

            else:
                if resource_type == "tree":
                    self.world.resource_manager.resources["wood"] = self.world.resource_manager.resources["wood"] + 50
                elif resource_type == "rock":
                    self.world.resource_manager.resources["stone"] = self.world.resource_manager.resources["stone"] + 15
                else:
                    self.world.resource_manager.resources["gold"] = self.world.resource_manager.resources["gold"] + 7

                self.selected_resource["tile"] = ""

            self.selected_resource = None
            self.is_farming = False

    def animation_walk_straight(self):
        self.movestraight()
        self.charge_images_for_animation(1, 15, "Walk")

