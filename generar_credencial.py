#!/usr/bin/env python3
"""Punto de entrada por terminal para generar una credencial.

La logica vive en el paquete credenciales/ (ver README.md para la
estructura completa del proyecto e instrucciones de instalacion).

Uso:
    python generar_credencial.py 70892343
    python generar_credencial.py 70892343 --tipo varon
    python generar_credencial.py 70892343 --logo mi_logo.svg --salida mi_credencial.png

Si corres el script sin argumentos, usa credenciales.config.DNI_POR_DEFECTO.
"""

from credenciales.cli import main

if __name__ == "__main__":
    main()
