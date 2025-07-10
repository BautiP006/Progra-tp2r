import random
import pygame
from BaseV2 import *

# --- FUNCIONES DE UTILIDAD ---

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """
    Dibuja texto multilínea en la superficie, ajustando el salto de línea si es necesario.
    """
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def mezclar_lista(lista_preguntas: list) -> None:
    """
    Mezcla la lista de preguntas in-place.
    """
    random.shuffle(lista_preguntas)

def verificar_respuesta(datos_juego: dict, pregunta_actual: dict, respuesta: int) -> bool:
    """
    Verifica si la respuesta es correcta y actualiza el puntaje y vidas.
    """
    if respuesta == pregunta_actual["respuesta_correcta"]:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        return True
    else:
        # SIN PUNTOS NEGATIVOS
        if datos_juego["puntuacion"] > PUNTUACION_ERROR:
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
        # CON PUNTOS NEGATIVOS (descomentar si lo deseas)
        # datos_juego["puntuacion"] -= PUNTUACION_ERROR
        datos_juego["vidas"] -= 1
        return False

def reiniciar_estadisticas(datos_juego: dict):
    """
    Reinicia el puntaje y las vidas del jugador.
    """
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS