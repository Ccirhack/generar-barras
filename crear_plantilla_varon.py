"""
Dibuja "plantilla_varon.png": una plantilla de credencial para varones con
el mismo tamaño (1200x1909) y la misma distribucion que "plantilla.png"
(circulo del logo arriba al centro, espacio libre abajo para el codigo de
barras), pero con estilo sobrio: azul marino, gris acero y detalles dorados,
formas geometricas en lugar de hojas y flores.

Uso:
    python crear_plantilla_varon.py
"""

import math
import os

from PIL import Image, ImageDraw

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_SALIDA = os.path.join(DIRECTORIO_BASE, "plantilla_varon.png")

ANCHO, ALTO = 1200, 1909
SS = 2  # se dibuja al doble y se reduce, para bordes suaves

# Paleta
AZUL_MARINO = (22, 38, 66)
AZUL_ACERO = (52, 88, 130)
GRIS_FONDO = (214, 222, 232)
GRIS_OSCURO = (170, 184, 202)
DORADO = (206, 158, 64)
BLANCO = (255, 255, 255)

# Circulo del logo (mismo que en generar_credencial.py)
CENTRO_CIRCULO = (600, 794)
RADIO_ARO = 352  # aro blanco; el logo ocupa radio 330 por dentro


def s(valor):
    """Escala coordenadas al lienzo sobremuestreado."""
    if isinstance(valor, (tuple, list)):
        return type(valor)(s(v) for v in valor)
    return valor * SS


def hexagono(cx, cy, r, rot=0):
    return [
        (cx + r * math.cos(math.radians(60 * i + rot)),
         cy + r * math.sin(math.radians(60 * i + rot)))
        for i in range(6)
    ]


def crear_plantilla(ruta_salida=RUTA_SALIDA):
    img = Image.new("RGB", (ANCHO * SS, ALTO * SS), GRIS_FONDO)
    d = ImageDraw.Draw(img)

    # --- Encabezado azul marino con borde inferior en diagonal ----------
    d.polygon(s([(0, 0), (ANCHO, 0), (ANCHO, 560), (0, 700)]), fill=AZUL_MARINO)
    # franja dorada que acompaña la diagonal
    d.polygon(s([(0, 700), (ANCHO, 560), (ANCHO, 584), (0, 724)]), fill=DORADO)
    # franja azul acero debajo de la dorada
    d.polygon(s([(0, 724), (ANCHO, 584), (ANCHO, 604), (0, 744)]), fill=AZUL_ACERO)

    # --- Lineas diagonales finas en la esquina superior izquierda --------
    for i in range(7):
        off = i * 38
        d.line(s([(0, 330 - off), (330 - off, 0)]), fill=AZUL_ACERO, width=s(6))
    d.line(s([(0, 380), (380, 0)]), fill=DORADO, width=s(8))

    # --- Emblema en el encabezado (hexagono blanco con centro dorado) ----
    cx, cy = 600, 180
    d.polygon(s(hexagono(cx, cy, 62, 30)), outline=BLANCO, width=s(9))
    d.polygon(s(hexagono(cx, cy, 34, 30)), fill=DORADO)

    # --- Hexagonos decorativos a la derecha ------------------------------
    for (hx, hy, hr, color, ancho) in [
        (1110, 300, 70, AZUL_ACERO, 6),
        (1165, 420, 45, DORADO, 5),
        (1090, 470, 30, AZUL_ACERO, 4),
        (1150, 900, 60, AZUL_ACERO, 6),
        (1110, 1030, 38, DORADO, 5),
        (1170, 1120, 28, AZUL_ACERO, 4),
    ]:
        d.polygon(s(hexagono(hx, hy, hr, 30)), outline=color, width=s(ancho))

    # --- Hexagonos decorativos a la izquierda (zona media) ---------------
    for (hx, hy, hr, color, ancho) in [
        (70, 900, 55, AZUL_ACERO, 6),
        (40, 1020, 32, DORADO, 5),
    ]:
        d.polygon(s(hexagono(hx, hy, hr, 30)), outline=color, width=s(ancho))

    # --- Esquina inferior izquierda: bloques en diagonal -----------------
    # (siguen por debajo del codigo de barras, que las tapa)
    d.polygon(s([(0, 1300), (609, ALTO), (0, ALTO)]), fill=GRIS_OSCURO)
    d.polygon(s([(0, 1520), (389, ALTO), (0, ALTO)]), fill=AZUL_ACERO)
    d.line(s([(0, 1460), (449, ALTO)]), fill=DORADO, width=s(8))

    # --- Esquina inferior derecha: triangulo marino + reticula de puntos -
    d.polygon(s([(ANCHO, 1500), (ANCHO, ALTO), (791, ALTO)]), fill=AZUL_MARINO)
    d.line(s([(ANCHO, 1465), (756, ALTO)]), fill=DORADO, width=s(8))
    for fila in range(4):
        for col in range(4):
            px = 1005 + col * 50
            py = 1230 + fila * 50
            d.ellipse(s([(px - 8, py - 8), (px + 8, py + 8)]), fill=AZUL_ACERO)

    # --- Aro blanco del circulo del logo ---------------------------------
    cx, cy = CENTRO_CIRCULO
    d.ellipse(s([(cx - RADIO_ARO, cy - RADIO_ARO), (cx + RADIO_ARO, cy + RADIO_ARO)]), fill=BLANCO)
    d.ellipse(s([(cx - 330, cy - 330), (cx + 330, cy + 330)]), fill=AZUL_ACERO)

    img = img.resize((ANCHO, ALTO), Image.LANCZOS)
    img.save(ruta_salida)
    print(f"Plantilla generada: {ruta_salida}")
    return ruta_salida


if __name__ == "__main__":
    crear_plantilla()
