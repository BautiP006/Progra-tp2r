import pygame
from BaseV2 import *
from Funciones import mostrar_texto

TAMAÑO_BOTON_VOLUMEN = (100,50)
TAMAÑO_BOTON_VOLVER = (120,50)
TAMAÑO_BOTON_MUSICA = (200,50)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)

pygame.init()

fuente_boton = pygame.font.SysFont("Arial Narrow",23)
fuente_volumen = pygame.font.SysFont("Arial Narrow",50)

boton_suma = {}
boton_suma["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_suma["rectangulo"] = boton_suma["superficie"].get_rect()
boton_suma["superficie"].fill(COLOR_ROJO)

boton_resta = {}
boton_resta["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLUMEN)
boton_resta["rectangulo"] = boton_resta["superficie"].get_rect()
boton_resta["superficie"].fill(COLOR_ROJO)

boton_volver = {}
boton_volver["superficie"] = pygame.Surface(TAMAÑO_BOTON_VOLVER)
boton_volver["rectangulo"] = boton_volver["superficie"].get_rect()
boton_volver["superficie"].fill(COLOR_AZUL)

boton_musica = {}
boton_musica["superficie"] = pygame.Surface(TAMAÑO_BOTON_MUSICA)
boton_musica["rectangulo"] = boton_musica["superficie"].get_rect()
boton_musica["superficie"].fill(COLOR_AZUL)

def mostrar_configuracion(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    global click_muteado
    retorno = "configuraciones"

    # --- FONDO GRIS ---
    pantalla.fill((60, 60, 60))

    # --- TÍTULO ---
    fuente_titulo = pygame.font.SysFont("Arial Black", 48)
    titulo = fuente_titulo.render("CONFIGURACIÓN", True, (255, 255, 255))
    pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 40))

    # --- BOTONES ---
    x_centro = pantalla.get_width() // 2
    y_vol = 180

    # Botón Volumen -
    boton_resta["rectangulo"] = pygame.Rect(x_centro - 160, y_vol, 100, 60)
    boton_resta["superficie"] = pygame.Surface((100, 60), pygame.SRCALPHA)
    boton_resta["superficie"].fill((200, 50, 50))
    pygame.draw.rect(boton_resta["superficie"], (255,255,255), (0,0,100,60), 3, border_radius=15)
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"].topleft)
    mostrar_texto(pantalla, "VOL -", (boton_resta["rectangulo"].x + 15, boton_resta["rectangulo"].y + 15), fuente_boton, COLOR_BLANCO)

    # Botón Volumen +
    boton_suma["rectangulo"] = pygame.Rect(x_centro + 60, y_vol, 100, 60)
    boton_suma["superficie"] = pygame.Surface((100, 60), pygame.SRCALPHA)
    boton_suma["superficie"].fill((50, 200, 50))
    pygame.draw.rect(boton_suma["superficie"], (255,255,255), (0,0,100,60), 3, border_radius=15)
    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"].topleft)
    mostrar_texto(pantalla, "VOL +", (boton_suma["rectangulo"].x + 15, boton_suma["rectangulo"].y + 15), fuente_boton, COLOR_BLANCO)

    # Porcentaje de volumen
    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']} %", (x_centro - 30, y_vol + 15), fuente_volumen, COLOR_BLANCO)

    # Botón música ON/OFF
    boton_musica["rectangulo"] = pygame.Rect(x_centro - 100, y_vol + 100, 200, 60)
    boton_musica["superficie"] = pygame.Surface((200, 60), pygame.SRCALPHA)
    boton_musica["superficie"].fill((0, 120, 255))
    pygame.draw.rect(boton_musica["superficie"], (255,255,255), (0,0,200,60), 3, border_radius=15)
    pantalla.blit(boton_musica["superficie"], boton_musica["rectangulo"].topleft)
    estado_musica = "ON" if datos_juego["musica_activada"] else "OFF"
    mostrar_texto(pantalla, f"MUSICA {estado_musica}", (boton_musica["rectangulo"].x + 20, boton_musica["rectangulo"].y + 15), fuente_boton, COLOR_BLANCO)

    # Botón CLICK ON/OFF
    boton_click = pygame.Rect(x_centro - 100, y_vol + 180, 200, 60)
    color_click = (200, 50, 50) if click_muteado else (0, 180, 100)
    pygame.draw.rect(pantalla, color_click, boton_click, border_radius=15)
    pygame.draw.rect(pantalla, (255,255,255), boton_click, 3, border_radius=15)
    texto_click = "CLICK: MUTED" if click_muteado else "CLICK: ACTIVO"
    fuente_btn = pygame.font.SysFont("Arial Black", 28)
    txt_btn = fuente_btn.render(texto_click, True, (255,255,255))
    pantalla.blit(txt_btn, txt_btn.get_rect(center=boton_click.center))

    # Botón volver
    boton_volver["rectangulo"] = pygame.Rect(30, pantalla.get_height() - 80, 160, 50)
    boton_volver["superficie"] = pygame.Surface((160, 50), pygame.SRCALPHA)
    boton_volver["superficie"].fill((0, 120, 255))
    pygame.draw.rect(boton_volver["superficie"], (255,255,255), (0,0,160,50), 3, border_radius=15)
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"].topleft)
    mostrar_texto(pantalla, "VOLVER", (boton_volver["rectangulo"].x + 30, boton_volver["rectangulo"].y + 10), fuente_boton, COLOR_BLANCO)

    # --- EVENTOS ---
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma["rectangulo"].collidepoint(evento.pos):
                if datos_juego["volumen_musica"] < 100:
                    datos_juego["volumen_musica"] += 5
                if not click_muteado:
                    CLICK_SONIDO.play()
            elif boton_resta["rectangulo"].collidepoint(evento.pos):
                if datos_juego["volumen_musica"] > 0:
                    datos_juego["volumen_musica"] -= 5
                if not click_muteado:
                    CLICK_SONIDO.play()
            elif boton_volver["rectangulo"].collidepoint(evento.pos):
                if not click_muteado:
                    CLICK_SONIDO.play()
                retorno = "menu"
            elif boton_musica["rectangulo"].collidepoint(evento.pos):
                datos_juego["musica_activada"] = not datos_juego["musica_activada"]
                if not click_muteado:
                    CLICK_SONIDO.play()
            elif boton_click.collidepoint(evento.pos):
                click_muteado = not click_muteado
                # Opcional: CLICK_SONIDO.play() solo si lo activas

    return retorno