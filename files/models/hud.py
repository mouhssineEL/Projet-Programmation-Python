from chat import *
import pygame as pg
import pygame

class Hud:

    def __init__(self, resource_manager, width, height):

        self.resource_manager = resource_manager

        self.width = width
        self.height = height

        self.hud_colour = (198, 155, 93, 175)

        # resouces hud
        self.resouces_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resouces_surface.fill(self.hud_colour)
        self.resources_rect = self.resouces_surface.get_rect(topleft=(0, 0))

        # building hud
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_surface.fill(self.hud_colour)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_surface.fill(self.hud_colour)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))

        self.images = self.load_images()
        self.tiles = self.create_build_hud()
        

        self.selected_tile = None
        self.examined_tile = None
        
        self.unité = []
        self.age = 0
        

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.80 + 10]
        object_width = self.build_surface.get_width() // 5
        compteur=0
        tiles = []
        
        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )
            if compteur <3:
                render_pos[0] += image_scale.get_width() + 10
        
            elif compteur == 3 or compteur== 7:
                render_pos[1] += image_scale.get_height() + 10
                render_pos[0] -= 3*(image_scale.get_width() + 10)
                
            else :
                render_pos[0] += image_scale.get_width() + 10
            compteur+=1  

        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]) and self.age >= self.resource_manager.whatage(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

        for tile in self.unité:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        if self.selected_tile is not None:
            img = self.selected_tile["image"].copy()
            img.set_alpha(100)

        # resouce hud
        screen.blit(self.resouces_surface, (0, 0))
        # build hud
        
        background = pygame.image.load('../assets/selectioncivpanel.png')
        background_scale=self.scale_image(background,self.width*1.01,self.height*0.25)
        screen.blit(background_scale, (self.width * 0, self.height * 0.75))

        #UI_menu_chat = pygame.image.load('../assets/UI_menu_chat.png')
        #UI_menu_chat_scale=background_scale=self.scale_image(UI_menu_chat,self.width*0.03,self.height*0.05)
        #screen.blit(UI_menu_chat_scale, (self.width*0.05, self.height*0.925))

        resourcecivpanel = pygame.image.load('../assets/resourcecivpanel.png')
        resourcecivpanel_scale = self.scale_image(resourcecivpanel,self.width*1.01,self.height*0.06)
        screen.blit(resourcecivpanel_scale, (self.width*0, self.height * 0.0))
        
        UI_food = pygame.image.load('../assets/iconfood.png')
        UI_UI_food_scale=background_scale=self.scale_image(UI_food,self.width*0.02,self.height*0.023)
        screen.blit(UI_UI_food_scale, (self.width*0.028, self.height*0.015))

        UI_wood = pygame.image.load('../assets/iconwood.png')
        UI_UI_wood_scale=background_scale=self.scale_image(UI_wood,self.width*0.02,self.height*0.023)
        screen.blit(UI_UI_wood_scale, (self.width*0.028 + 200, self.height*0.015))

        UI_stone = pygame.image.load('../assets/iconpierre.png')
        UI_UI_stone_scale=background_scale=self.scale_image(UI_stone,self.width*0.02,self.height*0.023)
        screen.blit(UI_UI_stone_scale, (self.width*0.028 + 400, self.height*0.015))

        UI_gold = pygame.image.load('../assets/icongold.png')
        UI_UI_gold_scale=background_scale=self.scale_image(UI_gold,self.width*0.02,self.height*0.023)
        screen.blit(UI_UI_gold_scale, (self.width*0.028 + 600, self.height*0.015))

        #background4 = pygame.image.load('assets/bg4.png')
        #screen.blit(background4, (self.width * 0.0, self.height * 0 -385))

        # select hud
        if self.examined_tile is not None :
            w, h = self.select_rect.width, self.select_rect.height
    
            img = self.examined_tile.image.copy()
            img_scale = self.scale_image(img, h=h * 0.7)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.80 + 40))
            
            if self.examined_tile.team == "player":
                draw_text(screen, self.examined_tile.name, 40, (255, 255, 255), [self.width*0.35,self.height * 0.80])
                draw_text(screen, str(self.examined_tile.health) +"/"+ str(self.examined_tile.basevie) , 30, (255, 255, 255), (self.width*0.60, self.height * 0.79))

                
                if self.examined_tile.pourcentageconstruction <= 100:
                    draw_text(screen, str(self.examined_tile.pourcentageconstruction) + "%", 30, (255, 255, 255),(self.width*0.63, self.height * 0.85) )
            else :
                draw_text(screen, self.examined_tile.name, 40, (255, 0, 0), [self.width*0.35,self.height * 0.80])
                draw_text(screen, str(self.examined_tile.health) +"/"+ str(self.examined_tile.basevie) , 40, (255, 255, 255), (self.width*0.50, self.height * 0.83))
               
                bar_color = (111, 210, 46)
                bar_position = [self.width*0.50, self.height * 0.90,self.examined_tile.health/2,20]
                
                back_bar_color=(60,63,60)
                back_bar_position = [self.width*0.50, self.height * 0.90,self.examined_tile.basevie/2,20]
                pygame.draw.rect(screen, back_bar_color,back_bar_position)
                pygame.draw.rect(screen, bar_color,bar_position)

                

#ajout unité
            

            
            if self.examined_tile.united and self.examined_tile.team == "player" and self.examined_tile.useable:
                self.unite = self.examined_tile.load_image()
                decalage = 0
                for unit_name,unit in self.unite.items() :
                    screen.blit(unit,(self.width*0.50+decalage, self.height * 0.85))
                    draw_text(screen, str(unit_name), 20, (255, 255, 255), (self.width*0.50+decalage, self.height * 0.85+50))
                    draw_text(screen, str(self.resource_manager.costs[unit_name]), 20, (255, 255, 255), (self.width*0.50+decalage, self.height * 0.85+70))
                    image = unit.copy()
                    rect = image.get_rect(topleft=(self.width*0.50+decalage, self.height * 0.85))

                    self.unité.append(
                    {
                    "name": unit_name,
                    "icon": image,
                    "image": self.unite[unit_name],
                    "rect": rect,
                    "affordable": True
                    }
                    )
                    decalage =+100
        
        
                

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

        # resources
        pos = self.width*0.05
        for resource, resource_value in self.resource_manager.resources.items():
            txt =":" + str(resource_value)
            draw_text(screen, txt, 30, (255,255,255), (pos, self.height*0.015))
            pos += 200 + len(str(resource_value))


            
    def load_images(self):

        # read images
        Towncenter = pygame.image.load("../Buildings/Towncenter.png").convert_alpha()
        House = pygame.image.load("../Buildings/House.png").convert_alpha()
        Barracks = pygame.image.load("../Buildings/Barracks.png").convert_alpha()
        ArcheryRange = pygame.image.load("../Buildings/Towncenter.png").convert_alpha()
        Stable = pygame.image.load("../Buildings/Stable.png").convert_alpha()
        SmallWall = pygame.image.load("../Buildings/SmallWall.png").convert_alpha()
        SmallWall1 = pygame.image.load("../Buildings/SmallWall1.png").convert_alpha()
        SmallWall2 = pygame.image.load("../Buildings/SmallWall2.png").convert_alpha()
        return {"Towncenter": Towncenter, "House": House,"Barracks":Barracks,"castel":ArcheryRange, "Stable":Stable, "SmallWall" :SmallWall,"SmallWall1" :SmallWall1, "SmallWall2":SmallWall2}

    
    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image


