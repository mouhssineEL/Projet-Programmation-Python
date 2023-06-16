
import sys
from .camera import Camera
from .world import World
from .selection_fonction import Selection
from .hud import *
from .players import *
from .AI import *
from .resource_manager import ResourceManager
####VARIABLES GLOBALES


class Game:

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.entities = [] #Les unités


        # Resource
        self.resource_manager = ResourceManager()
        self.resource_managerIA = ResourceManager()
        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height)
        #World
        self.world = World(self.resource_manager, self.entities,self.hud,MAP_SIZE,MAP_SIZE,self.width,self.height)

        #Camera
        self.camera = Camera(self.width, self.height)

        # Selecteur
        self.selecteur = Selection(self.screen)

        #ajout tchat
        self.tchat = InputBox( self.width*0.08, self.height*0.94, 140, 32, self.world, self.resource_manager,self.camera)

        ent =Archer(self.world.world[4][25], self.world, self.camera,"player",self.resource_manager)


        
        self.mobs = []
        self.mobs.append(ent)
        #IA
        self.IA = IA(self.world,self.camera,self.resource_manager)
        # horse
        #for _ in range(5): horse(self.world.world[15][15], self.world)
        # sheep
        #for _ in range(5): porc(self.world.world[15][15], self.world)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            self.tchat.handle_event(event)
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()




    def update(self):
        self.camera.update()
        self.hud.update()
        self.tchat.update()
        self.world.update(self.camera)
        self.IA.update()
        for e in self.entities : 
            e.update(self.camera)
            e.update_healthbarre(self.screen)
        





    def draw(self):
        self.screen.fill(BLACK)
        self.world.draw(self.screen,self.camera)
        self.hud.draw(self.screen)
        self.tchat.draw(self.screen)
        for ent in self.entities:
            if ent.health < ent.basevie and ent.health>1 :
                ent.update_healthbarre(self.screen)
                if 0.51*ent.basevie<ent.health < 0.9*ent.basevie:
                    ent.bar_color = (236,255,31)
                if 0.26*ent.basevie<ent.health < 0.5*ent.basevie:
                    ent.bar_color = (255, 172, 51)
                if ent.health < 0.25*ent.basevie:
                    ent.bar_color = (255, 51, 51)

        pygame.display.flip()

