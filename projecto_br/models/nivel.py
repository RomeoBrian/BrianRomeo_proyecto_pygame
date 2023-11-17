import pygame as pg
from settings.constantes import TILEZISE,ALTO,ANCHO
from models.tiles import Tile
from models.player import Player

class Nivel:
    def __init__(self,nivel_data,surface) -> None:
        self.__pantalla = surface
        #Definimos los grupos de sprites
        self.crear_nivel(nivel_data)
        self.__mover_mapa = 0
        self.__lugar = 0
        

    def crear_nivel(self,layout):
        self.__tiles = pg.sprite.Group()
        self.__player = pg.sprite.GroupSingle()
        for filas_index,filas in enumerate(layout):
            for col_index,celda in enumerate(filas):
                x = col_index * TILEZISE
                y = filas_index * TILEZISE
                if celda == '#':
                    tile = Tile((x,y),TILEZISE)
                    self.__tiles.add(tile)
                elif celda == 'P':
                    player_sprite = Player((x,y))
                    self.__player.add(player_sprite)

    def movimiento_horizontal_colisiones(self):
        player = self.__player.sprite
        player.rect.x += player.direccion.x * player.speed
        for sprite in self.__tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direccion.x < 0:
                    player.rect.left = sprite.rect.right
                    player.a_izquierda = True
                    self.__lugar = player.rect.left
                elif player.direccion.x > 0:
                    player.rect.right = sprite.rect.left
                    player.a_derecha = True
                    self.__lugar = player.rect.right
        
        if player.a_izquierda and (player.rect.left < self.__lugar or player.direccion.x >= 0):
            player.a_izquierda = False
        if player.a_derecha and (player.rect.right > self.__lugar or player.direccion.x <= 0):
            player.a_derecha = False

    
    def movimiento_vertical_colisiones(self):
        player = self.__player.sprite
        player.get_grounded()
        for sprite in self.__tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direccion.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direccion.y = 0
                    player.is_grounded = True
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
        direccion_x = player.direccion.x

        if player_x < ANCHO/4 and direccion_x < 0:
            self.__mover_mapa = 4
            player.speed = 0
        elif player_x > ANCHO - (ANCHO/4) and direccion_x > 0:
            self.__mover_mapa = -4
            player.speed = 0
        else:
            self.__mover_mapa = 0
            player.speed = 6

    def run(self):
        #tiles
        self.__tiles.update(self.__mover_mapa)
        self.__tiles.draw(self.__pantalla)
        self.mover_camara()

        #player
        self.__player.update()
        self.movimiento_horizontal_colisiones()
        self.movimiento_vertical_colisiones()
        self.__player.draw(self.__pantalla)
        

