"""Interfaz de linea de comandos para generar una credencial."""

import argparse

from .config import DNI_POR_DEFECTO, TIPO_POR_DEFECTO
from .credencial import generar_credencial


def main():
    parser = argparse.ArgumentParser(
        description="Genera una credencial a partir de la plantilla con logo y codigo de barras."
    )
    parser.add_argument(
        "dni", nargs="?", default=DNI_POR_DEFECTO,
        help="DNI o codigo a codificar (si no se pasa, usa DNI_POR_DEFECTO del script)",
    )
    parser.add_argument(
        "--tipo", choices=["mujer", "varon"], default=TIPO_POR_DEFECTO,
        help="Plantilla a usar: mujer (plantilla.png) o varon (plantilla_varon.png)",
    )
    parser.add_argument(
        "--logo", default=None,
        help="Ruta a un SVG para el circulo (por defecto peach-svgrepo-com.svg para mujer, escudo-varon.svg para varon)",
    )
    parser.add_argument(
        "--salida", default=None,
        help="Nombre del archivo de salida (por defecto credencial_<DNI>.png)",
    )
    args = parser.parse_args()

    salida = args.salida or f"credencial_{args.dni}.png"
    generar_credencial(args.dni, args.logo, salida, args.tipo)


if __name__ == "__main__":
    main()
