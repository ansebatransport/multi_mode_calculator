"""Export/import calculation history and sessions."""

__all__ = ["ExportImportManager"]

import csv
import json
import os
from datetime import datetime
from typing import Any, Optional


class ExportImportManager:
    def __init__(
        self,
        history_manager: Optional[Any] = None,
        clipboard_manager: Optional[Any] = None,
    ) -> None:
        self._history = history_manager
        self._clipboard = clipboard_manager

    def export_history_json(self, filepath: str) -> int:
        if self._history is None:
            raise RuntimeError("History manager not available")
        entries = [h.__dict__ if hasattr(h, "__dict__") else h for h in self._history.get_all()]
        with open(filepath, "w") as f:
            json.dump(entries, f, indent=2)
        return len(entries)

    def export_history_csv(self, filepath: str) -> int:
        if self._history is None:
            raise RuntimeError("History manager not available")
        entries = self._history.get_all()
        if not entries:
            return 0
        fieldnames = ["expression", "result", "mode", "timestamp"]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in entries:
                writer.writerow({"expression": e.expression, "result": e.result, "mode": e.mode, "timestamp": e.timestamp})
        return len(entries)

    def export_history_txt(self, filepath: str) -> int:
        if self._history is None:
            raise RuntimeError("History manager not available")
        entries = self._history.get_all()
        with open(filepath, "w") as f:
            f.write("Calculation History\n")
            f.write("=" * 60 + "\n\n")
            for i, e in enumerate(entries, 1):
                dt = datetime.fromtimestamp(e.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{i}] {dt} | {e.mode}\n")
                f.write(f"    {e.expression} = {e.result}\n\n")
        return len(entries)

    def import_history_json(self, filepath: str) -> int:
        if self._history is None:
            raise RuntimeError("History manager not available")
        with open(filepath, "r") as f:
            data = json.load(f)
        count = 0
        for item in data:
            expr = item.get("expression", "")
            result = item.get("result", "")
            mode = item.get("mode", "standard")
            if expr or result:
                self._history.add(expr, result, mode)
                count += 1
        return count

    def export_session(self, filepath: str) -> None:
        session: dict[str, Any] = {
            "exported_at": datetime.now().isoformat(),
        }
        if self._history is not None:
            session["history"] = [
                {"expression": e.expression, "result": e.result, "mode": e.mode, "timestamp": e.timestamp}
                for e in self._history.get_all()
            ]
        if self._clipboard is not None:
            session["clipboard"] = [
                {"value": c.value, "label": c.label, "source_mode": c.source_mode, "timestamp": c.timestamp}
                for c in self._clipboard.get_all()
            ]
        with open(filepath, "w") as f:
            json.dump(session, f, indent=2)

    def import_session(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            session = json.load(f)
        if "history" in session and self._history is not None:
            for item in session["history"]:
                self._history.add(
                    item.get("expression", ""),
                    item.get("result", ""),
                    item.get("mode", "standard"),
                )
        if "clipboard" in session and self._clipboard is not None:
            for item in session["clipboard"]:
                self._clipboard.copy(
                    item.get("value", ""),
                    item.get("source_mode", "standard"),
                    item.get("label", ""),
                )
