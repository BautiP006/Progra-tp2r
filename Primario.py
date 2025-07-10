import pygame
import csv
from BaseV2 import *
from MenuPrincipal import *
from MainJuego import *
from ConfiguracionV2 import *
from Tabla_Posiciones import *
from MenuFinal import *
from BaseV2 import CLICK_SONIDO, click_muteado

# --- CONFIGURACIÓN DE VENTANA Y JUEGO ---
ancho_ventana = 1400
alto_ventana = 900
VENTANA = (ancho_ventana, alto_ventana)
CANTIDAD_VIDAS = 3
FPS = 40  # Cuadros por segundo

# --- ESTADO DEL JUEGO ---
datos_juego = {
    "puntuacion": 0,
    "vidas": CANTIDAD_VIDAS,
    "nombre": "",
    "volumen_musica": 100,
    "racha": 0,
    "tiempo": 25,  # segundos por pregunta
    "musica_activada": True
}

# --- INICIALIZACIÓN DE PYGAME Y RECURSOS ---
pygame.init()
pygame.mixer.init()
CLICK_SONIDO = pygame.mixer.Sound("click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("error.mp3")
click_muteado = False
pygame.display.set_caption("Juego de Preguntas y Respuestas")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(VENTANA)
corriendo = True
reloj = pygame.time.Clock()
ventana_actual = "menu"
bandera_musica = False
partida_iniciada = False

# --- BUCLE PRINCIPAL ---
while corriendo:
    """
    Bucle principal del juego. Gestiona el ciclo de eventos, la música,
    el flujo entre pantallas y el renderizado general.

    Controla:
        - Volumen y reproducción de música.
        - Navegación entre ventanas principales (menú, juego, configuración, rankings, agregar preguntas, final, salir).
        - Inicialización y reinicio de partida.
        - Actualización de pantalla y cierre de pygame.
    """
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    # --- CONTROL DE MÚSICA ---
    pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
    if datos_juego["musica_activada"] and not bandera_musica:
        pygame.mixer.music.load("musica_inicio.mp3")
        pygame.mixer.music.play(-1)
        bandera_musica = True
    elif not datos_juego["musica_activada"] and bandera_musica:
        pygame.mixer.music.stop()
        bandera_musica = False

    # --- CONTROL DE VENTANAS ---
    if ventana_actual == "menu":
        partida_iniciada = False
        ventana_actual = mostrar_menu(pantalla, cola_eventos)

    elif ventana_actual == "juego":
        if not partida_iniciada:
            reiniciar_juego()
            datos_juego["vidas"] = CANTIDAD_VIDAS
            datos_juego["puntuacion"] = 0
            datos_juego["nombre"] = ""
            datos_juego["racha"] = 0
            datos_juego["tiempo"] = 25
            partida_iniciada = True
        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "configuraciones":
        ventana_actual = mostrar_configuracion(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos)

    elif ventana_actual == "agregar_preguntas":
        ventana_actual = mostrar_agregar_preguntas(pantalla, datos_juego, cola_eventos)

    elif ventana_actual == "terminado":
        partida_iniciada = False
        if bandera_musica:
            pygame.mixer.music.stop()
            bandera_musica = False
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "salir":
        corriendo = False

    pygame.display.flip()

pygame.quit()