"""Paquete para generar credenciales con logo circular y codigo de barras.

Expone las dos funciones publicas del proyecto:

    generar_credencial(dni, ruta_logo=None, archivo_salida="credencial.png", tipo="mujer")
    crear_plantilla(ruta_salida=...)  # dibuja assets/plantilla_varon.png desde cero
"""

from .credencial import generar_credencial
from .plantilla_varon import crear_plantilla

__all__ = ["generar_credencial", "crear_plantilla"]
