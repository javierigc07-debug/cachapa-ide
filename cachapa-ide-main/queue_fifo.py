"""Estructura de Cola FIFO implementada desde cero con lista enlazada interna."""


class _QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class FIFOQueue:
    """Cola First-In First-Out propia."""

    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def enqueue(self, value):
        node = _QueueNode(value)
        if self.is_empty():
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        node = self._front
        self._front = node.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        value = node.value
        node.next = None
        return value

    def to_list_snapshot(self):
        """Devuelve una representación (no destructiva) del contenido actual."""
        result = []
        current = self._front
        while current is not None:
            result.append(current.value)
            current = current.next
        return result