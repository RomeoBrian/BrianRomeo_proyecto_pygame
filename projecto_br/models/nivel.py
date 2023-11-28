import pygame as pg
from settings.constantes import TILEZISE,ANCHO,ALTO,open_configs
from models.tiles import Tile
from models.boundries import Boundry
from models.player import Player
from models.enemy import Enemy
from models.trampas import Trampa
from models.fish_coin import Fish_coin
from models.ui import Ui


class Nivel:
    def __init__(self,surface,diccionario_nivel: dict,crear_seleccion_nivel,nivel_actual) -> None:
        self.__pantalla = surface
        self.__trasparent_surface = pg.Surface((ANCHO,ALTO), pg.SRCALPHA)
        self.__nivel_config = diccionario_nivel
        self.__tile_settings = open_configs().get('map_settings')
        #ui
        self.__ui = Ui(self.__pantalla,open_configs().get('ui_settings'))
        self.crear_nivel(self.__nivel_config.get('MAP'))
        self.__lugar_player = 0
        self.__lugar_enemy = 0
        self.__movimiento_camara = pg.math.Vector2()
        self.__enemy_collision = False
        self.__fish_coin_recolectados = 0
        self.__nivel_actual = nivel_actual
        self.crear_seleccion_nivel = crear_seleccion_nivel

        #background
        self.__fondo_stone = pg.image.load('./assets/graphics/background/background_stone.png').convert_alpha()
        self.__fondo_stone = pg.transform.scale(self.__fondo_stone,(self.__fondo_stone.get_width()*2,self.__fondo_stone.get_height()*2))

        #musica
        # pg.mixer.music.load(self.__nivel_config.get('main_theme'))
        # pg.mixer.music.play(loops= -1)
        # pg.mixer.music.set_volume(0.4)
        self.__main_theme = pg.mixer.Sound(self.__nivel_config.get('main_theme'))
        self.__main_theme.play(loops=-1)
        self.__main_theme.set_volume(0.4)
     
    @property
    def fish_coin(self):
        return self.__fish_coin_recolectados
    
    @property
    def player(self):
        return self.__player

    @property
    def nivel_actual(self):
        return self.__nivel_actual

    @property
    def main_theme(self):
        return self.__main_theme

    def crear_nivel(self,layout):
        self.__tiles = pg.sprite.Group()
        self.__boundry = pg.sprite.Group()
        self.__player = pg.sprite.GroupSingle()
        self.__enemy = pg.sprite.Group()
        self.__trampa = pg.sprite.Group()
        self.__fish = pg.sprite.Group()
        for filas_index,filas in enumerate(layout):
            for col_index,celda in enumerate(filas):
                x = col_index * TILEZISE
                y = filas_index * TILEZISE
                for key,tiles in self.__tile_settings.items():
                    match key:
                        case 'tiles_movimiento':
                            for key, valor in tiles.items():
                                if celda == key:
                                    tile = Tile((x,y),TILEZISE,[valor],is_movable = True, direccion_y = True)
                                    self.__tiles.add(tile)
                        case 'tiles_invisibles':
                            for key, valor in tiles.items():
                                if celda == key:
                                    if key == 'b':
                                        boundries = Boundry((x,y),TILEZISE)
                                        self.__boundry.add(boundries)
                                    else:
                                        boundries = Boundry((x,y),TILEZISE,valor)
                                        self.__boundry.add(boundries)
                        case "entidades":
                            for key, valor in tiles.items():
                                if celda == key:
                                    if key == 'P':
                                        player_sprite = Player((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get(valor),self.__pantalla)
                                        self.__player.add(player_sprite)
                                    elif key == 'E':
                                        enemy_sprite = Enemy((x,y),self.__nivel_config.get('gravedad'),self.__nivel_config.get(valor))
                                        self.__enemy.add(enemy_sprite)
                                    elif key == 'T':
                                        trampa = Trampa((x,y),TILEZISE,[valor])
                                        self.__trampa.add(trampa)
                                    elif key == 'f':
                                        fish = Fish_coin((x,y),TILEZISE,self.__nivel_config.get(valor))
                                        self.__fish.add(fish)
                        case _:
                            for key, valor in tiles.items():
                                if celda == key:
                                    tile = Tile((x,y),TILEZISE,[valor])
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
                if player.direccion.x < 0 and not tile_sprite.is_movable:
                    player.frame_index = 0
                    player.rect.left = tile_sprite.rect.right + 3
                    player.a_izquierda = True
                    self.__lugar_player = player.rect.left
                elif player.direccion.x > 0 and not tile_sprite.is_movable:
                    player.frame_index = 0
                    player.rect.right = tile_sprite.rect.left  - 3
                    player.a_derecha = True
                    self.__lugar_player = player.rect.right
        
        for enemigo in enemys:
            enemigo.rect.x += enemigo.direccion.x * enemigo.speed
            enemigo.frame_movimiento += 1
            if enemigo.direccion.x != 0:
                enemigo.campo_vision.center = (enemigo.rect.centerx + (75 * enemigo.direccion.x),enemigo.rect.centery)
            #pg.draw.rect(self.__pantalla,'white',enemigo.campo_vision)
            if enemigo.campo_vision.colliderect(player.rect) and enemigo.ready:
                enemigo.shoot()
                enemigo.ready = False
                enemigo.tiempo_disparo = pg.time.get_ticks()
                
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
            for tile_sprite in self.__tiles.sprites():
                if tile_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.x < 0 and not tile_sprite.is_movable:
                        enemigo.frame_index = 0
                        enemigo.rect.left = tile_sprite.rect.right + 3
                        enemigo.a_izquierda = True
                        self.__lugar_enemy = enemigo.rect.left
                    elif enemigo.direccion.x > 0 and not tile_sprite.is_movable:
                        enemigo.frame_index = 0
                        enemigo.rect.right = tile_sprite.rect.left  - 3
                        enemigo.a_derecha = True
                        self.__lugar_enemy = enemigo.rect.right
            
        #enemy
        if len(self.__enemy) > 0:
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
            for tile_sprite in self.__tiles.sprites():
                if tile_sprite.rect.colliderect(enemigo.rect):
                    if enemigo.direccion.y > 0:
                        enemigo.rect.bottom = tile_sprite.rect.top
                        enemigo.direccion.y = 0
                        enemigo.is_grounded = True                  
                    elif enemigo.direccion.y < 0:
                        enemigo.rect.top = tile_sprite.rect.bottom
                        enemigo.direccion.y = 0
                        enemigo.en_techo = True
                
    
        if player.is_grounded and player.direccion.y < 0 or player.direccion.y > 1:
            player.is_grounded = False
        if player.en_techo and player.direccion.y > 0:
            player.en_techo = False
    
    def mover_camara(self,pausa):
        player = self.__player.sprite
        player_x = player.rect.centerx
        player_y = player.rect.centery
        direccion_x = player.direccion.x
        if not pausa:
            if player_x < self.__pantalla.get_width()/4 and direccion_x < 0:
                self.__movimiento_camara[0] = self.__nivel_config.get('velocidad_mover_mapa')
                player.speed = 0
            elif player_x > self.__pantalla.get_width() - (self.__pantalla.get_width()/4) and direccion_x > 0:
                self.__movimiento_camara[0] = -self.__nivel_config.get('velocidad_mover_mapa')
                player.speed = 0
            else:
                self.__movimiento_camara[0] = 0
                player.speed = self.__nivel_config.get('player').get('speed')
        else:
            self.__movimiento_camara[0] = 0
            player.speed = self.__nivel_config.get('player').get('speed')

    def ataque_enemigo(self):
        for enemigos in self.__enemy:
            if pg.sprite.spritecollide(enemigos, self.__player, False):
                self.__enemy_collision = True

    def damage_trampas(self):
        for trampas in self.__trampa:
            if trampas.rect.colliderect(self.__player.sprite.rect):
                trampas.contacto = True                
                

    def run(self,delta_ms,pausa):        
        self.mover_camara(pausa)
        
        #background
        self.tileBackground(self.__fondo_stone)

        #mensaje
        self.__ui.dibujar_texto('Para moverte podes usar awsd',50,(50,50),'white')

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
        self.__player.update(delta_ms,pausa)
        if not pausa:
            self.movimiento_horizontal_colisiones(delta_ms)
            self.movimiento_vertical_colisiones(delta_ms)
        self.__player.draw(self.__pantalla)
        #pg.draw.rect(self.__pantalla,'red',self.__player.sprite.rect)
        #pg.draw.circle(self.__pantalla, 'red',(self.__player.sprite.rect.centerx+10,self.__player.sprite.rect.centery) ,self.__player.sprite.radius)

        #enemy
        self.__enemy.update(self.__movimiento_camara[0],delta_ms,pausa)
        self.__enemy.draw(self.__pantalla)
        #for enemigos in self.__enemy:
            #pg.draw.rect(self.__pantalla,'red',enemigos.rect)
        
        #trampa
        self.__trampa.update(self.__movimiento_camara[0])
        self.__trampa.draw(self.__pantalla)

        #Fish
        self.__fish.update(self.__movimiento_camara[0],delta_ms,pausa)
        self.__fish.draw(self.__pantalla)
        
        #proyectil
        self.__player.sprite.proyectil_group.update(delta_ms)
        # for proyectil in self.__player.sprite.proyectil_group:
        #     pg.draw.rect(self.__pantalla,'red',proyectil.rect)
        self.__player.sprite.proyectil_group.draw(self.__pantalla)

        for enemigo in self.__enemy:
            enemigo.proyectil_group.update(delta_ms)
            enemigo.proyectil_group.draw(self.__pantalla)
        
        
        #colliosiones y muertes del enemigo
        if self.__player.sprite.is_hitting:
            for enemigos in self.__enemy:
                if self.__player.sprite.atack_rect.colliderect(enemigos):                 
                    enemigos.hit(self.__player.sprite.fuerza)
                    self.__player.sprite.is_hitting = False
            
            #colision bala del player con enemigo    
            enemigo_golpeado = pg.sprite.groupcollide(self.__player.sprite.proyectil_group,self.__enemy,True,False)
            for key in enemigo_golpeado:
                enemigo_golpeado[key][0].hit(self.__player.sprite.fuerza_disparo)
                self.__player.sprite.is_hitting = False

        #colision proyectil con tiles
        pg.sprite.groupcollide(self.__player.sprite.proyectil_group,self.__tiles,True,False)

        #colision proyectil con tiles
        pg.sprite.groupcollide(self.__player.sprite.proyectil_group,self.__tiles,True,False)

        #player death
        self.ataque_enemigo()
        if self.__enemy_collision:
            self.__enemy_collision = False
            self.__player.sprite.recibir_golpe(1)  
        
        #contacto con trampa
        self.damage_trampas()
        for trampa in self.__trampa:
            if trampa.contacto == True:
                damage = trampa.do_damage()
                self.__player.sprite.recibir_golpe(damage)

        #colision con fish coin
        if pg.sprite.spritecollide(self.__player.sprite, self.__fish,True):
            self.__fish_coin_recolectados += 1
            if len(self.__fish) == 0:
                print('Se recolectaron todos los fish coin')
        

        for enemigo in self.__enemy:
            if pg.sprite.spritecollide(self.__player.sprite,enemigo.proyectil_group, True):
                self.__player.sprite.recibir_golpe(enemigo.fuerza_proyectil)

        #condicion de Victoria
        if len(self.__fish) == 0 and len(self.__enemy) == 0:
                color_fondo_gana = (20, 19, 39,150)
                pg.draw.rect(self.__trasparent_surface,color_fondo_gana,[0,0,ANCHO,ALTO])
                #self.crear_seleccion_nivel(self.__nivel_actual,self.__nivel_config['desbloquea'])
                #print('Se gano el nivel')
        

