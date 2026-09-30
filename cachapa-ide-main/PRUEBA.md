# Prueba guiada de CACHAPA

Recorrido de ~5 minutos por todos los módulos del proyecto. Cada paso dice qué
escribir, qué debería salir y qué estructura de datos se está usando.

Escribe cada comando después de `cachapa>` y pulsa Enter.

---

## 1. Abrir el programa

Desde una terminal, en la carpeta del proyecto:

```bash
python main.py
```

**Debería salir:** `Configuración cargada exitosamente` y luego el prompt `cachapa>`.

> Se ejecuta desde una terminal. Con doble clic la ventana se cierra al terminar.

---

## 2. Crear un archivo — *lista enlazada*

```text
new prueba.py
```

Pide el contenido. Pega el siguiente código **tal cual**. La última línea
`:fin` le indica al programa que terminaste de escribir:

```text
def buscar(lista, x):
    eval("print(x)")
    for i in range(len(lista)):
        for j in range(len(lista)):
            if (lista[i] == x:
                return i
    # TODO mejorar esto
    return -1
:fin
```

El código tiene errores **a propósito**: un `eval` peligroso (línea 2), un
paréntesis sin cerrar (línea 5) y un TODO pendiente (línea 7).

**Debería salir:** `Archivo 'prueba.py' creado y establecido como activo.`

---

## 3. Validar los paréntesis — *pila*

```text
check
```

**Debería salir:**

```text
Error: símbolo '(' abierto en línea 5, columna 16 nunca fue cerrado.
```

---

## 4. Ordenar los diagnósticos — *Mergesort y Shellsort*

```text
sort severity mergesort
```

**Debería salir** (de menos a más grave):

```text
  [L7] (INFO) Comentario TODO pendiente.
  [L5] (ERROR) Posible paréntesis desbalanceado en la línea.
  [L2] (CRITICAL) Uso de eval/exec: riesgo de seguridad.
```

```text
sort line shellsort
```

**Debería salir** (por número de línea):

```text
  [L2] (CRITICAL) Uso de eval/exec: riesgo de seguridad.
  [L5] (ERROR) Posible paréntesis desbalanceado en la línea.
  [L7] (INFO) Comentario TODO pendiente.
```

Son los mismos tres diagnósticos, en otro orden según el criterio.

---

## 5. Analizar con IA — *cola FIFO*

```text
analyze
queue-status
```

**Debería salir:** la petición se encola (`Request#1(prueba.py)`), se procesa y
muestra la complejidad y una sugerencia. Como hay dos `for` anidados, debería
decir **O(n²)**. Después, `queue-status` muestra `0` peticiones pendientes.

Sin clave de API sale `Fuente: local_fallback` (estimación local). Para usar la
IA real, antes de abrir el programa:

```bash
# PowerShell
$env:SYNTHETIX_API_KEY = "sk-or-tu-clave"
```

Con clave debería salir `Fuente: api` y una respuesta más completa.

---

## 6. Corregir, deshacer y rehacer — *dos pilas*

```text
edit
```

Pega la versión corregida:

```text
def buscar(lista, x):
    for i in range(len(lista)):
        if lista[i] == x:
            return i
    return -1
:fin
```

Luego:

```text
check
undo
redo
```

**Debería salir:**
- `check` → `El código está correctamente balanceado.`
- `undo` → vuelve a mostrar el código con errores del paso 2.
- `redo` → vuelve a mostrar el código corregido.

---

## 7. Varios archivos — *lista enlazada*

```text
new otro.cpp
```

```text
int main() { return 0; }
:fin
```

Luego:

```text
list
switch 1
delete otro.cpp
list
```

**Debería salir:**
- Primer `list` → `[1] prueba.py` y `[2] otro.cpp (ACTIVO)`.
- `switch 1` → cambia a `prueba.py` y muestra su contenido.
- `delete otro.cpp` → `Archivo 'otro.cpp' eliminado y memoria liberada.`
- Segundo `list` → solo queda `[1] prueba.py (ACTIVO)`.

---

## 8. Salir

```text
exit
```

---

## Si algo no coincide

Anota el paso, el comando que escribiste y lo que salió en la consola, y
avísale al equipo (o abre un *issue* en el repositorio).
