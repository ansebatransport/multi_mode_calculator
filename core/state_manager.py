"""Preserves state when switching between calculator modes."""

__all__ = ["StateManager"]

from typing import Any


class StateManager:
    def __init__(self) -> None:
        self._states: dict[str, dict[str, Any]] = {}

    def save_state(self, mode: str, key: str, value: Any) -> None:
        if mode not in self._states:
            self._states[mode] = {}
        self._states[mode][key] = value

    def restore_state(self, mode: str, key: str, default: Any = None) -> Any:
        if mode not in self._states:
            return default
        return self._states[mode].get(key, default)

    def clear_state(self, mode: str) -> None:
        self._states.pop(mode, None)

    def clear_all(self) -> None:
        self._states.clear()

    def get_mode_state(self, mode: str) -> dict[str, Any]:
        return dict(self._states.get(mode, {}))
