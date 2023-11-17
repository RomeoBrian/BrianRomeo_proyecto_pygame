from typing import Any
import pygame as pg
from settings.utils import importar_carpeta


class Player(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.importar_player_assest()
        self.__frame_index = 1
        self.__velocidad_animacion = 0.10
        self.image = self.__animaciones['idle'][self.__frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.__estado = 'idle'
        self.__mirar_derecha = True
        self.__is_grounded = False
        self.__en_techo = False
        self.__a_derecha = False
        self.__a_izquierda = False
        self.__is_atacking = False
        self.__is_doble_salto = True
        self.__is_jumping = False
        
        #movimiento
        self.__direccion = pg.math.Vector2(0,0)
        self.__speed = 6
        self.__gravedad = 0.8
        self.__velocidad_salto = -16

    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self,velociadad):
        self.__speed = velociadad

    @property
    def direccion(self):
        return self.__direccion
    
    @direccion.setter
    def direccion(self,direccion):
        self.__direccion = direccion
    
    @property
    def is_grounded(self):
        return self.__is_grounded

    @is_grounded.setter
    def is_grounded(self,grounded: bool):
        self.__is_grounded = grounded
    
    @property
    def en_techo(self):
        return self.__en_techo

    @en_techo.setter
    def en_techo(self,techo: bool):
        self.__en_techo = techo
    
    @property
    def a_derecha(self):
        return self.__a_derecha

    @a_derecha.setter
    def a_derecha(self,derecha: bool):
        self.__a_derecha = derecha
    
    @property
    def a_izquierda(self):
        return self.__a_izquierda

    @a_izquierda.setter
    def a_izquierda(self,izquierda: bool):
        self.__a_izquierda = izquierda

    def importar_player_assest(self):
        path = 'assets/graphics/player/'
        self.__animaciones = {'idle': [], 'caer': [], 'correr': [], 'saltar': [], 'atack': []}

        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo)

    def player_estado(self):
        if self.__is_atacking:
            self.__estado = 'atack'
        else:
            if self.__direccion.y < 0 and not self.__is_grounded:
                self.__estado = 'saltar'
            elif self.__direccion.y > 0 and not self.__is_grounded:
                self.__estado = 'caer'
            else:
                if self.__direccion.x != 0:
                    self.__estado = 'correr'
                else:
                    self.__estado = 'idle'

    def play_animacion(self):
        animacion = self.__animaciones[self.__estado]

        self.__frame_index += self.__velocidad_animacion
        if self.__frame_index >= len(animacion):
            if self.__is_atacking:
                self.__is_atacking = False
                print(self.__frame_index)
            self.__frame_index = 0

        image = animacion[int(self.__frame_index)]
        if self.__mirar_derecha:
            self.image = image
        else:
            imagen_rotada = pg.transform.flip(image,True,False)
            self.image = imagen_rotada


        #Control de coliciones con los objetos del mapa
        if self.__is_grounded and self.__a_derecha:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.__is_grounded and self.__a_izquierda:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.__is_grounded:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.__en_techo and self.__a_derecha:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.__en_techo and self.__a_izquierda:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.__en_techo:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        




    def get_teclas(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_d]:
            self.__direccion.x = 1
            self.__mirar_derecha = True
        elif teclas[pg.K_a]:
            self.__direccion.x = -1
            self.__mirar_derecha = False
        else:
            self.__direccion.x = 0
        if teclas[pg.K_SPACE] and (self.__is_grounded or self.__is_jumping):
            if self.__is_doble_salto and self.__is_jumping and not self.__is_grounded:
                self.salto(False)
            elif self.__is_grounded and not self.__is_jumping:
                self.salto(True)
            print(self.__direccion.y,self.__is_doble_salto,self.__is_jumping)        
            
        if teclas[pg.K_f] and not self.__is_atacking:
            self.atack()
            
    def get_grounded(self):
        self.__direccion.y += self.__gravedad
        self.rect.y += self.__direccion.y

    def salto(self,jump: bool):
            self.__direccion.y = self.__velocidad_salto
            self.__is_jumping = jump
            

            #self.__is_jumping = False

                

        

    
    def atack(self):
        self.__is_atacking = True

    def update(self):
        self.get_teclas()
        self.player_estado()
        self.play_animacion()
        

        
