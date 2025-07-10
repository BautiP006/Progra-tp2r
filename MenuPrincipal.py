import pygame
from BaseV2 import *
from Funciones import mostrar_texto

# --- CONSTANTES Y CONFIGURACIÓN ---
pygame.init()
fuente_menu = pygame.font.SysFont("Arial Black", 32)
NOMBRES_BOTONES = ["JUGAR", "CONFIGURACION", "PUNTUACIONES", "AGREGAR PREGUNTA", "SALIR"]

# Cargar y escalar fondo solo una vez
def cargar_fondo(ruta, tamaño):
    """
    Carga y escala una imagen de fondo.

    Args:
        ruta (str): Ruta de la imagen.
        tamaño (tuple[int, int]): Dimensiones de la superficie destino.

    Returns:
        pygame.Surface: Imagen escalada.
    """
    fondo = pygame.image.load(ruta)
    return pygame.transform.scale(fondo, tamaño)

FONDO_MENU = cargar_fondo("images.jpeg", (1400, 900))

# --- FUNCIÓN PARA DIBUJAR BOTONES ---
def dibujar_boton(pantalla, rect, texto, fuente, color_borde, color_fondo, color_texto, hover=False):
    pygame.draw.rect(pantalla, color_borde, rect, border_radius=18)
    pygame.draw.rect(pantalla, color_fondo, rect.inflate(-6, -6), border_radius=16)
    texto_render = fuente.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)
    """
    Dibuja un botón con texto en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie destino.
        rect (pygame.Rect): Rectángulo del botón.
        texto (str): Texto a mostrar.
        fuente (pygame.font.Font): Fuente del texto.
        color_borde (tuple): Color del borde.
        color_fondo (tuple): Color de fondo.
        color_texto (tuple): Color del texto.
        hover (bool): Si el botón está en estado hover.
    """

# --- FUNCIÓN PRINCIPAL DEL MENÚ ---
def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    """
    Renderiza el menú principal y gestiona la navegación entre pantallas.

    Args:
        pantalla (pygame.Surface): Superficie principal.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de pygame.

    Returns:
        str: Estado siguiente del flujo del juego.
    """
    retorno = "menu"
    pantalla.blit(FONDO_MENU, (0, 0))

    # Definición de botones
    posiciones = [(125, 115), (125, 195), (125, 275), (125, 355), (125, 435)]
    ancho_boton, alto_boton = 400, 60
    color_normal = (0, 120, 255)
    color_hover = (0, 180, 255)
    color_borde = (255, 255, 255)
    color_texto = (255, 255, 255)

    mouse_pos = pygame.mouse.get_pos()
    botones_rect = []

    for i, (x, y) in enumerate(posiciones):
        rect = pygame.Rect(x, y, ancho_boton, alto_boton)
        botones_rect.append(rect)
        hover = rect.collidepoint(mouse_pos)
        color = color_hover if hover else color_normal
        dibujar_boton(pantalla, rect, NOMBRES_BOTONES[i], fuente_menu, color_borde, color, color_texto, hover)

    # --- PROCESAR EVENTOS ---
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, rect in enumerate(botones_rect):
                if rect.collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    nombre = NOMBRES_BOTONES[i]
                    if nombre == "SALIR":
                        return "salir"
                    elif nombre == "JUGAR":
                        return "juego"
                    elif nombre == "PUNTUACIONES":
                        return "rankings"
                    elif nombre == "CONFIGURACION":
                        return "configuraciones"
                    elif nombre == "AGREGAR PREGUNTA":
                        return "agregar_preguntas"
        elif evento.type == pygame.QUIT:
            return "salir"

    return retorno