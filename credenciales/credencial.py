"""Compone la credencial final: plantilla + logo + codigo de barras."""

import os

from PIL import Image, ImageDraw

from .codigo_barras import generar_imagen_codigo_barras
from .config import (
    CAJA_BARRAS,
    CIRCULO_BBOX,
    COLOR_FONDO_OLIVA,
    COLOR_FONDO_PEACH,
    DESBORDE_BARRAS,
    FONDO_CIRCULO,
    FONDO_CIRCULO_VARON,
    RUTA_LOGO_SVG,
    RUTA_LOGO_SVG_VARON,
    RUTA_PLANTILLA,
    RUTA_PLANTILLA_VARON,
    ZONA_MARCA,
    ZONA_NOMBRE,
    ZONA_SUBCARGO_ID,
)
from .logo import generar_imagen_logo


def _cargar_tarjeta(tipo, ruta_logo):
    if tipo == "varon":
        # plantilla_varon.png ya viene limpia (sin texto de ejemplo); si no
        # existe se dibuja en el momento.
        if not os.path.exists(RUTA_PLANTILLA_VARON):
            from .plantilla_varon import crear_plantilla
            crear_plantilla(RUTA_PLANTILLA_VARON)
        tarjeta = Image.open(RUTA_PLANTILLA_VARON).convert("RGBA")
        return tarjeta, ruta_logo or RUTA_LOGO_SVG_VARON, FONDO_CIRCULO_VARON

    tarjeta = Image.open(RUTA_PLANTILLA).convert("RGBA")
    return tarjeta, ruta_logo or RUTA_LOGO_SVG, FONDO_CIRCULO


def _pegar_logo(tarjeta, ruta_logo, fondo_circulo):
    diametro = CIRCULO_BBOX[2] - CIRCULO_BBOX[0]
    logo_img = generar_imagen_logo(diametro, ruta_logo, fondo_circulo)
    tarjeta.paste(logo_img, (CIRCULO_BBOX[0], CIRCULO_BBOX[1]), logo_img)


def _pegar_codigo_barras(tarjeta, dni):
    barras_img = generar_imagen_codigo_barras(dni)

    ancho_caja = CAJA_BARRAS[2] - CAJA_BARRAS[0]
    alto_caja = CAJA_BARRAS[3] - CAJA_BARRAS[1]
    escala_ajuste = min(ancho_caja / barras_img.width, alto_caja / barras_img.height)
    escala = escala_ajuste * DESBORDE_BARRAS

    nuevo_ancho = int(barras_img.width * escala)
    nuevo_alto = int(barras_img.height * escala)
    barras_img = barras_img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    centro_x = (CAJA_BARRAS[0] + CAJA_BARRAS[2]) / 2
    centro_y = (CAJA_BARRAS[1] + CAJA_BARRAS[3]) / 2
    x_barras = int(centro_x - nuevo_ancho / 2)
    y_barras = int(centro_y - nuevo_alto / 2)
    tarjeta.paste(barras_img, (x_barras, y_barras), barras_img)


def generar_credencial(dni, ruta_logo=None, archivo_salida="credencial.png", tipo="mujer"):
    """Genera una credencial completa (plantilla + logo + codigo de barras) y la guarda en disco."""
    tarjeta, ruta_logo, fondo_circulo = _cargar_tarjeta(tipo, ruta_logo)
    draw = ImageDraw.Draw(tarjeta)

    # 1) Quitar el texto de marca "LUXE A STUDIO" (se deja el logo/hoja);
    #    la plantilla de varon ya viene sin texto de ejemplo.
    if tipo == "mujer":
        draw.rectangle(ZONA_MARCA, fill=COLOR_FONDO_OLIVA)

    # 2) Logo dentro del circulo
    _pegar_logo(tarjeta, ruta_logo, fondo_circulo)

    # 3) Quitar nombre/cargo/ID de ejemplo
    if tipo == "mujer":
        draw.rectangle(ZONA_NOMBRE, fill=COLOR_FONDO_PEACH)
        draw.rectangle(ZONA_SUBCARGO_ID, fill=COLOR_FONDO_PEACH)

    # 4) Codigo de barras grande, ocupando (y desbordando un poco) el
    #    espacio inferior de la credencial
    _pegar_codigo_barras(tarjeta, dni)

    tarjeta.convert("RGB").save(archivo_salida)
    print(f"Credencial generada: {os.path.abspath(archivo_salida)}")
    return archivo_salida
