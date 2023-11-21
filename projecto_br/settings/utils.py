from os import walk
import pygame as pg
import re


def importar_carpeta(path,carpetas_bool = False, imagenes_bool = False):
    dict_animaciones = {}
    lista_imagenes = []
    for _,carpetas,imagenes in walk(path):
        if carpetas_bool:
            for indice_carpetas in range(len(carpetas)):
                dict_animaciones[carpetas[indice_carpetas]] = [] 
        if imagenes_bool:
            for imagen in imagenes:
                path_con_imagen = path + '/' + imagen
                imagen_surf = pg.image.load(path_con_imagen).convert_alpha()
                #if re.findall("player", path):
                ancho = imagen_surf.get_width()
                alto = imagen_surf.get_height()
                imagen_surf = pg.transform.scale(imagen_surf,(ancho*3,alto*3))
                lista_imagenes.append(imagen_surf)
    
    if carpetas_bool:
        return dict_animaciones
    if imagenes_bool:
        return lista_imagenes