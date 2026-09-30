# CACHAPA — Mini IDE (Proyecto Synthetix Studio)

**C**onsola de **A**nálisis, **C**omandos, **H**istorial, **A**lgoritmos, **P**ilas y **A**PI.

**Universidad José Antonio Páez (UJAP)**  
**Facultad de Ingeniería — Escuela de Ingeniería en Computación**  
**Materia:** Algoritmos y Estructuras de Datos II  

---

## 📋 Descripción del Proyecto

CACHAPA es un entorno de desarrollo minimalista por consola (Mini IDE) desarrollado íntegramente en Python utilizando Programación Orientada a Objetos (POO). Aplica el **Patrón de Diseño Command** para desacoplar y estructurar la ejecución de las operaciones sobre el código fuente.

**Regla Estricta Cumplida:** Todas las estructuras de datos lineales (Lista Enlazada Doble, Pila LIFO, Cola FIFO) y los algoritmos de ordenamiento (Mergesort y Shellsort) han sido **diseñados e implementados desde cero**, sin hacer uso de librerías ni estructuras nativas (como `std::list`, `std::stack`, `std::queue` o `.sort()`).

---

## 🏗️ Arquitectura del Sistema y Diseño de Clases

El sistema sigue una arquitectura modular en POO basada en el patrón **Command Pattern**:

```text
main.py            Entry point: ciclo interactivo CLI (input `cachapa>`).
ide.py             SynthetixIDE: orquestador central (contiene el registro comando -> Command).
commands.py        Interfaz abstracta Command y las 13 implementaciones concretas.
│
├── linked_list.py      FileNode y FileLinkedList (Lista Doblemente Enlazada de archivos).
├── stack.py            Node y Stack (Pila LIFO propia).
├── syntax_checker.py   SyntaxChecker (validador de balanceo de () {} [] usando la Pila).
├── history_manager.py  HistoryManager (control Undo/Redo con dos Pilas independientes).
├── analyzer.py         StaticAnalyzer y Diagnostic (recolector de diagnósticos y métricas).
├── sorting.py          Sorter (ordenamiento avanzado Mergesort y Shellsort).
├── queue_fifo.py       QueueNode y FIFOQueue (Cola FIFO propia).
├── request_buffer.py   RequestBuffer (administrador de solicitudes a la IA en cola FIFO).
├── ai_client.py        AIClient (cliente de comunicación HTTP con la API de IA).
└── config_loader.py    ConfigLoader (validador y cargador de `config.json`).
```

### Detalle de Clases Principales:

1. **`Command` (Interfaz Abstracta en `commands.py`)**: Define el método `execute(*args)`. Cada acción del CLI (`NewFileCommand`, `EditCommand`, `UndoCommand`, `CheckCommand`, etc.) hereda de esta clase.
2. **`FileLinkedList` / `FileNode` (`linked_list.py`)**: Representa la sesión de edición. Cada nodo contiene el nombre del archivo, su contenido en memoria, y punteros `prev` y `next`.
3. **`Stack` / `Node` (`stack.py`)**: Estructura LIFO con operaciones $O(1)$ (`push`, `pop`, `peek`, `is_empty`).
4. **`HistoryManager` (`history_manager.py`)**: Administra dos objetos `Stack` (`undo_stack` y `redo_stack`) por cada archivo abierto.
5. **`FIFOQueue` / `QueueNode` (`queue_fifo.py`)**: Estructura FIFO con punteros `front` y `rear` con operaciones $O(1)$ (`enqueue`, `dequeue`).
6. **`Sorter` (`sorting.py`)**: Implementaciones estáticas de **Mergesort** y **Shellsort** sobre arreglos de objetos `Diagnostic`.

---

## 📊 Justificación de Complejidad Algorítmica (Big O)

| Estructura / Algoritmo | Operación | Complejidad Temporal | Complejidad Espacial | Justificación Algorítmica |
|---|---|:---:|:---:|---|
| **Lista Enlazada Doble** (`FileLinkedList`) | Creación / Eliminación / Búsqueda | $O(1)$ inserción al final<br>$O(N)$ búsqueda | $O(N)$ | La inserción en el nodo `tail` es directa $O(1)$. La búsqueda o cambio por índice o nombre recorre secuencialmente los nodos $N$. |
| **Pila propia** (`Stack`) | `push`, `pop`, `peek` | $O(1)$ | $O(N)$ | Operaciones en el tope del apuntador de la pila sin necesidad de desplazamiento de memoria. |
| **Verificador de Sintaxis** (`SyntaxChecker`) | `check(code)` | $O(L)$ | $O(L)$ | Recorre los $L$ caracteres del código activo en una sola pasada. Apila aperturas y desapila en cierres. |
| **Historial Undo/Redo** (`HistoryManager`) | `undo` / `redo` | $O(1)$ | $O(K)$ | Apila y desapila el contenido previo en tiempo constante. $K$ es el número de estados guardados. |
| **Cola FIFO** (`FIFOQueue`) | `enqueue`, `dequeue` | $O(1)$ | $O(Q)$ | Inserción en `rear` y extracción desde `front` en tiempo constante directo $O(1)$. |
| **Mergesort** (`Sorter.mergesort`) | Ordenamiento de diagnósticos | $O(M \log M)$ | $O(M)$ | Divide el conjunto de $M$ diagnósticos recursivamente en mitades y realiza el *merge* de forma estable. |
| **Shellsort** (`Sorter.shellsort`) | Ordenamiento de diagnósticos | $O(M \log^2 M)$ a $O(M^{1.5})$ | $O(1)$ aux (In-place) | Utiliza secuencias de brechas (*gaps* $N/2^k$) para realizar ordenamientos por inserción distanciados de manera in-situ. |

---

## 🚀 Requisitos e Instalación

- **Python 3.10 o superior** (Utiliza únicamente la biblioteca estándar de Python, sin instalar paquetes con `pip`).
- **Archivo de Configuración:** Requiere `config.json` en la raíz del proyecto.

---

## ⚙️ Configuración (`config.json`)

Al iniciar la ejecución, el programa valida la presencia del archivo `config.json`. Si los directorios locales para respaldos (`backup_dir`) o logs (`log_dir`) no existen, se crean **automáticamente**.

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

### Clave API de Inteligencia Artificial (Opcional):
La clave API se lee de forma segura desde la variable de entorno `SYNTHETIX_API_KEY`:

```bash
# Windows (PowerShell)
$env:SYNTHETIX_API_KEY="sk-or-tu-api-key"

# Linux / macOS / Git Bash
export SYNTHETIX_API_KEY="sk-or-tu-api-key"
```
*(Si no se especifica una API Key, el comando `analyze` utiliza el motor de análisis estático local por defecto).*

---

## 💻 Guía de Uso del CLI (Comandos)

Para ejecutar la consola interactiva:

```bash
python main.py
```

| Módulo | Comando CLI | Descripción | Ejemplo de Uso |
|---|---|---|---|
| **Archivos y Configuración** | `new <nombre>` | Crea un nuevo archivo en memoria (ingresar texto y terminar con `:fin`). | `new script.py` |
| | `list` | Lista los archivos abiertos mostrando posición y estado (ACTIVO). | `list` |
| | `switch <id/nombre>` | Cambia el archivo activo actual para visualizar o editar. | `switch script.py` |
| | `delete <id/nombre>` | Elimina un archivo de la lista liberando sus nodos. | `delete 1` |
| | `config <ruta>` | Carga o recarga un archivo de configuración externo. | `config config.json` |
| **Validación e Historial** | `check` | Valida el correcto balanceo de `()`, `{}`, `[]` indicando línea y columna. | `check` |
| | `edit` | Reescribe el archivo activo actual registrando el estado anterior en el historial. | `edit` |
| | `undo` | Deshace el último cambio realizado usando la Pila de retroceso. | `undo` |
| | `redo` | Rehace el cambio previamente deshecho usando la Pila de avance. | `redo` |
| **Motor de Ordenamiento** | `sort <criterio> <algoritmo>` | Ordena alertas por `line` o `severity` usando `mergesort` o `shellsort`. | `sort severity mergesort` |
| **Buffer de Peticiones** | `queue-status` | Muestra las peticiones pendientes administradas en la cola FIFO. | `queue-status` |
| **Integración con IA** | `analyze` | Encola el archivo activo en la cola FIFO y envía la solicitud HTTP a la API de IA. | `analyze` |
| **Sistema** | `help` / `exit` | Muestra la ayuda de comandos o sale del programa. | `help` |

---

## 🧪 Ejemplo de Sesión en la Consola

```text
CACHAPA - Mini IDE (Synthetix Studio). Escriba 'help' para ver los comandos.
Configuración cargada exitosamente:
  ConfigLoader(backup_dir=./backups, log_dir=./logs, api_url=https://openrouter.ai/api/v1/chat/completions, model=google/gemini-2.5-flash)

cachapa> new main.py
Escriba el contenido (termine con una línea ':fin'):
def calcular(n):
    for i in range(n:
        print(i)
:fin
Archivo 'main.py' creado y establecido como activo.

cachapa> check
Error: símbolo '(' abierto en línea 2, columna 19 nunca fue cerrado.

cachapa> edit
Escriba el contenido (termine con una línea ':fin'):
def calcular(n):
    for i in range(n):
        print(i)
:fin
Contenido de 'main.py' actualizado.

cachapa> check
El código está correctamente balanceado.

cachapa> undo
Undo aplicado. Contenido actual:
def calcular(n):
    for i in range(n:
        print(i)

cachapa> exit
```
