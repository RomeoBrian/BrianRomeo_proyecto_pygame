import pygame as pg, sys
from settings.constantes import ANCHO,ALTO,FPS,MAP
from models.nivel import Nivel


class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((ANCHO,ALTO))
        pg.display.set_caption("Unamed plataformer")
        self.clock = pg.time.Clock()
        self.__nivel = Nivel(MAP,self.screen)

    def run(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        
            self.screen.fill('black')
            #set nivel
            self.__nivel.run()

            pg.display.update()
            self.clock.tick(FPS)
            


if __name__ == '__main__':
    game = Game()
    game.run()
    
