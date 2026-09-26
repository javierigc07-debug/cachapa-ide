"""Gestor de historial Undo/Redo basado en dos pilas independientes."""

from stack import Stack


class HistoryManager:
    def __init__(self):
        self._undo_stack = Stack()
        self._redo_stack = Stack()

    def register_change(self, previous_state: str):
        """Guarda el estado anterior antes de aplicar un cambio nuevo."""
        self._undo_stack.push(previous_state)
        self._redo_stack.clear()

    def undo(self, current_state: str):
        """Retrocede al estado anterior. Retorna el estado a restaurar o None."""
        if self._undo_stack.is_empty():
            return None
        previous_state = self._undo_stack.pop()
        self._redo_stack.push(current_state)
        return previous_state

    def redo(self, current_state: str):
        """Avanza al estado deshecho. Retorna el estado a restaurar o None."""
        if self._redo_stack.is_empty():
            return None
        next_state = self._redo_stack.pop()
        self._undo_stack.push(current_state)
        return next_state

    def has_undo(self) -> bool:
        return not self._undo_stack.is_empty()

    def has_redo(self) -> bool:
        return not self._redo_stack.is_empty()