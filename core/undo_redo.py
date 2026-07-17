"""Undo/redo system using command pattern."""

__all__ = ["UndoRedoManager"]

from typing import Any, Callable


class UndoRedoManager:
    def __init__(self, max_history: int = 100) -> None:
        self._undo_stack: list[tuple[Callable, Callable, tuple, dict]] = []
        self._redo_stack: list[tuple[Callable, Callable, tuple, dict]] = []
        self._max = max_history

    def execute(
        self, action: Callable, undo_action: Callable, *args, **kwargs
    ) -> Any:
        result = action(*args, **kwargs)
        self._undo_stack.append((action, undo_action, args, kwargs))
        if len(self._undo_stack) > self._max:
            self._undo_stack.pop(0)
        self._redo_stack.clear()
        return result

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        action, undo_action, args, kwargs = self._undo_stack.pop()
        undo_action(*args, **kwargs)
        self._redo_stack.append((action, undo_action, args, kwargs))
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        action, undo_action, args, kwargs = self._redo_stack.pop()
        action(*args, **kwargs)
        self._undo_stack.append((action, undo_action, args, kwargs))
        return True

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def clear(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
