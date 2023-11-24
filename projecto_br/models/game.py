import pygame as pg, sys
from settings.constantes import ANCHO,FPS,ALTO,open_configs
from models.nivel import Nivel

class Game:
    def __init__(self) -> None:
        pg.init()
        self.__config = open_configs().get('debug')
        MAP = self.__config.get('MAP')
        self.ancho_nivel = len(MAP)
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        pg.display.set_caption("Unamed plataformer")
        self.clock = pg.time.Clock()
        self.__nivel = Nivel(MAP,self.screen,self.__config,self.ancho_nivel)
        self.fog = pg.Surface((ANCHO,ALTO))
        self.fog.fill((91, 94, 94))
        self.fag_rect = self.fog.get_rect(topleft = (0,0))

        


    def run(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                    
        
            self.screen.fill((20, 19, 39))
            #set nivel
            delta_ms = self.clock.tick(FPS)
            self.__nivel.run(delta_ms)
            #self.screen.blit(self.fog,(0,0), special_flags=3)
            
            pg.display.update()