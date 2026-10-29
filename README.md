# Generar Credenciales

Genera credenciales de identificación (imagen PNG) a partir de una plantilla
de diseño, con el logo del emprendimiento dentro del círculo del encabezado
y un código de barras grande (Code128) generado a partir del DNI, listo
para imprimir o escanear.

Hay dos estilos de plantilla disponibles:

- **mujer**: plantilla floral/durazno (`assets/plantilla.png`), diseño original.
- **varon**: plantilla sobria azul marino / gris acero / dorado
  (`assets/plantilla_varon.png`), generada con formas geométricas.

## Qué hace el script, paso a paso

1. Abre la plantilla PNG correspondiente al tipo elegido.
2. Borra el texto de ejemplo (marca, nombre, cargo, ID) que trae la plantilla
   de mujer; la de varón ya se genera limpia.
3. Renderiza el logo SVG, lo recorta en círculo y lo pega centrado en el
   círculo del encabezado.
4. Genera un código de barras Code128 con el DNI, lo recorta al contenido
   real y lo pega bien grande en la mitad inferior de la credencial.
5. Guarda el resultado como `credencial_<DNI>.png`.

## Estructura del proyecto

```
generar-barras/
├── generar_credencial.py       # punto de entrada: genera una credencial
├── crear_plantilla_varon.py    # punto de entrada: (re)genera plantilla_varon.png
├── requirements.txt
├── assets/                     # plantillas y logos SVG (insumos, no se generan)
│   ├── plantilla.png
│   ├── plantilla_varon.png
│   ├── peach-svgrepo-com.svg
│   └── escudo-varon.svg
└── credenciales/                # paquete con toda la logica
    ├── config.py                # rutas, colores y coordenadas de la plantilla
    ├── logo.py                  # renderiza el SVG del logo dentro del circulo
    ├── codigo_barras.py         # genera la imagen del codigo de barras
    ├── plantilla_varon.py       # dibuja plantilla_varon.png desde cero
    ├── credencial.py            # compone plantilla + logo + codigo de barras
    └── cli.py                   # interfaz de linea de comandos (argparse)
```

Los archivos `credencial_<DNI>.png` que genera el script se guardan en la
raíz del proyecto (no se versionan en git).

## Instalación

Requiere Python 3.9+ y [Homebrew](https://brew.sh) (para `cairo`, que usa
`rlPyCairo` al renderizar los SVG).

```bash
# dependencias del sistema (una sola vez)
brew install pkg-config cairo

# entorno virtual del proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# credencial de mujer (plantilla por defecto)
python generar_credencial.py 70892343

# credencial de varon
python generar_credencial.py 70892343 --tipo varon

# logo y archivo de salida personalizados
python generar_credencial.py 70892343 --logo mi_logo.svg --salida mi_credencial.png
```

Si corrés el script sin argumentos, usa `DNI_POR_DEFECTO` definido en
`credenciales/config.py`.

Para regenerar `assets/plantilla_varon.png` desde cero (por ejemplo después
de tocar los colores o la distribución en `credenciales/plantilla_varon.py`):

```bash
python crear_plantilla_varon.py
```

## Uso como paquete

La lógica también se puede importar directamente en otro script Python:

```python
from credenciales import generar_credencial

generar_credencial("70892343", tipo="varon", archivo_salida="salida.png")
```
