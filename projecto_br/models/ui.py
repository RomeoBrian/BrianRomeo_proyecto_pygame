import pygame as pg

class Ui():
    def __init__(self,pantalla,configs: dict):
        self.__pantalla = pantalla
        self.__ui_configs = configs
        self.__font = self.__ui_configs.get('font')

        #vida
        self.__imagen_barra_vida = pg.image.load(self.__ui_configs.get('healt_bar'))
        self.__corazon = pg.image.load(self.__ui_configs.get('heart'))
        self.__barra_vida_topleft = self.__ui_configs.get('barra_vida_topleft')#(65,22)
        self.__maximo_ancho_barra = self.__ui_configs.get('maximo_ancho_barra')
        self.__altura_barra = self.__ui_configs.get('altura_barra')

        #Fish coin
        self.__fish_coin = pg.image.load(self.__ui_configs.get('fish_coin'))
        self.__fish_rect = self.__fish_coin.get_rect(topleft = self.__ui_configs.get('topleft_fish'))
        

    def renderizar_texto(self,texto,size,pos,color):
        font = pg.font.Font(self.__font,size)
        texto_surface = font.render(texto,True,color)
        return texto_surface
    
    def dibujar_texto(self,texto,size,pos,color):
        texto_surface = self.renderizar_texto(texto,size,pos,color)
        texto_rect = texto_surface.get_rect(center = pos)
        self.__pantalla.blit(texto_surface,texto_rect)
    
    def mostar_vida(self,vida_actual,vida_maxima):
        self.__pantalla.blit(self.__imagen_barra_vida,(20,10))
        self.__pantalla.blit(self.__corazon,(20,10))
        ratio_vida_actual = vida_actual/vida_maxima
        ancho_actual_barra = self.__maximo_ancho_barra * ratio_vida_actual
        vida_rect = pg.Rect((self.__barra_vida_topleft),(ancho_actual_barra,self.__altura_barra))
        pg.draw.rect(self.__pantalla,(255,0,0),vida_rect)
    
    def mostrar_fish(self,cantidad):
        self.__pantalla.blit(self.__fish_coin,self.__fish_rect)
        self.dibujar_texto(str(cantidad),20,(self.__fish_rect.right + 10,self.__fish_rect.centery),'#c3c7c7')
        # cantidad_fish = self.font.render(str(cantidad),False,'#c3c7c7')
        # cantidad_fish_rec = cantidad_fish.get_rect(midleft = (self.__fish_rect.right + 4,self.__fish_rect.centery))
        # self.__pantalla.blit(cantidad_fish,cantidad_fish_rec)

