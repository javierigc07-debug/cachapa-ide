"""
Punto de entrada del Mini IDE 'Synthetix Studio'.
Consola de línea de comandos: lee comandos y los despacha (Command Pattern).

Uso: python main.py [ruta_config]   (por defecto: config.json)
"""

import sys

from ide import SynthetixIDE


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"

    ide = SynthetixIDE()
    print("Synthetix Studio - Mini IDE. Escriba 'help' para ver los comandos.")

    # La configuración externa se lee obligatoriamente al iniciar.
    ide.dispatch(f"config {config_path}")
    if not ide.config.loaded:
        print("No se pudo iniciar sin configuración.")
        sys.exit(1)

    while True:
        try:
            line = input("synthetix> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip() in ("exit", "quit"):
            break
        ide.dispatch(line)


if __name__ == "__main__":
    main()
