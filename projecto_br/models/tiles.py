import pygame as pg
import random

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,size,tile_list): 
        super().__init__()
        #self.image = pg.Surface((size,size))
        self.__tile_list = tile_list
        self.image = pg.image.load(self.__tile_list[0])
        self.image = pg.transform.scale(self.image,(size,size))
        #self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, mover):
        self.rect.x += mover