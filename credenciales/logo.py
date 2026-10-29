"""Renderiza el logo SVG dentro del circulo de la credencial."""

import os
import tempfile

from PIL import Image, ImageDraw
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from .config import FONDO_CIRCULO, RUTA_LOGO_SVG


def generar_imagen_logo(diametro, ruta_svg=RUTA_LOGO_SVG, fondo_circulo=FONDO_CIRCULO):
    """Devuelve una imagen RGBA circular (diametro x diametro) con el SVG centrado."""
    dibujo = svg2rlg(ruta_svg)
    escala = diametro / max(dibujo.width, dibujo.height)
    dibujo.width *= escala
    dibujo.height *= escala
    dibujo.scale(escala, escala)

    color_fondo = (fondo_circulo[0] << 16) | (fondo_circulo[1] << 8) | fondo_circulo[2]
    with tempfile.TemporaryDirectory() as tmp_dir:
        ruta_png = os.path.join(tmp_dir, "logo.png")
        renderPM.drawToFile(dibujo, ruta_png, fmt="PNG", bg=color_fondo)
        with Image.open(ruta_png) as img:
            logo = img.convert("RGB").copy()

    lienzo = Image.new("RGB", (diametro, diametro), fondo_circulo)
    x = (diametro - logo.width) // 2
    y = (diametro - logo.height) // 2
    lienzo.paste(logo, (x, y))

    mascara = Image.new("L", (diametro, diametro), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, diametro, diametro], fill=255)
    salida = Image.new("RGBA", (diametro, diametro))
    salida.paste(lienzo, (0, 0), mascara)
    return salida
