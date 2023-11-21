import pygame as pg, sys
from settings.constantes import ANCHO,FPS,TILEZISE,open_configs
from models.nivel import Nivel

class Game:
    def __init__(self) -> None:
        pg.init()
        self.__config = open_configs().get('debug')
        MAP = self.__config.get('MAP')
        ALTO = len(MAP) * TILEZISE
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        pg.display.set_caption("Unamed plataformer")
        self.clock = pg.time.Clock()
        self.__nivel = Nivel(MAP,self.screen,self.__config)
        self.fog = pg.Surface((ANCHO,ALTO))
        self.fog.fill((91, 94, 94))
        self.fag_rect = self.fog.get_rect(topleft = (0,0))

        #background
        self.imagen_fondo = pg.image.load('./assets/graphics/background/Background_1.png')
        self.imagen_fondo = pg.transform.scale(self.imagen_fondo,(ANCHO,ALTO))

        self.imagen_nubes = pg.image.load('./assets/graphics/background/Background_2.png')
        self.imagen_nubes = pg.transform.scale(self.imagen_nubes,(ANCHO,self.imagen_nubes.get_height()))


    def run(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                    
        
            self.screen.fill((20, 19, 39))
            self.screen.blit(self.imagen_fondo,(0,0))
            self.screen.blit(self.imagen_nubes,(0,0))
            #set nivel
            delta_ms = self.clock.tick(FPS)
            self.__nivel.run(delta_ms)
            #self.screen.blit(self.fog,(0,0), special_flags=3)
            
            pg.display.update()