"""Shared clipboard for cross-mode data transfer."""

__all__ = ["ClipboardEntry", "ClipboardManager"]

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ClipboardEntry:
    value: str
    label: str
    source_mode: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


class ClipboardManager:
    def __init__(self, max_entries: int = 20, persist_path: str = None) -> None:
        self._entries: list[ClipboardEntry] = []
        self._max = max_entries
        self._persist_path = persist_path or os.path.expanduser("~/.calc_clipboard.json")
        self._load()

    def copy(self, value: str, source_mode: str, label: str = "") -> ClipboardEntry:
        entry = ClipboardEntry(value=value, label=label, source_mode=source_mode)
        self._entries.append(entry)
        if len(self._entries) > self._max:
            self._entries.pop(0)
        self._save()
        return entry

    def paste(self, index: int = -1) -> str:
        if not self._entries:
            raise IndexError("Clipboard is empty")
        return self._entries[index].value

    def get_all(self) -> list[ClipboardEntry]:
        return list(self._entries)

    def delete(self, index: int) -> None:
        if not self._entries:
            raise IndexError("Clipboard is empty")
        del self._entries[index]
        self._save()

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def _load(self) -> None:
        try:
            with open(self._persist_path, "r") as f:
                data = json.load(f)
            self._entries = [ClipboardEntry(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError, TypeError, KeyError):
            self._entries = []

    def _save(self) -> None:
        data = [asdict(e) for e in self._entries]
        with open(self._persist_path, "w") as f:
            json.dump(data, f, indent=2)
