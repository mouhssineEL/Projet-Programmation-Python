import pygame

class Batiment :
    def __init__(self, pos, world, camera, resource_manager, team) :
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.camera = camera
        self.world = world
        self.world.entities.append(self)
        self.world.buildings[self.pos_x][self.pos_y] = self
        self.tile = self.world.world[self.pos_x][self.pos_y]
        self.tile["entity"] = True
        self.pos_x_r = self.tile["render_pos"][0]
        self.pos_y_r = self.tile["render_pos"][1]
        self.resource_manager = resource_manager
        self.counter = 0
        self.pourcentageconstruction = 0
        self.united = False
        self.team = team
        self.selected = False
        self.coordonne = []
        self.useable = False
        self.curr_tick = pygame.time.get_ticks()
        self.construction_time = self.curr_tick
        self.bar_color = (111, 210, 46)
        self.last_click = {"tick": 0, "type": -1}
        iso_poly = self.tile["iso_poly"]
        self.iso_poly = None
        

    def worksite(self, size) :
        return pygame.image.load("../Buildings/in_construction/"+str(size)+"X"+str(size)+"/while_building_"+str(size)+"_1.png")

    def in_construction(self,size) :
            if self.counter == self.constructiontime :
                self.image =pygame.image.load("../Buildings/in_construction/"+str(size)+"X"+str(size)+"/while_building_"+str(size)+"_2.png")
            elif self.counter == 2*self.constructiontime :
                self.image =pygame.image.load("../Buildings/in_construction/"+str(size)+"X"+str(size)+"/while_building_"+str(size)+"_3.png")
            elif self.counter >= 3*self.constructiontime :
                self.image =pygame.image.load("../Buildings/"+self.name+".png")
                self.useable = True
                self.curr_tick = 0


    def broken(self, size) :
        return pygame.image.load("../Buildings/broken/broken_building_"+str(size)+".png")

    def find_all_tiles(self) :
        all_tiles = []
        for s1 in range(0,self.size) :
            for s2 in range(0,self.size) :
                next_tile = self.world.world[self.tile["grid"][0]+s1][self.tile["grid"][0]+s2]
                next_tile["collision"] = True
                next_tile["entity"] = True
                all_tiles.append(next_tile)
        return all_tiles

    def update(self, camera) :

        mx,my = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        self.selection_box.update(self.pos_x_r + self.world.map_tiles.get_width() / 2 + camera.scroll.x + 48,
                                  self.pos_y_r - self.image.get_height() + camera.scroll.y + 48, 96, 192)

        pos_poly = [self.pos_x_r + self.world.map_tiles.get_width() / 2 + camera.scroll.x + 96,
                    self.pos_y_r - self.image.get_height() + camera.scroll.y + 192]

        self.iso_poly = [(pos_poly[0], pos_poly[1] - 48), (pos_poly[0] + 96, pos_poly[1]),
                         (pos_poly[0], pos_poly[1] + 48), (pos_poly[0] - 96, pos_poly[1])]

        if self.selection_box.collidepoint(mx,my):
            if mouse_action[0] :
                click = pygame.time.get_ticks()
                if self.world.is_on_a_tick(self.last_click["tick"],400) :
                    if not self.selected :
                        self.last_click["tick"] = click
                        self.last_click["type"] = 0
                        self.selected = True
                        self.world.selected_units.append(self)
                    else :
                        self.last_click["tick"] = click
                        self.last_click["type"] = 0
                        self.selected = False
                        self.world.selected_units.remove(self)  

        if self.selected and mouse_action[2] :
            self.selected = False
            self.world.selected_units.remove(self)

        if not self.useable :
            self.pourcentageconstruction = (pygame.time.get_ticks()-self.construction_time)//(3*self.constructiontime*10)
            if self.world.is_on_a_tick(self.curr_tick, self.constructiontime*1000) :
                self.counter += 1
                self.curr_tick = pygame.time.get_ticks()
                self.in_construction(self.size)

        else :
            if self.health <= 0 :
                self.world.buildings[self.pos_x][self.pos_y] = None
                del self

    def update_healthbarre(self,surface):
        
        bar_position = [self.pos_x+2415+self.camera.scroll.x, self.pos_y -35 + self.camera.scroll.y,self.health,5]
        back_bar_color=(60,63,60)
        back_bar_position = [self.pos_x+2415+self.camera.scroll.x, self.pos_y -35 + self.camera.scroll.y,self.basevie,5]
        pygame.draw.rect(surface, back_bar_color,back_bar_position)
        pygame.draw.rect(surface, self.bar_color,bar_position)

class Towncenter(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = pygame.image.load("../Buildings/Towncenter.png")
        self.name = "Towncenter"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.useable = True
        self.united = True
        self.health = 600
        self.basevie = 600
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()

    def load_image(self):
        villager = pygame.image.load("../assets/villager.png").convert_alpha()
        upgrade = pygame.image.load("../assets/upgrade.png").convert_alpha()
        return{"Villager": villager, "upgrade": upgrade} 



class House(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "House"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 550
        self.basevie= 550
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()

class Barracks(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "Barracks"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 350
        self.basevie= 350
        self.united = True
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()

    def load_image(self):
        axemen = pygame.image.load("../assets/Axethrower.png").convert_alpha()
        clubman= pygame.image.load("../assets/Axethrower.png").convert_alpha()
        return{"AxeThrower": axemen,"Clubman":clubman}

class castel(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "castel"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 350
        self.basevie= 350
        self.united = True
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 200)
        self.all_tiles = self.find_all_tiles()
        self.coordonne = 0
    def load_image(self):
        archer = pygame.image.load("../assets/archer.png").convert_alpha()
        return{"Archer": archer}    

class Stable(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "Stable"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 350
        self.basevie= 350
        self.united = True
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()

    def load_image(self):
        scout = pygame.image.load("../assets/Scout.png").convert_alpha()
        return{"Scout": scout}  

class SmallWall(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "SmallWall"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health =200
        self.basevie= 200
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()

class SmallWall1(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "SmallWall1"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 200
        self.basevie= 200
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()      


class SmallWall2(Batiment):

    def __init__(self, pos, world, camera, resource_manager, team):
        super().__init__(pos, world, camera, resource_manager, team)
        self.size = 1
        self.image = self.worksite(self.size)
        self.name = "SmallWall2"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager.apply_cost_to_resource(self.name)
        self.health = 200
        self.basevie= 200
        self.constructiontime = 1
        self.selection_box = pygame.Rect(self.pos_x_r + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 48,
                                            self.pos_y_r - self.image.get_height() + self.camera.scroll.y + 48, 96, 192)
        self.all_tiles = self.find_all_tiles()
