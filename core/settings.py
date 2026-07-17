"""User settings/preferences with persistence."""

__all__ = [
    "AngleMode", "NumberBase", "DataSize", "DisplayFormat",
    "Settings", "SettingsManager",
]

import json
import os
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any


class AngleMode(Enum):
    DEGREES = "degrees"
    RADIANS = "radians"
    GRADIANS = "gradians"


class NumberBase(Enum):
    HEX = 16
    DEC = 10
    OCT = 8
    BIN = 2


class DataSize(Enum):
    BYTE = 8
    WORD = 16
    DWORD = 32
    QWORD = 64


class DisplayFormat(Enum):
    STANDARD = "standard"
    SCIENTIFIC = "scientific"
    ENGINEERING = "engineering"
    FRACTION = "fraction"


@dataclass
class Settings:
    angle_mode: str = "degrees"
    number_base: int = 10
    data_size: int = 64
    display_format: str = "standard"
    decimal_places: int = 10
    font_size: int = 16
    theme: str = "dark"
    always_on_top: bool = False
    show_history: bool = True
    show_clipboard: bool = True
    last_mode: str = "standard"
    window_width: int = 420
    window_height: int = 650
    window_x: int = -1
    window_y: int = -1
    signed_mode: bool = True


class SettingsManager:
    def __init__(self, persist_path: str = None) -> None:
        self._path = persist_path or os.path.expanduser("~/.calc_settings.json")
        self._settings = Settings()
        self._load()

    def get(self, key: str) -> Any:
        if not hasattr(self._settings, key):
            raise KeyError(f"Unknown setting: '{key}'")
        return getattr(self._settings, key)

    def set(self, key: str, value: Any) -> None:
        if not hasattr(self._settings, key):
            raise KeyError(f"Unknown setting: '{key}'")
        setattr(self._settings, key, value)
        self._save()

    def reset(self) -> None:
        self._settings = Settings()
        self._save()

    @property
    def angle_mode(self) -> str:
        return self._settings.angle_mode

    @property
    def display_format(self) -> str:
        return self._settings.display_format

    def _load(self) -> None:
        try:
            with open(self._path, "r") as f:
                data = json.load(f)
            for key, value in data.items():
                if hasattr(self._settings, key):
                    setattr(self._settings, key, value)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _save(self) -> None:
        with open(self._path, "w") as f:
            json.dump(asdict(self._settings), f, indent=2)
