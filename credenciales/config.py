"""Rutas, colores y coordenadas compartidas por el resto del paquete.

Todas las coordenadas estan medidas sobre assets/plantilla.png (1200x1909 px);
assets/plantilla_varon.png se diseno con las mismas medidas para que coincidan.
"""

import os

DIRECTORIO_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTORIO_ASSETS = os.path.join(DIRECTORIO_BASE, "assets")

RUTA_PLANTILLA = os.path.join(DIRECTORIO_ASSETS, "plantilla.png")
RUTA_PLANTILLA_VARON = os.path.join(DIRECTORIO_ASSETS, "plantilla_varon.png")
RUTA_LOGO_SVG = os.path.join(DIRECTORIO_ASSETS, "peach-svgrepo-com.svg")
RUTA_LOGO_SVG_VARON = os.path.join(DIRECTORIO_ASSETS, "escudo-varon.svg")

DNI_POR_DEFECTO = "70892343"
TIPO_POR_DEFECTO = "mujer"  # "mujer" o "varon"

# Circulo donde va el logo (bbox cuadrado que encierra el circulo interior)
CIRCULO_BBOX = (270, 464, 930, 1124)
FONDO_CIRCULO = (216, 154, 91)  # tono tostado a juego con plantilla.png
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
