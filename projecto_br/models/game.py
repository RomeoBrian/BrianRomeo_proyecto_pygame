import pygame as pg, sys
from settings.constantes import ANCHO,FPS,ALTO,open_configs
from models.nivel import Nivel
from models.ui import Ui
from models.nivel_select import Nivel_select
from models.botones import Boton
from models.menu_opciones import Opciones

class Game:
    
    def __init__(self) -> None:
        pg.init()
        self.__nivel_maximo_alcanzado = 0
        self.__config = open_configs()
        self.__niveles = open_configs().get('level_manager_settings')
        self.__estado = 'seleccion'
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        self.surface = pg.Surface((ANCHO,ALTO), pg.SRCALPHA)
        self.__color_fondo = (20, 19, 39,255)
        pg.display.set_caption("Unamed plataformer")
        self.clock = pg.time.Clock()
        self.__nivel_select = Nivel_select(0,self.__nivel_maximo_alcanzado,self.screen,self.crear_nivel)
        #self.__nivel = Nivel(MAP,self.screen,self.__nivel_config,self.ancho_nivel)
        self.fog = pg.Surface((ANCHO,ALTO))
        self.fog.fill((91, 94, 94))
        self.fag_rect = self.fog.get_rect(topleft = (0,0))
        self.__cliked = False

        #pausa
        self.__game_pausa = False
        self.__button_image = pg.image.load(open_configs().get('ui_settings').get('boton')).convert_alpha()

        #crear Boton
        self.__boton_resume = Boton(((ANCHO/2),(ALTO/2) - 90),self.screen,'SALIR PAUSA',None,0.5)
        self.__boton_opciones = Boton(((ANCHO/2),(ALTO/2) - 10),self.screen,'OPCIONES',None,0.5)
        self.__boton_volver = Boton(((ANCHO/2),(ALTO/2) + 70),self.screen,'VOLVER AL MENU',None,0.5)


        #ui
        self.__ui = Ui(self.screen,self.__config.get('ui_settings'))

        #opciones
        self.__opciones = Opciones(True,self.screen)

    def crear_seleccion_nivel(self,nivel_actual,nuevo_maximo_nivel):
        if nuevo_maximo_nivel > self.__nivel_maximo_alcanzado:
            self.__nivel_maximo_alcanzado = nuevo_maximo_nivel
        self.__nivel_select = Nivel_select(nivel_actual,self.__nivel_maximo_alcanzado,self.screen,self.crear_nivel)
        self.__estado = 'seleccion'
        self.__nivel.main_theme.stop()
        self.__game_pausa = False
    
    def crear_nivel(self,nivel_actual):
        nivel_config = self.__config.get(self.__niveles[nivel_actual]['contenido'])
        self.__nivel = Nivel(self.screen,nivel_config,self.crear_seleccion_nivel,nivel_actual)
        self.__estado = 'nivel'

    def vovler_estado(self,estado):
        self.__estado = estado

    def run(self,manejar_estado):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_ESCAPE:
                        if self.__game_pausa:
                            self.__game_pausa = False
                        else:
                            self.__game_pausa = True
                if evento.type == pg.MOUSEBUTTONUP:
                    self.__cliked = False
                
                
                    
        
            self.screen.fill(self.__color_fondo)
            #set nivel
            delta_ms = self.clock.tick(FPS)
            if self.__estado == 'seleccion':
                self.__ui.dibujar_texto('SELECCION DE NIVEL',50,((ANCHO/2),(ALTO/2) - 300),'white')
                self.__nivel_select.run()
            else:
                self.__nivel.run(delta_ms,self.__game_pausa)
                self.__ui.mostar_vida(self.__nivel.player.sprite.vidas,self.__nivel.player.sprite.vida_maxima)
                self.__ui.mostrar_fish(self.__nivel.fish_coin)
                if self.__game_pausa:
                    color_fondo_pausa = (20, 19, 39,150)
                    pg.draw.rect(self.surface,color_fondo_pausa,[0,0,ANCHO,ALTO])
                    self.screen.blit(self.surface,(0,0))
                    if self.__estado == 'nivel':
                        self.__ui.dibujar_texto('PAUSA',50,((ANCHO/2),(ALTO/2) - 300),'white')
                        if self.__boton_resume.draw(self.screen) and not self.__cliked:
                            self.__game_pausa = False
                            self.__cliked = True
                        elif self.__boton_opciones.draw(self.screen) and not self.__cliked:
                            self.__estado = 'opciones'
                            self.__cliked = True
                        elif self.__boton_volver.draw(self.screen) and not self.__cliked:
                            self.__nivel.crear_seleccion_nivel(self.__nivel.nivel_actual,self.__nivel_maximo_alcanzado)
                            self.__cliked = True
                    if self.__estado == 'opciones':
                        self.__opciones.run(self.vovler_estado,'nivel')
                
                
            #self.screen.blit(self.fog,(0,0), special_flags=3)


            pg.display.update()