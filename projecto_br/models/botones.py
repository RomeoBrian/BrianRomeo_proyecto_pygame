import pygame as pg
from settings.constantes import open_configs
from models.ui import Ui

class Boton():
    def __init__(self,pos,pantalla,text_input,image,scale = 1) -> None:
        #ui
        self.__config_ui = open_configs().get('ui_settings')
        self.__ui = Ui(pantalla,self.__config_ui)
        self.__text_input = text_input
        self.__text = self.__ui.renderizar_texto(self.__text_input,20,pos,'white')
        if image != None:
            self.image = pg.transform.scale(image,(int(image.get_width()*scale), int(image.get_height()*scale)))
        else:
            self.image = self.__text
        self.rect = self.image.get_rect(center = pos)
        self.__text_rect = self.__text.get_rect(center = pos)
        self.__clicked = False

    def draw(self,pantalla):
        accion = False
        mouse_pos = pg.mouse.get_pos()
    
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.__clicked:
                self.__clicked = True
                accion = True
        if pg.mouse.get_pressed()[0] == 0:
            self.__clicked = False
        
        if self.image is not None:
            pantalla.blit(self.image, self.rect)
        pantalla.blit(self.__text, self.__text_rect)
        #pantalla.blit(self.image, (self.rect.x, self.rect.y))
        
        return accion