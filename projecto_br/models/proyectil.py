import pygame as pg
from settings.constantes import ANCHO

class Proyectil(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction,path = None, img_path = False):
        super().__init__()
        # self.image = pygame.Surface((50, 10))
        # self.image.fill((255, 0, 0))
        self.direction = direction
        self.__load_img(img_path,path)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        

    def __load_img(self, img_path: bool,path = None):
        if img_path:
            self.image = pg.image.load(path)
            if self.direction == 'izquierda':
                imagen_rotada = pg.transform.flip(self.image,True,False)
                self.image = imagen_rotada
        else: 
            self.image = pg.Surface((8, 8))
            self.image.fill('white')

    def update(self):
        match self.direction:
            case 'derecha':
                self.rect.x += 20
                if self.rect.x >= ANCHO:
                    self.kill()
            case 'izquierda':
                self.rect.x -= 20
                if self.rect.x <= 0:
                    self.kill()