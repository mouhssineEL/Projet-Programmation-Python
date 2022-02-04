#on a pas arriver a travailiier avec chat
import pygame as pg

from players import *
pg.init()
window = pg.display.set_mode((840, 580))
COLOR_INACTIVE = (255,255,255)
COLOR_ACTIVE = (255,0,0)
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, world, resource_manager,camera, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.world = world
        self.resource_manager = resource_manager
        self.camera = camera
      

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            
            if self.rect.collidepoint(event.pos):
                
                self.active = not self.active
            else:
                self.active = False
            
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    cheatcode(self,self.text)
                    
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
       
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        pg.display.flip()

    def draw(self, screen):
        
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        
        pg.draw.rect(screen, self.color, self.rect, 2)



def entrercmd(screen1):
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 200, 140, 32)
    input_box3 =InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2,input_box3]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for boxff in input_boxes:
                boxff.handle_event(event)

        for box in input_boxes:
            box.update()

        screen1.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen1)

        pg.display.flip()
        clock.tick(30)

def cheatcode(self, txt):
    if txt=='NINJALUI':
        print('ajout de ressource')
        self.resource_manager.resources["food"]+=10000
        self.resource_manager.resources["wood"]+=10000
        self.resource_manager.resources["stone"]+=10000
        self.resource_manager.resources["gold"]+=10000
        self.text = ''
    elif txt=="BIGDADY":
        Biggy(self.world.world[15][13], self.world, self.camera, "player")
        print("spawn de bigpuffy")
        self.text=''
    elif txt=="STEROIDS":
        print("miam miam")
        self.text=''
    else :
        self.text = ''

if __name__ == '__main__':
    entrercmd(window)
    pg.quit()
