import pygame
import csv
import random
from BaseV2 import *
from Funciones import *

# --- VARIABLES GLOBALES Y CONFIGURACIÓN ---
racha_correctas = 0
comodines = {"bomba": True, "x2": True, "doble_chance": True, "pasar": True}
bomba_oculta = []
x2_activado = False
doble_chance_activado = False
ya_usó_doble_chance = False

# Carga imágenes de comodines
imagen_bomba = pygame.image.load("bomba.png")
imagen_x2 = pygame.image.load("x2.png")
imagen_doble = pygame.image.load("doble_chance.png")
imagen_pasar = pygame.image.load("pasar.png")
imagenes_comodines = {
    "bomba": imagen_bomba,
    "x2": imagen_x2,
    "doble_chance": imagen_doble,
    "pasar": imagen_pasar
}

# Definir tamaños
TAMAÑO_PREGUNTA = (800, 100)
TAMAÑO_RESPUESTA = (700, 60)

# Fondo (NO escalar aquí)
imagen_fondo = pygame.image.load("ImagenRespu.png")

# --- FUNCIONES AUXILIARES ---
def cargar_preguntas_csv(ruta_csv):
    """
    Carga preguntas desde un archivo CSV sin usar csv.DictReader.

    Args:
        ruta_csv (str): Ruta al archivo CSV.

    Returns:
        list: Lista de diccionarios con las preguntas.
    """
    preguntas = []
    with open(ruta_csv, encoding='utf-8') as f:
        lineas = f.readlines()
        encabezado = [col.strip() for col in lineas[0].strip().split(",")]
        for i, linea in enumerate(lineas[1:]):
            partes = [col.strip() for col in linea.strip().split(",")]
            if len(partes) == 6:
                try:
                    preguntas.append({
                        "pregunta": partes[0],
                        "respuesta_1": partes[1],
                        "respuesta_2": partes[2],
                        "respuesta_3": partes[3],
                        "respuesta_4": partes[4],
                        "respuesta_correcta": int(partes[5])
                    })
                except Exception as e:
                    print(f"❌ Error en la fila {i + 2}: {e}")
                    print(f"Contenido problemático: {partes}")
            else:
                print(f"❌ Formato incorrecto en la fila {i + 2}: {linea.strip()}")
    return preguntas

def mezclar_lista(lista):
    random.shuffle(lista)
    return lista

# --- INICIALIZACIÓN ---
Preguntas = cargar_preguntas_csv('Preguntas.csv')
lista_preguntas = Preguntas.copy()
mezclar_lista(lista_preguntas)
indice = 0
bandera_respuesta = False
bandera_mostrar = True

TIEMPO_PREGUNTA = 25
tiempo_restante = TIEMPO_PREGUNTA
ultimo_tick = pygame.time.get_ticks()
tiempo_feedback = 0

pygame.init()
COLOR_AZUL = (0, 120, 255)
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)

# --- CREAR SUPERFICIES PARA PREGUNTA Y RESPUESTAS ---
cartas_respuestas = []
for i in range(4):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = pygame.Surface(TAMAÑO_RESPUESTA)
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)

fuente_pregunta = pygame.font.SysFont("Arial Narrow", 30)
fuente_respuesta = pygame.font.SysFont("Arial Narrow", 23)
fuente_texto = pygame.font.SysFont("Arial Narrow", 25)

# --- FUNCIÓN PRINCIPAL DEL JUEGO ---
def mostrar_juego(pantalla, cola_eventos, datos_juego):
    """
    Renderiza y gestiona la lógica principal del juego de preguntas.

    Args:
        pantalla (pygame.Surface): Superficie principal donde se dibuja el juego.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de pygame.
        datos_juego (dict): Estado actual del jugador (vidas, puntuación, etc.).

    Returns:
        str: Estado siguiente del flujo del juego ("juego", "terminado", "salir", etc.).
    """
    global indice, bandera_respuesta, bandera_mostrar, tiempo_restante, ultimo_tick
    global racha_correctas, bomba_oculta, x2_activado, doble_chance_activado, ya_usó_doble_chance
    global tiempo_feedback, comodines
    retorno = "juego"
    ahora = pygame.time.get_ticks()

    # Fondo escalado
    fondo_escalado = pygame.transform.scale(imagen_fondo, (pantalla.get_width(), pantalla.get_height()))
    pantalla.blit(fondo_escalado, (0, 0))

    # Actualizar tiempo por pregunta
    if tiempo_feedback == 0:
        if ahora - ultimo_tick >= 1000:
            tiempo_restante -= 1
            ultimo_tick = ahora
            if tiempo_restante <= 0:
                ERROR_SONIDO.play()
                datos_juego["vidas"] -= 1
                datos_juego["puntuacion"] -= 2
                if datos_juego["vidas"] < 0:
                    datos_juego["vidas"] = 0
                racha_correctas = 0
                bandera_respuesta = True
                bandera_mostrar = True
                tiempo_feedback = ahora

    # Pregunta
    TAM_CUADRO = (800, 100)
    POS_CUADRO = ((pantalla.get_width() - TAM_CUADRO[0]) // 2, 60)
    cuadro_pregunta = pygame.Surface(TAM_CUADRO)
    cuadro_pregunta.fill((0, 102, 204))
    pregunta_actual = lista_preguntas[indice]
    texto_pregunta = fuente_pregunta.render(pregunta_actual["pregunta"], True, COLOR_BLANCO)
    rect_texto = texto_pregunta.get_rect(center=(TAM_CUADRO[0]//2, TAM_CUADRO[1]//2))
    cuadro_pregunta.blit(texto_pregunta, rect_texto)
    pantalla.blit(cuadro_pregunta, POS_CUADRO)

    # Respuestas
    for i in range(4):
        x = (pantalla.get_width() - TAMAÑO_RESPUESTA[0]) // 2
        y = POS_CUADRO[1] + TAM_CUADRO[1] + 30 + i*70
        cuadro_respuesta = pygame.Surface(TAMAÑO_RESPUESTA)
        cuadro_respuesta.fill((0, 0, 0))
        if tiempo_feedback > 0 and bandera_respuesta:
            pixel = cartas_respuestas[i]['superficie'].get_at((0,0))
            color_overlay = None
            if pixel[:3] == (0, 200, 0):
                color_overlay = (0, 200, 0, 120)
            elif pixel[:3] == (200, 0, 0):
                color_overlay = (200, 0, 0, 120)
            if color_overlay:
                overlay = pygame.Surface(TAMAÑO_RESPUESTA, pygame.SRCALPHA)
                overlay.fill(color_overlay)
                cuadro_respuesta.blit(overlay, (0, 0))
        if (i+1) in bomba_oculta:
            mostrar_texto(cuadro_respuesta, " ", (20, 20), fuente_respuesta, COLOR_BLANCO)
        else:
            mostrar_texto(cuadro_respuesta, pregunta_actual[f"respuesta_{i+1}"], (20, 20), fuente_respuesta, COLOR_BLANCO)
        cartas_respuestas[i]['superficie'] = cuadro_respuesta
        cartas_respuestas[i]['rectangulo'] = pantalla.blit(cuadro_respuesta, (x, y))

    # Comodines
    fuente_comodin = pygame.font.SysFont("Arial Narrow", 21)
    nombres_comodines = ["bomba", "x2", "doble_chance", "pasar"]
    botones_comodines = []
    for idx, nombre in enumerate(nombres_comodines):
        color = (0, 200, 0) if comodines[nombre] else (150, 150, 150)
        boton = pygame.Surface((120, 40))
        boton.fill(color)
        imagen = pygame.transform.scale(imagenes_comodines[nombre], (32, 32))
        boton.blit(imagen, (5, 4))
        mostrar_texto(boton, nombre.upper(), (45, 8), fuente_comodin, (255,255,255))
        x_boton = pantalla.get_width() - 150
        y_boton = pantalla.get_height() - 220 + idx*50
        rect = boton.get_rect(topleft=(x_boton, y_boton))
        pantalla.blit(boton, rect.topleft)
        botones_comodines.append((rect, nombre))

    # Info de juego
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 10), fuente_texto, COLOR_NEGRO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 40), fuente_texto, COLOR_NEGRO)
    mostrar_texto(pantalla, f"TIEMPO: {tiempo_restante}", (10, 70), fuente_texto, (200,0,0))

    # Feedback visual/sonoro antes de avanzar
    if tiempo_feedback > 0:
        pygame.display.flip()
        if ahora - tiempo_feedback > 700:
            indice += 1
            if indice >= len(lista_preguntas):
                indice = 0
                mezclar_lista(lista_preguntas)
            bandera_respuesta = False
            bandera_mostrar = True
            tiempo_restante = TIEMPO_PREGUNTA
            bomba_oculta.clear()
            doble_chance_activado = False
            ya_usó_doble_chance = False
            tiempo_feedback = 0
            if datos_juego["vidas"] <= 0:
                return "terminado"
        else:
            return retorno

    # Procesar eventos SOLO si no se está mostrando feedback
    if tiempo_feedback == 0:
        for evento in cola_eventos:
            if evento.type == pygame.QUIT:
                retorno = "salir"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Comodines
                for rect, nombre in botones_comodines:
                    if rect.collidepoint(evento.pos) and comodines[nombre]:
                        comodines[nombre] = False
                        if nombre == "bomba":
                            bomba_oculta.clear()
                            correct = pregunta_actual["respuesta_correcta"]
                            opciones = [1,2,3,4]
                            opciones.remove(correct)
                            bomba_oculta = random.sample(opciones, 2)
                        elif nombre == "x2":
                            x2_activado = True
                        elif nombre == "doble_chance":
                            doble_chance_activado = True
                            ya_usó_doble_chance = False
                        elif nombre == "pasar":
                            indice += 1
                            if indice >= len(lista_preguntas):
                                indice = 0
                                mezclar_lista(lista_preguntas)
                            bandera_mostrar = True
                            tiempo_restante = TIEMPO_PREGUNTA
                            bomba_oculta.clear()
                        break
                # Respuestas
                for i in range(4):
                    if cartas_respuestas[i]['rectangulo'].collidepoint(evento.pos):
                        respuesta_usuario = i + 1
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta_usuario):
                            CLICK_SONIDO.play()
                            cartas_respuestas[i]['superficie'].fill((0, 200, 0))
                            datos_juego["puntuacion"] += 5 if not x2_activado else 10
                            if x2_activado:
                                x2_activado = False
                            racha_correctas += 1
                            if racha_correctas == 5:
                                datos_juego["vidas"] += 1
                                racha_correctas = 0
                            bandera_respuesta = True
                            bandera_mostrar = True
                            tiempo_feedback = ahora
                        else:
                            # --- DOBLE CHANCE ---
                            if doble_chance_activado and not ya_usó_doble_chance:
                                ya_usó_doble_chance = True
                                ERROR_SONIDO.play()
                                cartas_respuestas[i]['superficie'].fill((200, 0, 0))
                                # No se pierde vida ni termina la pregunta, solo se desactiva el doble chance
                                break
                            else:
                                ERROR_SONIDO.play()
                                cartas_respuestas[i]['superficie'].fill((200, 0, 0))
                                racha_correctas = 0
                                bandera_respuesta = True
                                bandera_mostrar = True
                                tiempo_feedback = ahora
                        break
    return retorno

def reiniciar_juego():
    """
    Reinicia todas las variables globales y el estado del juego para una nueva partida.
    """
    global comodines, racha_correctas, bomba_oculta, x2_activado, doble_chance_activado, ya_usó_doble_chance
    global lista_preguntas, indice, bandera_respuesta, bandera_mostrar, tiempo_restante, tiempo_feedback
    comodines = {"bomba": True, "x2": True, "doble_chance": True, "pasar": True}
    racha_correctas = 0
    bomba_oculta = []
    x2_activado = False
    doble_chance_activado = False
    ya_usó_doble_chance = False
    lista_preguntas = Preguntas.copy()
    mezclar_lista(lista_preguntas)
    indice = 0
    bandera_respuesta = False
    bandera_mostrar = True
    tiempo_restante = TIEMPO_PREGUNTA
    tiempo_feedback = 0

# --- PANTALLA DE CONFIGURACIÓN (opcional) ---
def pantalla_configuracion(pantalla):
    """
    Muestra la pantalla de configuración básica y espera la acción del usuario.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja la configuración.
    """
    pantalla.fill((200, 200, 255))
    fuente = pygame.font.SysFont("Arial", 50)
    texto = fuente.render("Configuración", True, (0, 0, 0))
    pantalla.blit(texto, (pantalla.get_width()//2 - 170, 100))
    fuente2 = pygame.font.SysFont("Arial", 30)
    texto2 = fuente2.render("Presiona ESC para volver al menú", True, (0, 0, 100))
    pantalla.blit(texto2, (pantalla.get_width()//2 - 220, 300))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                esperando = False

# --- PANTALLA FINAL (opcional, modular) ---
def pantalla_final(pantalla, datos_juego):
    """
    Muestra la pantalla final para ingresar el nombre del jugador y visualizar el puntaje.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja la pantalla final.
        datos_juego (dict): Estado final del jugador (incluye puntuación y nombre).
    """
    fondo_escalado = pygame.transform.scale(imagen_fondo, (pantalla.get_width(), pantalla.get_height()))
    pantalla.blit(fondo_escalado, (0, 0))
    overlay = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))
    pantalla.blit(overlay, (0, 0))
    mi_imagen = pygame.image.load("Imagenfondofinal.jpg")
    pantalla.blit(mi_imagen, (pantalla.get_width()//2 - mi_imagen.get_width()//2, 60))

    fuente_grande = pygame.font.SysFont("Arial Black", 60)
    fuente_mediana = pygame.font.SysFont("Arial", 35)
    fuente_input = pygame.font.SysFont("Arial", 40)

    box_width, box_height = 500, 350
    box_x = pantalla.get_width() // 2 - box_width // 2
    box_y = pantalla.get_height() // 2 - box_height // 2
    caja = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    caja.fill((240, 240, 255, 230))
    pygame.draw.rect(caja, (120, 120, 200), caja.get_rect(), 4, border_radius=18)
    pantalla.blit(caja, (box_x, box_y))

    texto = fuente_grande.render("¡Juego Terminado!", True, (80, 0, 120))
    rect = texto.get_rect(center=(pantalla.get_width()//2, box_y + 60))
    puntaje = fuente_mediana.render(f"Puntuación: {datos_juego['puntuacion']}", True, (30, 30, 30))
    instrucciones = fuente_mediana.render("Escribe tu nombre y presiona ENTER", True, (60, 60, 120))

    input_box = pygame.Rect(pantalla.get_width()//2 - 180, box_y + 170, 360, 55)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    active = True
    nombre = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        datos_juego["nombre"] = nombre
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    elif len(nombre) < 20 and event.unicode.isprintable():
                        nombre += event.unicode

        pantalla.blit(fondo_escalado, (0, 0))
        pantalla.blit(overlay, (0, 0))
        pantalla.blit(caja, (box_x, box_y))
        pantalla.blit(texto, rect)
        pantalla.blit(puntaje, (pantalla.get_width()//2 - 120, box_y + 110))
        pantalla.blit(instrucciones, (pantalla.get_width()//2 - 220, box_y + 140))

        pygame.draw.rect(pantalla, color_active if active else color_inactive, input_box, 3, border_radius=12)
        txt_surface = fuente_input.render(nombre, True, (0, 0, 0))
        pantalla.blit(txt_surface, (input_box.x + 12, input_box.y + 10))

        pygame.display.flip()

# --- MENÚ AGREGAR PREGUNTAS (modular y gráfico) ---
def mostrar_agregar_preguntas(pantalla, datos_juego, eventos):
    """
    Renderiza la interfaz para agregar nuevas preguntas y respuestas al juego.

    Args:
        pantalla (pygame.Surface): Superficie donde se dibuja la interfaz.
        datos_juego (dict): Estado actual del juego (no siempre usado aquí).
        eventos (list[pygame.event.Event]): Lista de eventos de pygame.

    Returns:
        str: Estado siguiente del flujo ("agregar_preguntas", "menu", "salir").
    """
    fuente = pygame.font.SysFont("Arial", 28)
    color_fondo = (230, 230, 255)
    color_input = (255, 255, 255)
    color_borde = (0, 120, 255)
    color_texto = (0, 0, 0)
    color_boton = (0, 180, 100)
    color_boton_hover = (0, 220, 140)

    # Mantener el estado de los campos entre llamadas
    if not hasattr(mostrar_agregar_preguntas, "campos"):
        mostrar_agregar_preguntas.campos = [
            {"label": "Pregunta:", "texto": "", "rect": pygame.Rect(200, 80, 1000, 40)},
            {"label": "Respuesta 1:", "texto": "", "rect": pygame.Rect(200, 150, 1000, 40)},
            {"label": "Respuesta 2:", "texto": "", "rect": pygame.Rect(200, 210, 1000, 40)},
            {"label": "Respuesta 3:", "texto": "", "rect": pygame.Rect(200, 270, 1000, 40)},
            {"label": "Respuesta 4:", "texto": "", "rect": pygame.Rect(200, 330, 1000, 40)},
        ]
    if not hasattr(mostrar_agregar_preguntas, "campo_activo"):
        mostrar_agregar_preguntas.campo_activo = 0
    if not hasattr(mostrar_agregar_preguntas, "respuesta_correcta"):
        mostrar_agregar_preguntas.respuesta_correcta = 0
    if not hasattr(mostrar_agregar_preguntas, "mensaje"):
        mostrar_agregar_preguntas.mensaje = ""

    campos = mostrar_agregar_preguntas.campos
    campo_activo = mostrar_agregar_preguntas.campo_activo
    respuesta_correcta = mostrar_agregar_preguntas.respuesta_correcta
    mensaje = mostrar_agregar_preguntas.mensaje

    boton_guardar = pygame.Rect(600, 420, 200, 50)

    pantalla.fill(color_fondo)
    instrucciones = fuente.render("Completa los campos, selecciona la respuesta correcta y haz clic en Guardar.", True, color_texto)
    pantalla.blit(instrucciones, (200, 30))

    for i, campo in enumerate(campos):
        pygame.draw.rect(pantalla, color_input, campo["rect"], border_radius=8)
        pygame.draw.rect(pantalla, color_borde if i == campo_activo else (180,180,180), campo["rect"], 2, border_radius=8)
        label = fuente.render(campo["label"], True, color_texto)
        pantalla.blit(label, (campo["rect"].x - 170, campo["rect"].y + 5))
        texto = fuente.render(campo["texto"], True, color_texto)
        pantalla.blit(texto, (campo["rect"].x + 10, campo["rect"].y + 5))

    fuente_resp = pygame.font.SysFont("Arial", 22)
    for i in range(4):
        radio = 12
        x = 1230
        y = 165 + i * 60
        color_circulo = (0, 180, 100) if respuesta_correcta == i else (180,180,180)
        pygame.draw.circle(pantalla, color_circulo, (x, y), radio)
        if respuesta_correcta == i:
            pygame.draw.circle(pantalla, (0, 80, 0), (x, y), 6)
        txt = fuente_resp.render(f"Correcta", True, color_texto)
        pantalla.blit(txt, (x + 20, y - 12))

    mouse_pos = pygame.mouse.get_pos()
    color_btn = color_boton_hover if boton_guardar.collidepoint(mouse_pos) else color_boton
    pygame.draw.rect(pantalla, color_btn, boton_guardar, border_radius=10)
    txt_guardar = fuente.render("GUARDAR", True, (255,255,255))
    pantalla.blit(txt_guardar, txt_guardar.get_rect(center=boton_guardar.center))

    if mensaje:
        fuente_msg = pygame.font.SysFont("Arial", 24)
        color_msg = (0,180,0) if "guardada" in mensaje else (200,0,0)
        pantalla.blit(fuente_msg.render(mensaje, True, color_msg), (200, 500))

    pygame.display.flip()

    for event in eventos:
        if event.type == pygame.QUIT:
            return "salir"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mostrar_agregar_preguntas.campo_activo = 0
                mostrar_agregar_preguntas.respuesta_correcta = 0
                mostrar_agregar_preguntas.mensaje = ""
                for c in campos:
                    c["texto"] = ""
                return "menu"
            elif event.key == pygame.K_TAB or event.key == pygame.K_RETURN:
                campo_activo = (campo_activo + 1) % len(campos)
            elif event.key == pygame.K_BACKSPACE:
                campos[campo_activo]["texto"] = campos[campo_activo]["texto"][:-1]
            else:
                if len(campos[campo_activo]["texto"]) < 120 and event.unicode.isprintable():
                    campos[campo_activo]["texto"] += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, campo in enumerate(campos):
                if campo["rect"].collidepoint(event.pos):
                    campo_activo = i
            for i in range(4):
                radio = 12
                x = 1230
                y = 165 + i * 60
                if (event.pos[0] - x)**2 + (event.pos[1] - y)**2 <= radio**2:
                    respuesta_correcta = i
            if boton_guardar.collidepoint(event.pos):
                textos = [c["texto"].strip() for c in campos]
                if all(textos) and 0 <= respuesta_correcta < 4:
                    try:
                        with open('Preguntas.csv', 'a', encoding='utf-8', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([textos[0], textos[1], textos[2], textos[3], textos[4], respuesta_correcta+1])
                        mensaje = "Pregunta guardada correctamente."
                        for c in campos:
                            c["texto"] = ""
                    except Exception as e:
                        mensaje = f"Error al guardar: {e}"
                else:
                    mensaje = "Completa todos los campos y selecciona la respuesta correcta."
        mostrar_agregar_preguntas.campos = campos
        mostrar_agregar_preguntas.campo_activo = campo_activo
        mostrar_agregar_preguntas.respuesta_correcta = respuesta_correcta
        mostrar_agregar_preguntas.mensaje = mensaje

    return "agregar_preguntas"