"""
Generador de credenciales a partir de la plantilla "plantilla.png".

Toma la plantilla (fondo, hoja, circulo, decoracion ya diseñados), quita
el texto de marca ("LUXE A STUDIO") y el nombre/cargo/ID de ejemplo,
pone el logo (peach-svgrepo-com.svg) dentro del circulo y pega un
codigo de barras real -bien grande, ocupando el espacio inferior- generado
a partir del DNI.

Hay dos plantillas: "mujer" (plantilla.png, la original) y "varon"
(plantilla_varon.png, creada con crear_plantilla_varon.py). Se elige con
--tipo; si no se indica se usa TIPO_POR_DEFECTO.

Uso por terminal (el DNI va despues del nombre del script):
    python generar_credencial.py 70892343
    python generar_credencial.py 70892343 --tipo varon
    python generar_credencial.py 70892343 --logo mi_logo.svg --salida mi_credencial.png

Uso sin terminal: cambia el valor de DNI_POR_DEFECTO aqui abajo y corre el
archivo (por ejemplo con el boton "Run" de tu editor, o "python generar_credencial.py"
sin nada mas). Si en cambio SI escribis un DNI por terminal, ese es el que se usa.
"""

import argparse
import os
import tempfile

import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageChops, ImageDraw
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

# ---------------------------------------------------------------------------
# <<< EDITA ESTA LINEA con el DNI que quieras si corres el script sin
# argumentos por terminal >>>
# python generar_credencial.py 73700356
#python generar_credencial.py 73700356 --tipo varon
# ---------------------------------------------------------------------------
DNI_POR_DEFECTO = "70892343"
TIPO_POR_DEFECTO = "mujer"  # "mujer" o "varon"

# ---------------------------------------------------------------------------
# Plantilla y coordenadas (medidas sobre plantilla.png, 1200x1909)
# ---------------------------------------------------------------------------

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_PLANTILLA = os.path.join(DIRECTORIO_BASE, "plantilla.png")
RUTA_LOGO_SVG = os.path.join(DIRECTORIO_BASE, "peach-svgrepo-com.svg")
RUTA_PLANTILLA_VARON = os.path.join(DIRECTORIO_BASE, "plantilla_varon.png")
RUTA_LOGO_SVG_VARON = os.path.join(DIRECTORIO_BASE, "escudo-varon.svg")

# Circulo donde va el logo (bbox cuadrado que encierra el circulo interior)
CIRCULO_BBOX = (270, 464, 930, 1124)
FONDO_CIRCULO = (216, 154, 91)  # tono tostado a juego con la plantilla
FONDO_CIRCULO_VARON = (52, 88, 130)  # azul acero de plantilla_varon.png

COLOR_FONDO_PEACH = (238, 185, 148)  # durazno de fondo de la plantilla
COLOR_FONDO_OLIVA = (97, 78, 28)     # verde oliva del encabezado

# Texto "LUXE A STUDIO" bajo el logo del encabezado -> se borra
ZONA_MARCA = (380, 268, 820, 315)

# Nombre/cargo/ID de ejemplo entre el circulo y el codigo de barras -> se
# borran. Dos rectangulos porque la hoja decorativa de la izquierda llega
# mas a la derecha en la fila de abajo (hasta x~185) que en la de arriba
# (hasta x~109, donde empieza el nombre en x=185).
ZONA_NOMBRE = (120, 1150, 1150, 1345)
ZONA_SUBCARGO_ID = (200, 1345, 1150, 1520)

# Zona donde va el codigo de barras: bien grande, con permiso a
# "desbordar" un poco sobre el fondo durazno (sin tocar la hoja
# decorativa de la izquierda ni el circulo con lunares de la esquina
# inferior derecha).
CAJA_BARRAS = (205, 1150, 955, 1900)
DESBORDE_BARRAS = 1.02  # >1.0 = el codigo de barras sobresale un poco de la caja


# ---------------------------------------------------------------------------
# Logo (SVG) dentro del circulo
# ---------------------------------------------------------------------------

def generar_imagen_logo(diametro, ruta_svg=RUTA_LOGO_SVG, fondo_circulo=FONDO_CIRCULO):
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


# ---------------------------------------------------------------------------
# Codigo de barras
# ---------------------------------------------------------------------------

def generar_imagen_codigo_barras(dni):
    dni = str(dni)
    codigo = barcode.get("code128", dni, writer=ImageWriter())
    with tempfile.TemporaryDirectory() as tmp_dir:
        ruta_base = os.path.join(tmp_dir, "barras_tmp")
        opciones = {
            "module_width": 0.6,
            "module_height": 36.0,
            "quiet_zone": 2.0,
            "font_size": 26,
            "text_distance": 10.0,  # mas separacion = el numero de DNI queda mas abajo
            "dpi": 300,
            "write_text": True,
        }
        ruta = codigo.save(ruta_base, options=opciones)
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


# ---------------------------------------------------------------------------
# Generacion de la credencial completa a partir de la plantilla
# ---------------------------------------------------------------------------

def generar_credencial(dni, ruta_logo=None, archivo_salida="credencial.png", tipo="mujer"):
    if tipo == "varon":
        # plantilla_varon.png ya viene limpia (sin texto de ejemplo); si no
        # existe se dibuja en el momento.
        if not os.path.exists(RUTA_PLANTILLA_VARON):
            from crear_plantilla_varon import crear_plantilla
            crear_plantilla(RUTA_PLANTILLA_VARON)
        tarjeta = Image.open(RUTA_PLANTILLA_VARON).convert("RGBA")
        ruta_logo = ruta_logo or RUTA_LOGO_SVG_VARON
        fondo_circulo = FONDO_CIRCULO_VARON
    else:
        tarjeta = Image.open(RUTA_PLANTILLA).convert("RGBA")
        ruta_logo = ruta_logo or RUTA_LOGO_SVG
        fondo_circulo = FONDO_CIRCULO
    draw = ImageDraw.Draw(tarjeta)

    # 1) Quitar el texto de marca "LUXE A STUDIO" (se deja el logo/hoja)
    if tipo == "mujer":
        draw.rectangle(ZONA_MARCA, fill=COLOR_FONDO_OLIVA)

    # 2) Logo dentro del circulo
    diametro = CIRCULO_BBOX[2] - CIRCULO_BBOX[0]
    logo_img = generar_imagen_logo(diametro, ruta_logo, fondo_circulo)
    tarjeta.paste(logo_img, (CIRCULO_BBOX[0], CIRCULO_BBOX[1]), logo_img)

    # 3) Quitar nombre/cargo/ID de ejemplo
    if tipo == "mujer":
        draw.rectangle(ZONA_NOMBRE, fill=COLOR_FONDO_PEACH)
        draw.rectangle(ZONA_SUBCARGO_ID, fill=COLOR_FONDO_PEACH)

    # 4) Codigo de barras grande, ocupando (y desbordando un poco) el
    #    espacio inferior de la credencial
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

    tarjeta.convert("RGB").save(archivo_salida)
    print(f"Credencial generada: {os.path.abspath(archivo_salida)}")
    return archivo_salida


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Genera una credencial a partir de plantilla.png con logo y codigo de barras.")
    parser.add_argument("dni", nargs="?", default=DNI_POR_DEFECTO,
                         help="DNI o codigo a codificar (si no se pasa, usa DNI_POR_DEFECTO del script)")
    parser.add_argument("--tipo", choices=["mujer", "varon"], default=TIPO_POR_DEFECTO,
                         help="Plantilla a usar: mujer (plantilla.png) o varon (plantilla_varon.png)")
    parser.add_argument("--logo", default=None,
                         help="Ruta a un SVG para el circulo (por defecto peach-svgrepo-com.svg para mujer, escudo-varon.svg para varon)")
    parser.add_argument("--salida", default=None,
                         help="Nombre del archivo de salida (por defecto credencial_<DNI>.png)")
    args = parser.parse_args()

    salida = args.salida or f"credencial_{args.dni}.png"
    generar_credencial(args.dni, args.logo, salida, args.tipo)


if __name__ == "__main__":
    main()
