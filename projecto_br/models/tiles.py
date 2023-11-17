from typing import Any
import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,size): 
        super().__init__()
        self.image = pg.Surface((size,size))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, mover_x):
        self.rect.x += mover_x