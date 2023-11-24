import pygame as pg
from settings.constantes import ANCHO,FPS
from settings.utils import importar_carpeta
from models.proyectil import Proyectil


class Player(pg.sprite.Sprite):
    def __init__(self,pos,gravedad,diccionario_config: dict,pantalla):
        super().__init__()
        self.importar_player_assest()
        self.__pantalla = pantalla
        #animacion
        self.__player_config = diccionario_config
        self.__frame_rate = self.__player_config.get('frame_rate')
        self.__frame_index = 0
        self.__velocidad_animacion = self.__player_config.get('velocidad_animacion')
        self.image = self.__animaciones['idle'][self.__frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.__estado = 'idle'
        self.__mirar_derecha = True
        self.__is_grounded = False
        self.__en_techo = False
        self.__a_derecha = False
        self.__a_izquierda = False
        self.__do_salto = True
        self.__do_super_salto = self.__player_config.get('super_salto')
        self.__ready = True
        self.__damage = False
        self.radius = 20
        self.__atack_rect = pg.Rect(0,0,0,0)

        #vida
        self.__vidas = self.__player_config.get('vida')

        #ataque
        self.__is_atacking = False
        self.__is_hitting = False
        self.__is_shooting = False
        self.__fuerza = self.__player_config.get('fuerza')
        self.__proyectil_group = pg.sprite.Group()
        self.__tiempo_disparo = 0
        self.__disparo_cooldown = self.__player_config.get('disparo_cooldown')
        
        #movimiento
        self.__direccion = pg.math.Vector2(0,0)
        self.__speed = self.__player_config.get('speed')
        self.__gravedad = gravedad
        self.__altura_salto = self.__player_config.get('altura_salto')
        if self.__do_super_salto:
            self.__altura_salto += 5
        self.__velocidad_salto = self.__altura_salto

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
    
    @property
    def do_salto(self):
        return self.__do_salto

    @do_salto.setter
    def do_salto(self,saltar: bool):
        self.__do_salto = saltar
    
    @property
    def do_super_salto(self):
        return self.__do_super_salto

    @do_super_salto.setter
    def do_super_salto(self,super_salto: bool):
        self.__do_super_salto = super_salto

    @property
    def proyectil_group(self):
        return self.__proyectil_group

    @proyectil_group.setter
    def proyectil_group(self,proyectil: bool):
        self.__proyectil_group = proyectil
    
    @property
    def frame_index(self):
        return self.__frame_index
    
    @frame_index.setter
    def frame_index(self,frame):
        self.__frame_index = frame

    @property
    def vidas(self):
        return self.__vidas

    @property
    def atack_rect(self):
        return self.__atack_rect

    @property
    def is_atacking(self):
        return self.__is_atacking

    @is_atacking.setter
    def is_atacking(self,atacking):
        self.__is_atacking = atacking
    
    @property
    def is_hitting(self):
        return self.__is_hitting

    @is_hitting.setter
    def is_hitting(self,hitting):
        self.__is_hitting = hitting
    
    @property
    def fuerza(self):
        return self.__fuerza

    @fuerza.setter
    def fuerza(self,aumento_fuerza):
        self.__fuerza = aumento_fuerza

    def importar_player_assest(self):
        path = 'assets/graphics/player/'
        self.__animaciones = importar_carpeta(path,carpetas_bool= True)#{'idle': [], 'caer': [], 'correr': [], 'saltar': [], 'atack': [], 'shoot': []}
        
        for animacion in self.__animaciones.keys():
            path_completo = path + animacion
            self.__animaciones[animacion] = importar_carpeta(path_completo,imagenes_bool= True)

    def player_estado(self):
        if self.__vidas > 0:
            if self.__is_atacking:
                self.__estado = 'atack'
            elif self.__is_shooting:
                self.__estado = 'shoot'
            elif self.__direccion.y < 0 and not self.__is_grounded:
                self.__estado = 'saltar'
            elif self.__direccion.y > 0 and not self.__is_grounded:
                self.__estado = 'caer'
            elif self.__damage:
                self.__estado = 'damage'
            elif self.__direccion.x != 0:
                self.__estado = 'correr'
            else:
                if self.__is_grounded:
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
        if self.__is_shooting:
            self.__frame_rate = 80  
        if self.__velocidad_animacion >= self.__frame_rate:
            self.__frame_index += 1
            self.__frame_index %= len(animacion)
            image = animacion[self.__frame_index]
            self.tomar_direccion_imagen(image)
            self.__velocidad_animacion = 0
            if self.__estado == 'atack' and self.__frame_index == 2:
                self.__is_atacking = False
            if self.__estado == 'damage' and self.__frame_index == 2:
                self.__damage = False
            if self.__estado == 'death' and self.__frame_index == 5:
                print('murio')
                self.__frame_rate = 10000
        
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
        

    def walk(self,derecha = True):
        if derecha:
            self.__direccion.x = 1
        else:
            self.__direccion.x = -1
        return self.__direccion.x
    

    def get_teclas(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_d] and not teclas[pg.K_a]:
            self.walk(True)
            self.__mirar_derecha = True     
        if teclas[pg.K_a] and not teclas[pg.K_d]:
            self.walk(False)
            self.__mirar_derecha = False
        if not teclas[pg.K_a] and not teclas[pg.K_d]:
            self.__direccion.x = 0
            self.__estado = 'idle'
        if teclas[pg.K_SPACE] and self.__is_grounded:    
            self.salto()       
        if teclas[pg.K_f] and not self.__is_atacking and self.__ready:
            self.atack()
            self.__ready = False
            self.__tiempo_disparo = pg.time.get_ticks()
        if teclas[pg.K_e] and not self.__is_shooting and self.__ready:
            self.shoot()
            self.__ready = False
            self.__tiempo_disparo = pg.time.get_ticks()
            


    def cooldown(self):
        if not self.__ready:
            curent_time = pg.time.get_ticks()
            if curent_time - self.__tiempo_disparo >= self.__disparo_cooldown:
                self.__is_shooting = False
                self.__ready = True
                self.__frame_index = 0

    def get_grounded(self):
        self.__direccion.y += self.__gravedad
        self.rect.y += self.__direccion.y
        self.__velocidad_salto = self.__altura_salto

    def salto(self):
            if self.__do_salto:
                self.__direccion.y -= self.__velocidad_salto
                self.__velocidad_salto -= self.__gravedad
                if self.__velocidad_salto > -self.__altura_salto:
                    self.__do_salto = False
                    self.__velocidad_salto = self.__altura_salto
                
                

    
    def atack(self):
        self.__is_hitting = True
        self.__is_atacking = True
        if self.__is_hitting:
            if self.__mirar_derecha:
                self.__atack_rect = pg.Rect(self.rect.centerx,self.rect.y, 20 + self.rect.width, self.rect.height)
            else:
                self.__atack_rect = pg.Rect(self.rect.centerx - 45,self.rect.y, 20 + self.rect.width, self.rect.height)
        #dibujo el rectangulo para probar como funciona.
        #pg.draw.rect(self.__pantalla, 'red',self.__atack_rect)
        
    
    def shoot(self):
        self.__is_shooting = True
        self.__proyectil_group.add(self.crear_proyectil())
    
    def crear_proyectil(self):
        if self.__mirar_derecha:
            return Proyectil(self.rect.centerx, self.rect.centery, 'derecha','./assets/graphics/player/proyectil/proyectil.png' ,True) # Crea y devuelve un objeto de la clase Bullet en la posición actual del ratón
        else:
            return Proyectil(self.rect.centerx, self.rect.centery, 'izquierda','./assets/graphics/player/proyectil/proyectil.png' , True) # Crea y devuelve un objeto de la clase Bullet en la posición actual del ratón
    
    def recibir_golpe(self):
        self.__vidas -= 1
        self.__damage = True

    def update(self,delta_ms):
        self.get_teclas()
        self.cooldown()
        self.player_estado()
        self.play_animacion(delta_ms)


        
