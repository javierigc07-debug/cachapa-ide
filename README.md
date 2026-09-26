# CACHAPA — Mini IDE (Proyecto Synthetix Studio)

**C**onsola de **A**nálisis, **C**omandos, **H**istorial, **A**lgoritmos, **P**ilas y **A**PI.

Proyecto de Algoritmos y Estructuras de Datos II (UJAP, septiembre 2026).

Entorno de desarrollo minimalista por consola, estructurado con el **patrón
Command**. Todas las estructuras de datos (lista enlazada, pila, cola) y los
algoritmos de ordenamiento (Mergesort, Shellsort) están implementados desde
cero, sin usar estructuras predefinidas ni `.sort()`.

## Requisitos

- Python 3.10 o superior (solo biblioteca estándar, no hay dependencias externas).
- Opcional: una API key de [OpenRouter](https://openrouter.ai) para el comando `analyze`.

## Ejecución

```bash
python main.py              # usa config.json
python main.py otra.json    # usa otro archivo de configuración
```

Al iniciar, el programa lee obligatoriamente el archivo de configuración.
Python es interpretado: no requiere compilación.

### Clave de la API de IA

La clave **no** se guarda en el repositorio. Se lee de la variable de entorno
indicada en `config.json` (`api_key_env`, por defecto `SYNTHETIX_API_KEY`):

```bash
# PowerShell
$env:SYNTHETIX_API_KEY = "sk-or-..."
# Linux / macOS / Git Bash
export SYNTHETIX_API_KEY="sk-or-..."
```

Sin clave, `analyze` funciona en modo local: da una estimación básica de la
complejidad a partir de los bucles del código.

Para probar todos los módulos paso a paso, ver [PRUEBA.md](PRUEBA.md).

## Archivo de configuración (`config.json`)

```json
{
  "backup_dir": "./backups",
  "log_dir": "./logs",
  "api": {
    "base_url": "https://openrouter.ai/api/v1",
    "endpoint": "/chat/completions",
    "model": "google/gemini-2.5-flash",
    "api_key_env": "SYNTHETIX_API_KEY",
    "timeout_s": 30
  }
}
```

## Comandos

| Módulo | Comando | Descripción |
|---|---|---|
| Archivos y configuración | `new <nombre>` | Crea un archivo; el contenido se escribe línea por línea y termina con `:fin` |
| | `list` | Lista los archivos abiertos y marca el activo |
| | `switch <id/nombre>` | Cambia el archivo activo y muestra su contenido |
| | `delete <id/nombre>` | Elimina el archivo y libera su nodo |
| | `config <ruta>` | Carga un archivo de configuración |
| Validación e historial | `check` | Valida el balanceo de `()`, `{}`, `[]` e indica línea y columna del error |
| | `edit` | Reescribe el archivo activo (guarda el estado anterior para `undo`) |
| | `undo` / `redo` | Deshace / rehace usando dos pilas |
| Ordenamiento | `sort <line\|severity> <mergesort\|shellsort>` | Ordena los diagnósticos del análisis estático |
| Buffer de peticiones | `queue-status` | Muestra las peticiones pendientes en la cola FIFO |
| API de IA | `analyze` | Encola el código activo y lo envía a la IA (Big O y refactorización) |
| | `help` / `exit` | Ayuda / salir |

Ejemplo de sesión:

```text
cachapa> new utils.py
Escriba el contenido (termine con una línea ':fin'):
def foo():
    for i in range(10):
        if (i > 5:
            print(i)
:fin
cachapa> check
Error: símbolo '(' abierto en línea 3, columna 12 nunca fue cerrado.
cachapa> sort severity mergesort
```

## Arquitectura

```
main.py            Consola: lee cada línea y la pasa a SynthetixIDE.dispatch()
ide.py             SynthetixIDE: contiene los módulos y el mapa comando -> objeto Command
commands.py        Command (clase abstracta) y un Command concreto por cada comando
│
├── linked_list.py      FileLinkedList / FileNode — lista doblemente enlazada de archivos
├── stack.py            Stack — pila propia
├── syntax_checker.py   SyntaxChecker — balanceo de símbolos con la pila
├── history_manager.py  HistoryManager — undo/redo con dos pilas (una por archivo)
├── analyzer.py         StaticAnalyzer / Diagnostic — genera los diagnósticos
├── sorting.py          Sorter — Mergesort y Shellsort
├── queue_fifo.py       FIFOQueue — cola propia
├── request_buffer.py   RequestBuffer — encola y despacha las peticiones en orden
├── ai_client.py        AIClient — petición HTTP a la API (con modo local de respaldo)
└── config_loader.py    ConfigLoader — lee config.json
```

**Patrón Command:** cada comando de la consola es una clase que hereda de
`Command` e implementa `execute(args)`. `SynthetixIDE` solo busca el comando
en su mapa y lo ejecuta, así que agregar un comando nuevo no obliga a tocar el
despachador.
