"""Algoritmos de ordenamiento avanzados implementados desde cero: Mergesort y Shellsort."""


class Diagnostic:
    """Representa un diagnóstico/alerta de análisis estático de código."""

    SEVERITY_ORDER = {"info": 1, "warning": 2, "error": 3, "critical": 4}

    def __init__(self, line: int, message: str, severity: str):
        self.line = line
        self.message = message
        self.severity = severity.lower()

    def severity_weight(self) -> int:
        return self.SEVERITY_ORDER.get(self.severity, 0)

    def __repr__(self):
        return f"[L{self.line}] ({self.severity.upper()}) {self.message}"


class Sorter:
    """Contenedor de algoritmos de ordenamiento implementados manualmente."""

    @staticmethod
    def _key(diag: Diagnostic, criterio: str):
        if criterio == "line":
            return diag.line
        elif criterio == "severity":
            return diag.severity_weight()
        raise ValueError("Criterio inválido. Use 'line' o 'severity'.")

    # ---------------- MERGESORT ----------------
    @staticmethod
    def mergesort(items, criterio: str):
        arr = list(items)
        Sorter._merge_sort_rec(arr, criterio)
        return arr

    @staticmethod
    def _merge_sort_rec(arr, criterio):
        n = len(arr)
        if n <= 1:
            return
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]
        Sorter._merge_sort_rec(left, criterio)
        Sorter._merge_sort_rec(right, criterio)
        Sorter._merge(arr, left, right, criterio)

    @staticmethod
    def _merge(arr, left, right, criterio):
        i = j = k = 0
        while i < len(left) and j < len(right):
            if Sorter._key(left[i], criterio) <= Sorter._key(right[j], criterio):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    # ---------------- SHELLSORT ----------------
    @staticmethod
    def shellsort(items, criterio: str):
        arr = list(items)
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and Sorter._key(arr[j - gap], criterio) > Sorter._key(temp, criterio):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr