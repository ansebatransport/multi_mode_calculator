"""Calculation history with persistence."""

__all__ = ["HistoryEntry", "HistoryManager"]

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List


@dataclass
class HistoryEntry:
    expression: str
    result: str
    mode: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


class HistoryManager:
    def __init__(self, max_entries: int = 100, persist_path: str = None) -> None:
        self._entries: list[HistoryEntry] = []
        self._max = max_entries
        self._persist_path = persist_path or os.path.expanduser("~/.calc_history.json")
        self._load()

    def add(self, expression: str, result: str, mode: str) -> HistoryEntry:
        entry = HistoryEntry(expression=expression, result=result, mode=mode)
        self._entries.append(entry)
        if len(self._entries) > self._max:
            self._entries = self._entries[-self._max:]
        self._save()
        return entry

    def get_all(self) -> list[HistoryEntry]:
        return list(self._entries)

    def get(self, index: int) -> HistoryEntry:
        if not self._entries:
            raise IndexError("History is empty")
        return self._entries[index]

    def search(self, query: str) -> list[HistoryEntry]:
        q = query.lower()
        return [e for e in self._entries if q in e.expression.lower() or q in e.result.lower()]

    def delete(self, index: int) -> None:
        if not self._entries:
            raise IndexError("History is empty")
        del self._entries[index]
        self._save()

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def _load(self) -> None:
        try:
            with open(self._persist_path, "r") as f:
                data = json.load(f)
            self._entries = [HistoryEntry(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError, TypeError, KeyError):
            self._entries = []

    def _save(self) -> None:
        data = [asdict(e) for e in self._entries]
        with open(self._persist_path, "w") as f:
            json.dump(data, f, indent=2)
