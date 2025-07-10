import pygame
import json
from datetime import datetime
from Funciones import mostrar_texto

# --- CONSTANTES Y CONFIGURACIÓN ---
pygame.init()
CUADRO_TEXTO = (400, 80)
COLOR_AZUL = (0, 120, 255)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

fuente_titulo = pygame.font.SysFont("Arial Black", 38)
fuente_input = pygame.font.SysFont("Arial", 32)
fuente_ranking = pygame.font.SysFont("Arial", 28)

# --- FUNCIONES MODULARES ---

def guardar_partida(nombre, puntaje):
    """
    Guarda una partida en el archivo JSON de rankings.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje obtenido.
    """
    try:
        with open("partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except FileNotFoundError:
        partidas = []

    partidas.append({
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    partidas.sort(key=lambda x: x["puntaje"], reverse=True)

    with open("partidas.json", "w", encoding="utf-8") as f:
        json.dump(partidas, f, ensure_ascii=False, indent=2)

def mostrar_ranking(pantalla, color_boton, color_boton_hover, color_borde):
    """
    Dibuja el ranking de las 10 mejores partidas y el botón VOLVER.

    Args:
        pantalla (pygame.Surface): Superficie de destino.
        color_boton (tuple): Color base del botón.
        color_boton_hover (tuple): Color hover del botón.
        color_borde (tuple): Color del borde del botón.

    Returns:
        pygame.Rect: Rectángulo del botón VOLVER.
    """
    try:
        with open("partidas.json", "r", encoding="utf-8") as f:
            partidas = json.load(f)
    except:
        partidas = []
    partidas.sort(key=lambda x: x["puntaje"], reverse=True)

    # Título
    titulo = fuente_titulo.render("TOP 10 PARTIDAS", True, color_boton)
    pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 40))

    # Ranking
    for i, partida in enumerate(partidas[:10]):
        texto = f"{i+1}. {partida['nombre']} - {partida['puntaje']} pts - {partida['fecha']}"
        texto_render = fuente_ranking.render(texto, True, COLOR_NEGRO)
        pantalla.blit(texto_render, (pantalla.get_width() // 2 - 320, 100 + i * 35))

    # Botón VOLVER
    boton_volver = pygame.Rect(pantalla.get_width() // 2 - 80, 500, 160, 50)
    mouse_pos = pygame.mouse.get_pos()
    color_btn = color_boton_hover if boton_volver.collidepoint(mouse_pos) else color_boton
    pygame.draw.rect(pantalla, color_btn, boton_volver, border_radius=15)
    pygame.draw.rect(pantalla, color_borde, boton_volver, 3, border_radius=15)
    txt_volver = fuente_input.render("VOLVER", True, COLOR_BLANCO)
    pantalla.blit(txt_volver, txt_volver.get_rect(center=boton_volver.center))
    return boton_volver

def mostrar_input_nombre(pantalla, nombre, color_boton, color_borde, color_input, color_texto):
    """
    Dibuja la interfaz para ingresar el nombre del jugador.

    Args:
        pantalla (pygame.Surface): Superficie de destino.
        nombre (str): Nombre actual ingresado.
        color_boton (tuple): Color del título.
        color_borde (tuple): Color del borde de la caja.
        color_input (tuple): Color de fondo de la caja.
        color_texto (tuple): Color del texto.
    """
    # Título
    titulo = fuente_titulo.render("¡Juego terminado!", True, color_boton)
    pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 60))

    # Instrucción
    instruccion = fuente_ranking.render("Ingrese su nombre y presione ENTER:", True, color_texto)
    pantalla.blit(instruccion, (pantalla.get_width() // 2 - instruccion.get_width() // 2, 160))

    # Caja de texto para el nombre
    input_rect = pygame.Rect(pantalla.get_width() // 2 - 200, 220, 400, 50)
    pygame.draw.rect(pantalla, color_input, input_rect, border_radius=12)
    pygame.draw.rect(pantalla, color_borde, input_rect, 3, border_radius=12)
    texto_nombre = fuente_input.render(nombre, True, color_texto)
    pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 10))

    # Sombra o glow
    pygame.draw.rect(pantalla, (180, 180, 255), input_rect.inflate(12, 12), 6, border_radius=16)

# --- FUNCIÓN PRINCIPAL DE PANTALLA FINAL ---
def mostrar_fin_juego(pantalla, cola_eventos, datos_juego):
    """
    Controla la pantalla final: ingreso de nombre, guardado y muestra del ranking.

    Args:
        pantalla (pygame.Surface): Superficie de destino.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de pygame.
        datos_juego (dict): Estado final del jugador.

    Returns:
        str: Estado siguiente del flujo ("menu").
    """
    nombre = ""
    escribiendo = True
    ranking_mostrado = False
    color_fondo = (230, 230, 255)
    color_input = (255, 255, 255)
    color_borde = (0, 120, 255)
    color_texto = (0, 0, 0)
    color_boton = (0, 120, 255)
    color_boton_hover = (0, 180, 255)

    while escribiendo:
        pantalla.fill(color_fondo)

        if not ranking_mostrado:
            mostrar_input_nombre(pantalla, nombre, color_boton, color_borde, color_input, color_texto)
        else:
            boton_volver = mostrar_ranking(pantalla, color_boton, color_boton_hover, color_borde)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "menu"
            elif evento.type == pygame.KEYDOWN:
                if not ranking_mostrado:
                    if evento.key == pygame.K_RETURN and nombre.strip() != "":
                        guardar_partida(nombre, datos_juego["puntuacion"])
                        ranking_mostrado = True
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    elif len(nombre) < 15 and evento.unicode.isprintable():
                        nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN and ranking_mostrado:
                boton_volver = pygame.Rect(pantalla.get_width() // 2 - 80, 500, 160, 50)
                if boton_volver.collidepoint(evento.pos):
                    return "menu"