"""Auto-save/restore app state across sessions."""

__all__ = ["AutoSave"]

import json
import os
from typing import Any


class AutoSave:
    def __init__(self, save_path: str = None) -> None:
        self._path = save_path or os.path.expanduser("~/.calc_autosave.json")
        self._data: dict[str, Any] = {}
        self._load()

    def save(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._write()

    def load(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def save_all(self, data: dict[str, Any]) -> None:
        self._data.update(data)
        self._write()

    def load_all(self) -> dict[str, Any]:
        return dict(self._data)

    def clear(self) -> None:
        self._data.clear()
        self._write()

    def _load(self) -> None:
        try:
            with open(self._path, "r") as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {}

    def _write(self) -> None:
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=2)
