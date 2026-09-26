"""
Punto de entrada de CACHAPA, el Mini IDE del proyecto Synthetix Studio.
Consola de línea de comandos: lee comandos y los despacha (Command Pattern).

Uso: python main.py [ruta_config]   (por defecto: config.json)
"""

import os
import sys

from ide import SynthetixIDE


def main():
    # Trabajar siempre desde la carpeta del proyecto, aunque se ejecute con
    # doble clic o con el botón Run del editor desde otra carpeta.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"

    ide = SynthetixIDE()
    print("CACHAPA - Mini IDE (Synthetix Studio). Escriba 'help' para ver los comandos.")

    # La configuración externa se lee obligatoriamente al iniciar.
    ide.dispatch(f"config {config_path}")
    if not ide.config.loaded:
        print("No se pudo iniciar sin configuración.")
        sys.exit(1)

    while True:
        try:
            line = input("cachapa> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip() in ("exit", "quit"):
            break
        ide.dispatch(line)


if __name__ == "__main__":
    main()
