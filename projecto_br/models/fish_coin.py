import pygame as pg
from settings.utils import importar_carpeta


class Fish_coin(pg.sprite.Sprite):
    def __init__(self,pos,size,diccionario_config) -> None:
        super().__init__()
        self.__fish_config = diccionario_config
        self.importar_assest()
        self.__frame_rate = self.__fish_config.get('frame_rate')
        self.__frame_index = 0
        self.__velocidad_animacion = self.__fish_config.get('velocidad_animacion')
        self.image = self.__animaciones['animado'][self.__frame_index]
        #self.image = pg.Surface((size,size))
        self.image = pg.transform.scale(self.image,(size*2,size*2))
        #self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        
    
    def importar_assest(self):
        path = self.__fish_config.get('path')
        self.__animaciones = importar_carpeta(path,carpetas_bool= True)
        
        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool= True)


    def play_animacion(self,delta_ms):
        animacion = self.__animaciones['animado']

        self.__velocidad_animacion += delta_ms
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            self.image = image
            self.image = pg.transform.scale(self.image,(40,40))
            self.__velocidad_animacion = 0
    
    
    def update(self, mover,delta_ms,pausa):
        if not pausa:
            self.rect.x += mover
            self.play_animacion(delta_ms)