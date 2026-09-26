"""Estructura de Lista Doblemente Enlazada implementada desde cero."""


class FileNode:
    """Nodo que representa un archivo abierto en la sesión."""

    def __init__(self, name: str, content: str = ""):
        self.name = name
        self.content = content
        self.prev = None
        self.next = None


class FileLinkedList:
    """Lista doblemente enlazada de archivos (implementación propia)."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.active_node = None
        self._size = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def create_file(self, name: str, content: str = "") -> FileNode:
        """Crea un nuevo archivo en memoria y lo agrega al final de la lista."""
        node = FileNode(name, content)
        if self.is_empty():
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        self.active_node = node
        return node

    def find(self, identifier: str):
        """Busca un archivo por nombre o por índice (id) posicional (1-based)."""
        current = self.head
        idx = 1
        try:
            target_idx = int(identifier)
        except ValueError:
            target_idx = None

        while current is not None:
            if current.name == identifier or idx == target_idx:
                return current
            current = current.next
            idx += 1
        return None

    def list_files(self):
        """Retorna lista de tuplas (posicion, nombre, es_activo)."""
        result = []
        current = self.head
        idx = 1
        while current is not None:
            result.append((idx, current.name, current is self.active_node))
            current = current.next
            idx += 1
        return result

    def switch_active(self, identifier: str) -> bool:
        node = self.find(identifier)
        if node is None:
            return False
        self.active_node = node
        return True

    def delete_file(self, identifier: str) -> bool:
        """Elimina un nodo de la lista liberando referencias (memoria)."""
        node = self.find(identifier)
        if node is None:
            return False

        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        if self.active_node is node:
            self.active_node = self.head if self.head is not None else None

        # Liberación explícita de referencias del nodo
        node.prev = None
        node.next = None
        node.content = None
        self._size -= 1
        return True