import pygame as pg
from settings.constantes import TILEZISE,ANCHO,ALTO
from models.tiles import Tile
from models.boundries import Boundry
from models.player import Player
from models.enemy import Enemy

class Nivel:
    def __init__(self,nivel_data,surface,diccionario_nivel: dict,ancho_nivel) -> None:
        self.__pantalla = surface
        self.__nivel_config = diccionario_nivel
        #Definimos los grupos de sprites
        self.__mover_mapa = 0
        self.__nivel_data = nivel_data
        self.crear_nivel(nivel_data)
        self.__lugar_player = 0
        self.__lugar_enemy = 0
        self.__scroll_offset = 200
        self.__movimiento_camara = pg.math.Vector2()
        self.__enemy_collision = False
        self.__ancho_nivel = ancho_nivel

        #background
        self.__fondo_stone = pg.image.load('./assets/graphics/background/background_stone.png').convert_alpha()
        self.__fondo_stone = pg.transform.scale(self.__fondo_stone,(self.__fondo_stone.get_width()*2,self.__fondo_stone.get_height()*2))
     
        

    def crear_nivel(self,layout):
        self.__tiles = pg.sprite.Group()
        self.__boundry = pg.sprite.Group()
        self.__player = pg.sprite.GroupSingle()
        self.__enemy = pg.sprite.Group()
        for filas_index,filas in enumerate(layout):
            for col_index,celda in enumerate(filas):
                x = col_index * TILEZISE
                y = filas_index * TILEZISE
                match celda:
                    case '0':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_medio.png'])
                        self.__tiles.add(tile)
                    case '1':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_arriba_derecha.png'])
                        self.__tiles.add(tile)
                    case '2':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_medio_derecha.png'])
                        self.__tiles.add(tile)
                    case '3':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_abajo_derecha.png'])
                        self.__tiles.add(tile)
                    case '4':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_abajo_medio.png'])
                        self.__tiles.add(tile)
                    case '5':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_abajo_izquierda.png'])
                        self.__tiles.add(tile)
                    case '6':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_medio_izquierda.png'])
                        self.__tiles.add(tile)
                    case '7':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_arriba_izquierda.png'])
                        self.__tiles.add(tile)
                    case '8':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_fondo_medio.png'])
                        self.__tiles.add(tile)
                    case 'q':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_invertido_arriba_derecha.png'])
                        self.__tiles.add(tile)
                    case 'e':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_invertido_arriba_izquierda.png'])
                        self.__tiles.add(tile)
                    case 'z':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_invertido_abajo_izquierda.png'])
                        self.__tiles.add(tile)
                    case 'c':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/piso_invertido_abajo_derecha.png'])
                        self.__tiles.add(tile)
                    case 'p':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/plataforma_inicio.png'])
                        self.__tiles.add(tile)
                    case 'l':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/plataforma_medio.png'])
                        self.__tiles.add(tile)
                    case 'a':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/plataforma_fin.png'])
                        self.__tiles.add(tile)
                    case 't':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/plataforma_sola.png'])
                        self.__tiles.add(tile)
                    case 'b':
                        boundries = Boundry((x,y),TILEZISE)
                        self.__boundry.add(boundries)
                    case 'P':
                        player_sprite = Player((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get('player'),self.__pantalla)
                        self.__player.add(player_sprite)
                    case 'E':
                        enemy_sprite = Enemy((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get('enemy'))
                        self.__enemy.add(enemy_sprite)
                    case 'T':
                        tile = Tile((x,y),TILEZISE,['./assets/graphics/tiles/ground/trampa.png'])
                        self.__tiles.add(tile)
    
    def tileBackground(self,image: pg.Surface) -> None:
        screenWidth, screenHeight = self.__pantalla.get_size()
        imageWidth, imageHeight = image.get_size()
        
        # Calculate how many tiles we need to draw in x axis and y axis
        tilesX = int(screenWidth / imageWidth) + 1
        tilesY = int(screenHeight / imageHeight) + 1
        # Loop over both and blit accordingly
        for x in range(tilesX):
            for y in range(tilesY):
                self.__pantalla.blit(image, (x * imageWidth, y * imageHeight))


    def movimiento_horizontal_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.rect.x += player.direccion.x * player.speed
        enemys = self.__enemy.sprites()
        #colision del player con el entorno
        for tile_sprite in self.__tiles.sprites():
            if tile_sprite.rect.colliderect(player.rect):
                if player.direccion.x < 0:
                    player.frame_index = 0
                    player.rect.left = tile_sprite.rect.right + 3
                    player.a_izquierda = True
                    self.__lugar_player = player.rect.left
                elif player.direccion.x > 0:
                    player.frame_index = 0
                    player.rect.right = tile_sprite.rect.left  - 3
                    player.a_derecha = True
                    self.__lugar_player = player.rect.right
        
        for enemigo in enemys:
            enemigo.rect.x += enemigo.direccion.x * enemigo.speed
            enemigo.frame_movimiento += 1
            enemigo.campo_vision.center = (enemigo.rect.centerx + 75 * enemigo.direccion.x,enemigo.rect.centery)
            #pg.draw.rect(self.__pantalla,'white',enemigo.campo_vision)
            for boundry_sprite in self.__boundry.sprites():
                if boundry_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.x < 0:
                        enemigo.rect.left = boundry_sprite.rect.right + 1.7
                        enemigo.a_izquierda = True
                        self.__lugar_enemy = enemigo.rect.left
                    elif enemigo.direccion.x > 0:
                        enemigo.rect.right = boundry_sprite.rect.left - 1.7
                        enemigo.a_derecha = True
                        self.__lugar_enemy = enemigo.rect.right
        
        #enemy
        if enemigo.a_izquierda and (enemigo.rect.left < self.__lugar_enemy or enemigo.direccion.x >= 0):
            enemigo.a_izquierda = False
        if enemigo.a_derecha and (enemigo.rect.right > self.__lugar_enemy or enemigo.direccion.x <= 0):
            enemigo.a_derecha = False
                    
        #player
        if player.a_izquierda and (player.rect.left < self.__lugar_player or player.direccion.x >= 0):
            player.a_izquierda = False
        if player.a_derecha and (player.rect.right > self.__lugar_player or player.direccion.x <= 0):
            player.a_derecha = False

        

    
    def movimiento_vertical_colisiones(self,delta_ms):
        player = self.__player.sprite
        player.get_grounded()
        enemys = self.__enemy.sprites()
        for tile_sprite in self.__tiles.sprites():
            if tile_sprite.rect.colliderect(player.rect):
                if player.direccion.y > 0:
                    player.rect.bottom = tile_sprite.rect.top
                    player.direccion.y = 0
                    player.is_grounded = True
                    player.do_salto = True                   
                elif player.direccion.y < 0:
                    player.rect.top = tile_sprite.rect.bottom
                    player.direccion.y = 0
                    player.en_techo = True
                    
        for enemigo in enemys:
            enemigo.get_grounded()
            for boundry_sprite in self.__tiles.sprites():
                if boundry_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.y > 0:
                        enemigo.rect.bottom = boundry_sprite.rect.top
                        enemigo.direccion.y = 0
                        enemigo.is_grounded = True                  
                    elif enemigo.direccion.y < 0:
                        enemigo.rect.top = boundry_sprite.rect.bottom
                        enemigo.direccion.y = 0
                        enemigo.en_techo = True
                
    
        if player.is_grounded and player.direccion.y < 0 or player.direccion.y > 1:
            player.is_grounded = False
        if player.en_techo and player.direccion.y > 0:
            player.en_techo = False
    
    def mover_camara(self):
        player = self.__player.sprite
        player_x = player.rect.centerx
        player_y = player.rect.centery
        direccion_x = player.direccion.x

        if player_x < self.__pantalla.get_width()/4 and direccion_x < 0:
            self.__movimiento_camara[0] = self.__nivel_config.get('velocidad_mover_mapa')
            player.speed = 0
        elif player_x > self.__pantalla.get_width() - (self.__pantalla.get_width()/4) and direccion_x > 0:
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
        
        #background
        self.tileBackground(self.__fondo_stone)

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
            #print(self.__player.sprite.vidas)

        self.mover_camara()

        #tiles
        self.__tiles.update(self.__movimiento_camara[0])
        self.__tiles.draw(self.__pantalla)
        # for tiles in self.__tiles:
        #     pg.draw.rect(self.__pantalla,'red',tiles.rect)

        #boundries
        self.__boundry.update(self.__movimiento_camara[0])
        self.__boundry.draw(self.__pantalla)
        #for boundries in self.__boundry:
        #    self.__pantalla.blit(boundries.image,(0,0))

        #player
        self.__player.update(delta_ms)
        self.movimiento_horizontal_colisiones(delta_ms)
        self.movimiento_vertical_colisiones(delta_ms)
        self.__player.draw(self.__pantalla)
        #pg.draw.rect(self.__pantalla,'red',self.__player.sprite.rect)
        #pg.draw.circle(self.__pantalla, 'red',(self.__player.sprite.rect.centerx+10,self.__player.sprite.rect.centery) ,self.__player.sprite.radius)

        #enemy
        self.__enemy.update(self.__movimiento_camara[0],delta_ms)
        self.__enemy.draw(self.__pantalla)
        #for enemigos in self.__enemy:
            #pg.draw.rect(self.__pantalla,'red',enemigos.rect)
        

        #proyectil
        self.__player.sprite.proyectil_group.update()
        self.__player.sprite.proyectil_group.draw(self.__pantalla)
        

