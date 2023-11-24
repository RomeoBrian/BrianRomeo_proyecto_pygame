import pygame as pg

class Boundry(pg.sprite.Sprite):
    def __init__(self,pos,size): 
        super().__init__()
        self.image = pg.Surface((size,size)).convert_alpha()
        #self.image.set_alpha(128)
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, mover):
        self.rect.x += mover