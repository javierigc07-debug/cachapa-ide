"""Estructura de Pila (Stack) implementada desde cero con lista enlazada interna."""


class _StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    """Pila LIFO propia, sin usar list.append/pop ni collections."""

    def __init__(self):
        self._top = None
        self._size = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def push(self, value):
        node = _StackNode(value)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop():
        pass  # nunca usado, evitar stubs reales: reemplazado abajo

    def pop(self):
        if self.is_empty():
            return None
        node = self._top
        self._top = node.next
        self._size -= 1
        value = node.value
        node.next = None
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self._top.value

    def clear(self):
        self._top = None
        self._size = 0