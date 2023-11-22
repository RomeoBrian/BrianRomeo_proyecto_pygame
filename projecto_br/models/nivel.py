import pygame as pg
from settings.constantes import TILEZISE,ANCHO
from models.tiles import Tile
from models.player import Player
from models.enemy import Enemy

class Nivel:
    def __init__(self,nivel_data,surface,diccionario_nivel: dict) -> None:
        self.__pantalla = surface
        self.__nivel_config = diccionario_nivel
        #Definimos los grupos de sprites
        self.__mover_mapa = 0
        self.crear_nivel(nivel_data)
        self.__lugar = 0
        self.__movimiento_camara = pg.math.Vector2()
        self.__enemy_collision = False
     
        

    def crear_nivel(self,layout):
        self.__tiles = pg.sprite.Group()
        self.__player = pg.sprite.GroupSingle()
        self.__enemy = pg.sprite.Group()
        for filas_index,filas in enumerate(layout):
            for col_index,celda in enumerate(filas):
                x = col_index * TILEZISE
                y = filas_index * TILEZISE
                if celda == '#':
                    tile = Tile((x,y),TILEZISE)
                    self.__tiles.add(tile)
                elif celda == 'P':
                    player_sprite = Player((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get('player'),self.__pantalla)
                    self.__player.add(player_sprite)
                elif celda == 'E':
                    enemy_sprite = Enemy((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get('enemy'))
                    self.__enemy.add(enemy_sprite)
    

    def movimiento_horizontal_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.rect.x += player.direccion.x * player.speed
        enemys = self.__enemy.sprites()
        for enemigo in enemys:
            enemigo.rect.x += enemigo.direccion.x * enemigo.speed
        for sprite in self.__tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direccion.x < 0:
                    self.__player.sprite.frame_index = 0
                    player.rect.left = sprite.rect.right
                    player.a_izquierda = True
                    self.__lugar = player.rect.left
                elif player.direccion.x > 0:
                    self.__player.sprite.frame_index = 0
                    player.rect.right = sprite.rect.left
                    player.a_derecha = True
                    self.__lugar = player.rect.right
        
                    
        
        if player.a_izquierda and (player.rect.left < self.__lugar or player.direccion.x >= 0):
            player.a_izquierda = False
        if player.a_derecha and (player.rect.right > self.__lugar or player.direccion.x <= 0):
            player.a_derecha = False

    
    def movimiento_vertical_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.get_grounded()
        for sprite in self.__tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direccion.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direccion.y = 0
                    player.is_grounded = True
                    player.do_salto = True                   
                elif player.direccion.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direccion.y = 0
                    player.en_techo = True
                
    
        if player.is_grounded and player.direccion.y < 0 or player.direccion.y > 1:
            player.is_grounded = False
        if player.en_techo and player.direccion.y > 0:
            player.en_techo = False
    
    def mover_camara(self):
        player = self.__player.sprite
        player_x = player.rect.centerx
        player_y = player.rect.centery
        direccion_x = player.direccion.x

        if player_x < self.__pantalla.get_width()/2 and direccion_x < 0:
            self.__movimiento_camara[0] = self.__nivel_config.get('velocidad_mover_mapa')
            player.speed = 0
        elif player_x > self.__pantalla.get_width() - (self.__pantalla.get_width()/2) and direccion_x > 0:
            self.__movimiento_camara[0] = -self.__nivel_config.get('velocidad_mover_mapa')
            player.speed = 0
        else:
            self.__movimiento_camara[0] = 0
            player.speed = self.__nivel_config.get('player').get('speed')
        

    def ataque_enemigo(self):
        for enemigos in self.__enemy:
            if pg.sprite.spritecollide(enemigos, self.__player, False):
                self.__enemy_collision = True

    def run(self,delta_ms):
        
        
        #colliosiones y muertes del enemigo
        if self.__player.sprite.is_hitting:
            for enemigos in self.__enemy:
                if self.__player.sprite.atack_rect.colliderect(enemigos):
                    print('hit')                    
                    enemigos.hit(self.__player.sprite.fuerza)
                    self.__player.sprite.is_hitting = False

        #player death
        self.ataque_enemigo()
        if self.__enemy_collision:
            self.__enemy_collision = False
            self.__player.sprite.recibir_golpe()
            print(self.__player.sprite.vidas)


        #tiles
        self.__tiles.update(self.__movimiento_camara[0])
        self.__tiles.draw(self.__pantalla)
        self.mover_camara()

        #player
        self.__player.update(delta_ms)
        self.movimiento_horizontal_colisiones(delta_ms)
        self.movimiento_vertical_colisiones(delta_ms)
        self.__player.draw(self.__pantalla)
        #pg.draw.circle(self.__pantalla, 'red',(self.__player.sprite.rect.centerx+10,self.__player.sprite.rect.centery) ,self.__player.sprite.radius)

        #enemy
        self.__enemy.update(self.__movimiento_camara[0],delta_ms)
        self.__enemy.draw(self.__pantalla)
        

        #proyectil
        self.__player.sprite.proyectil_group.update()
        self.__player.sprite.proyectil_group.draw(self.__pantalla)
        

