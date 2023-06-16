from .buildings import *
from .players import AxeThrower
from .players import Villager

class IA:
    def __init__(self, world, camera, resource_manager):
       

        self.world = world
        self.camera = camera
        self.resource_manager = resource_manager
        self.ent1 = AxeThrower(self.world.world[7][28], self.world, self.camera, "enemy", self.resource_manager)
        # ent3 = Villager(self.world.world[3][3], self.world, self.camera, "enemy", self.resource_manager)
        self.world.iaworkers.append(self.ent1)
        # self.world.iaworkers.append(ent3)
        self.unit = Villager(self.world.world[9][30], self.world, self.camera, "player", self.resource_manager)
        Towncenter([30, 30], self.world, self.camera, self.resource_manager, "ennemy")

        #ArcheryRange([32, 31], self.world, self.camera, self.resource_manager, "ennemy")

        self.selected_enemie = []
        self.selected_enemie.append(self.unit)
        print(self.selected_enemie)
        self.attacking = False

    def go_attackIA(self):

        if self.selected_enemie:
            enemy = self.selected_enemie[0]
            enemy_pos = enemy.tile["grid"]
            self.attacking = True
            if self.world.world[enemy_pos[0]][enemy_pos[1]]["entity"]:  # si la tile cible n'a plus d'entité dessus
                if self.selected_enemie:  # s'il reste des ennemis dans la liste de cibles
                    if self.ent1.dest_tile == self.ent1.tile:
                        self.ent1.create_path(enemy_pos[0],
                                              enemy_pos[1] + 1)  # on attaque le prochain ennemi de la liste
            # condition pour qu'un personnage allié attaque sa cible s'il est assez près
            if self.ent1.tile in enemy.tile["adj_tiles"] and self.world.world[enemy_pos[0]][enemy_pos[1]]["entity"]:
                enemy.is_attacked = True

                if enemy.health > 0:
                    if self.world.is_on_a_tick(self.ent1.last_attack, 1000):
                        self.last_attack = pygame.time.get_ticks()
                        enemy.health = enemy.health - self.ent1.attack_damage

                if enemy.health <= 0:
                    print("IA killed unit")
                    self.en_attack = False
                    del self.selected_enemie[0]

                    if self.selected_enemie != []:
                        new_enemy_pos = self.selected_enemie[0].tile["grid"]
                        self.ent1.create_path(new_enemy_pos[0], new_enemy_pos[1])
                self.is_attacked = False
                self.en_attack = False

    def update(self):

        # if self.attacking == False:
        self.go_attackIA()
