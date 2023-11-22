import pygame as pg
from settings.constantes import ANCHO
from settings.utils import importar_carpeta


class Enemy(pg.sprite.Sprite):
    def __init__(self,pos,gravedad,enemy_configs: dict):
        super().__init__()
        self.importar_enemy_assest()
        self.__enemy_configs = enemy_configs
        #animacion
        self.__frame_index = 0
        self.__frame_movimiento = 0
        self.__frame_rate = self.__enemy_configs.get('frame_rate')
        self.__velocidad_animacion = self.__enemy_configs.get('velocidad_animacion')
        self.__velocidad_movimiento = self.__enemy_configs.get('velocidad_movimiento')
        self.image = self.__animaciones['idle'][self.__frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.__estado = 'idle'
        self.__mirar_derecha = True
        self.__is_grounded = False
        self.__en_techo = False
        self.__a_derecha = False
        self.__a_izquierda = False
        self.__get_hit = False

        #vida
        self.__vidas = self.__enemy_configs.get('vidas')

        #ataque
        self.__is_atacking = False
        self.__is_shooting = False
        self.__fuerza = self.__enemy_configs.get('fuerza')
        
        #movimiento
        self.__direccion = pg.math.Vector2(0,0)
        self.__speed =  self.__enemy_configs.get('speed')
        self.__gravedad = gravedad

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
    def fuerza(self):
        return self.__fuerza
    
    @fuerza.setter
    def fuerza(self,aumento_fuerza):
        self.__fuerza = aumento_fuerza

    def importar_enemy_assest(self):
        path = 'assets/graphics/enemy/summon/'
        self.__animaciones = importar_carpeta(path,carpetas_bool = True)

        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool = True)

    def enemy_estado(self):
        if self.__vidas > 0:
            if self.__is_atacking:
                self.__estado = 'atack'
            elif self.__is_shooting:
                self.__estado = 'shoot'
            elif self.__get_hit:
                self.__estado = 'damage'
            else: 
                self.__estado = 'idle'
        else:
            self.__estado = 'death'

    def tomar_direccion_imagen(self,image):
        if self.__mirar_derecha:
            self.image = image
        else:
            imagen_rotada = pg.transform.flip(image,True,False)
            self.image = imagen_rotada

    def play_animacion(self,delta_ms):
        animacion = self.__animaciones[self.__estado]

        self.__velocidad_animacion += delta_ms
        if self.__estado == 'death':
            self.__velocidad_animacion += delta_ms/10
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            self.tomar_direccion_imagen(image)
            self.__velocidad_animacion = 0
            if self.__estado == 'damage' and self.__frame_index == 3:
                self.__get_hit = False
            if self.__estado == 'death' and self.__frame_index == 4:
                self.kill()
        

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
        
    def moviemiento_enemigo(self,delta_time):
        self.__velocidad_movimiento += delta_time
        if self.__velocidad_movimiento >= self.__frame_rate:
            self.__frame_movimiento += 1
            if(self.__frame_movimiento > 0 and self.__frame_movimiento < 4):
                self.__direccion.x = 1
                self.__mirar_derecha = True
            elif(self.__frame_movimiento >= 4 and self.__frame_movimiento < 6):
                self.__direccion.x = -1
                self.__mirar_derecha = False
            else:
                self.__frame_movimiento = 0
            self.__velocidad_movimiento = 0
    

    def get_grounded(self):
        self.__direccion.y += self.__gravedad
        self.rect.y += self.__direccion.y
    
    def atack(self):
        self.__is_atacking = True
        self.__frame_index = 0
    
    def shoot(self):
        self.__is_shooting = True
        self.__frame_index = 0

    def hit(self, golpe):
        self.__get_hit = True
        self.__vidas -= golpe
        

    def update(self,mover,delta_ms):
        self.rect.x += mover
        self.moviemiento_enemigo(delta_ms)
        self.enemy_estado()
        self.play_animacion(delta_ms)


        
