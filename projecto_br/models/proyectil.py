import pygame as pg
from settings.constantes import ANCHO
from settings.utils import importar_carpeta

class Proyectil(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction,path = None, img_path = False):
        super().__init__()
        # self.image = pygame.Surface((50, 10))
        # self.image.fill((255, 0, 0))
        print(path)
        self.importar_assest(path)
        self.__frame_index = 0
        self.__frame_rate = 100
        self.__velocidad_animacion = 0.25
        self.direction = direction
        #self.__load_img(img_path,path)
        self.image = self.__animaciones['proyectil'][self.__frame_index]
        self.image = pg.transform.scale(self.image,(32,32))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        #self.image = pg.transform.scale(self.image,(32,32))
        

    def importar_assest(self,path):
        self.__animaciones = {'proyectil': []}
        
        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool= True)
            

    def tomar_direccion_imagen(self,image):
        if self.direction == 'derecha':
            self.image = image
        else:
            imagen_rotada = pg.transform.flip(image,True,False)
            self.image = imagen_rotada

    def play_animacion(self,delta_ms):
        animacion = self.__animaciones['proyectil']

        self.__velocidad_animacion += delta_ms
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            image = pg.transform.scale(image,(32,32))
            self.tomar_direccion_imagen(image)
            self.__velocidad_animacion = 0
    
    
    
    
    def __load_img(self, img_path: bool,path = None):
        if img_path:
            self.image = pg.image.load(path)
            if self.direction == 'izquierda':
                imagen_rotada = pg.transform.flip(self.image,True,False)
                self.image = imagen_rotada
        else: 
            self.image = pg.Surface((8, 8))
            self.image.fill('white')

    def update(self,delta_ms):
        self.play_animacion(delta_ms)
        match self.direction:
            case 'derecha':
                self.rect.x += 10
                if self.rect.x >= ANCHO:
                    self.kill()
            case 'izquierda':
                self.rect.x -= 10
                if self.rect.x <= 0:
                    self.kill()