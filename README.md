
# Flecha Parser

Este proyecto es un parser para el lenguaje funcional "Flecha" utilizando Python y PLY. El objetivo es analizar el código fuente de Flecha y generar un AST (Árbol de Sintaxis Abstracta) en formato JSON.

## Requisitos

- Python 3.11.4
- PLY (Python Lex-Yacc). (Versión recomendada: 3.11).

## Instalación

Antes de ejecutar el proyecto, asegúrate de instalar PLY. Puedes hacerlo utilizando `pip`:

```bash
pip install ply
```

## Archivos

El repositorio contiene los siguientes archivos:

- `flecha_parser.py`: Contiene las reglas del parser y las definiciones del AST.
- `lexer_flecha.py`: Define los tokens y el lexer para el lenguaje Flecha.
- `main.py`: Script principal para ejecutar el parser en la consola.
- `pueba.input`: Archivo de entrada que contiene el código que se desea analizar.
- `salida.json`: Archivo de salida que contiene el AST generado en formato JSON.

## Uso

Para ejecutar el parser desde la línea de comandos, sigue los siguientes pasos:

1. Abre la terminal y navega a la carpeta del proyecto.
2. Usa el siguiente comando para ejecutar `main.py`:

```bash
python main.py prueba.input salida.json
```

## Estructura del AST

El AST se genera en formato JSON y sigue una estructura jerárquica que representa las construcciones y expresiones del lenguaje Flecha. Puedes revisar `salida.json` para ver un ejemplo del AST generado.
En caso de haber errores se mostrarán en la consola que se ejecutó el comando.