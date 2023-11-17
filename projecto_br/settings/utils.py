from os import walk
import pygame as pg
import re

def importar_carpeta(path):
    lista_imagenes = []

    for _,__,imagenes in walk(path):
        for imagen in imagenes:
            path_con_imagen = path + '/' + imagen
            imagen_surf = pg.image.load(path_con_imagen).convert_alpha()
            if re.findall("player", path):
                ancho = imagen_surf.get_width()
                alto = imagen_surf.get_height()
                imagen_surf = pg.transform.scale(imagen_surf,(ancho*3,alto*3))
                
            lista_imagenes.append(imagen_surf)

    return lista_imagenes