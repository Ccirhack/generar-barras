"""Genera la imagen del codigo de barras (Code128) a partir de un DNI."""

import os
import tempfile

import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageChops

OPCIONES_BARRAS = {
    "module_width": 0.6,
    "module_height": 36.0,
    "quiet_zone": 2.0,
    "font_size": 26,
    "text_distance": 10.0,  # mas separacion = el numero de DNI queda mas abajo
    "dpi": 300,
    "write_text": True,
}


def generar_imagen_codigo_barras(dni):
    """Devuelve una imagen RGBA con el codigo de barras recortado al contenido real."""
    dni = str(dni)
    codigo = barcode.get("code128", dni, writer=ImageWriter())
    with tempfile.TemporaryDirectory() as tmp_dir:
        ruta_base = os.path.join(tmp_dir, "barras_tmp")
        ruta = codigo.save(ruta_base, options=OPCIONES_BARRAS)
        with Image.open(ruta) as img:
            img = img.convert("RGB")

    # python-barcode deja un margen inferior en blanco mas grande que el
    # superior; se recorta al contenido real (barras + numero) para que no
    # quede una franja blanca vacia debajo del DNI.
    fondo = Image.new("RGB", img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, fondo).getbbox()
    if bbox:
        margen = 10
        bbox = (
            max(bbox[0] - margen, 0),
            max(bbox[1] - margen, 0),
            min(bbox[2] + margen, img.width),
            min(bbox[3] + margen, img.height),
        )
        img = img.crop(bbox)

    return img.convert("RGBA")
