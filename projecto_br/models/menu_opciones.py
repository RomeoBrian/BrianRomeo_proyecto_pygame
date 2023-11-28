import pygame as pg, sys
from settings.constantes import ANCHO,ALTO,FPS,open_configs
from models.botones import Boton
from models.ui import Ui

class Opciones():
    def __init__(self,click: bool,pantalla) -> None:
        self.__button_image = pg.image.load(open_configs().get('ui_settings').get('boton')).convert_alpha()
        self.__pantalla = pantalla
        #crear Boton
        self.__boton_audio = Boton(((ANCHO/2),(ALTO/2) - 90),self.__pantalla,'AUDIO',None,0.5)
        self.__boton_teclas = Boton(((ANCHO/2),(ALTO/2) - 10),self.__pantalla,'TECLAS',None,0.5)
        self.__boton_volver = Boton(((ANCHO/2),(ALTO/2) + 70),self.__pantalla,'VOLVER',None,0.5)
        self.__clicked = click
        self.clock = pg.time.Clock()

        

    def run(self,volver_estado,menu_anterior):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if evento.type == pg.MOUSEBUTTONUP:
                    self.__clicked = False
        #ui
        ui = Ui(self.__pantalla,open_configs().get('ui_settings'))
        ui.dibujar_texto('Opciones',50,((ANCHO/2),(ALTO/2) - 300),'white')
        if self.__boton_audio.draw(self.__pantalla) and not self.__clicked:
            print('audio')
            self.__clicked = True
        if self.__boton_teclas.draw(self.__pantalla) and not self.__clicked:
            print('teclas')
            self.__clicked = True
        if self.__boton_volver.draw(self.__pantalla) and not self.__clicked:
            match menu_anterior:
                case 'nivel':
                    volver_estado('nivel')
                case 'main':
                    volver_estado('main')
            self.__clicked = True
                