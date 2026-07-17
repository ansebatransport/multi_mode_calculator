"""Command pattern base classes for undo/redo."""

__all__ = ["Command", "ExpressionCommand", "CompositeCommand"]

from abc import ABC, abstractmethod
from typing import Any, Callable


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any: ...

    @abstractmethod
    def undo(self) -> Any: ...


class ExpressionCommand(Command):
    def __init__(self, old_expr: str, new_expr: str, display_callback: Callable[[str], None]) -> None:
        self._old = old_expr
        self._new = new_expr
        self._callback = display_callback

    def execute(self) -> None:
        self._callback(self._new)

    def undo(self) -> None:
        self._callback(self._old)


class CompositeCommand(Command):
    def __init__(self, commands: list[Command]) -> None:
        self._commands = commands

    def execute(self) -> None:
        for c in self._commands:
            c.execute()

    def undo(self) -> None:
        for c in reversed(self._commands):
            c.undo()
