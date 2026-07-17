import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import tempfile
import unittest
from core.export_import import ExportImportManager
from core.history import HistoryManager, HistoryEntry
from core.clipboard import ClipboardManager


class MockHistoryManager:
    def __init__(self):
        self._entries = []
        self._add_calls = []

    def add(self, expression, result, mode):
        self._add_calls.append((expression, result, mode))
        entry = HistoryEntry(expression=expression, result=result, mode=mode)
        self._entries.append(entry)
        return entry

    def get_all(self):
        return list(self._entries)


class MockClipboardManager:
    def __init__(self):
        self._entries = []
        self._copy_calls = []

    def copy(self, value, source_mode, label=""):
        self._copy_calls.append((value, source_mode, label))
        self._entries.append({"value": value, "source_mode": source_mode, "label": label})

    def get_all(self):
        return [
            type("Entry", (), {
                "value": e["value"],
                "label": e["label"],
                "source_mode": e["source_mode"],
                "timestamp": 0
            })()
            for e in self._entries
        ]


class TestExportImportHistory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.history = MockHistoryManager()
        self.eim = ExportImportManager(history_manager=self.history)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_export_history_json(self):
        self.history.add("1+1", "2", "standard")
        self.history.add("2*3", "6", "standard")
        count = self.eim.export_history_json(self.tmp.name)
        self.assertEqual(count, 2)
        with open(self.tmp.name, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["expression"], "1+1")
        self.assertEqual(data[0]["result"], "2")

    def test_import_history_json(self):
        entries = [
            {"expression": "1+1", "result": "2", "mode": "standard", "timestamp": 1000},
            {"expression": "2*3", "result": "6", "mode": "standard", "timestamp": 2000},
        ]
        with open(self.tmp.name, "w") as f:
            json.dump(entries, f)
        count = self.eim.import_history_json(self.tmp.name)
        self.assertEqual(count, 2)
        self.assertEqual(len(self.history._add_calls), 2)
        self.assertEqual(self.history._add_calls[0], ("1+1", "2", "standard"))

    def test_import_skips_empty_entries(self):
        entries = [
            {"expression": "", "result": "", "mode": "standard"},
            {"expression": "5+5", "result": "10", "mode": "standard"},
        ]
        with open(self.tmp.name, "w") as f:
            json.dump(entries, f)
        count = self.eim.import_history_json(self.tmp.name)
        self.assertEqual(count, 1)

    def test_export_empty_history(self):
        count = self.eim.export_history_json(self.tmp.name)
        self.assertEqual(count, 0)
        with open(self.tmp.name, "r") as f:
            data = json.load(f)
        self.assertEqual(data, [])


class TestExportImportNoManager(unittest.TestCase):
    def test_export_no_history_raises(self):
        eim = ExportImportManager()
        with self.assertRaises(RuntimeError):
            eim.export_history_json("test.json")

    def test_import_no_history_raises(self):
        eim = ExportImportManager()
        with self.assertRaises(RuntimeError):
            eim.import_history_json("test.json")


class TestExportImportInvalidFormat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.history = MockHistoryManager()
        self.eim = ExportImportManager(history_manager=self.history)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_import_invalid_json(self):
        with open(self.tmp.name, "w") as f:
            f.write("not valid json {{{")
        with self.assertRaises(json.JSONDecodeError):
            self.eim.import_history_json(self.tmp.name)

    def test_import_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.eim.import_history_json("/nonexistent/path.json")


class TestExportImportSession(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.history = MockHistoryManager()
        self.clipboard = MockClipboardManager()
        self.eim = ExportImportManager(
            history_manager=self.history,
            clipboard_manager=self.clipboard,
        )

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_export_session(self):
        self.history.add("1+1", "2", "standard")
        self.eim.export_session(self.tmp.name)
        with open(self.tmp.name, "r") as f:
            data = json.load(f)
        self.assertIn("exported_at", data)
        self.assertIn("history", data)
        self.assertEqual(len(data["history"]), 1)
        self.assertEqual(data["history"][0]["expression"], "1+1")

    def test_import_session(self):
        session = {
            "history": [
                {"expression": "2+2", "result": "4", "mode": "standard", "timestamp": 1000}
            ]
        }
        with open(self.tmp.name, "w") as f:
            json.dump(session, f)
        self.eim.import_session(self.tmp.name)
        self.assertEqual(len(self.history._add_calls), 1)
        self.assertEqual(self.history._add_calls[0], ("2+2", "4", "standard"))


class TestExportImportCSV(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        self.tmp.close()
        self.history = MockHistoryManager()
        self.eim = ExportImportManager(history_manager=self.history)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_export_csv(self):
        self.history.add("1+1", "2", "standard")
        count = self.eim.export_history_csv(self.tmp.name)
        self.assertEqual(count, 1)
        with open(self.tmp.name, "r") as f:
            content = f.read()
        self.assertIn("expression", content)
        self.assertIn("1+1", content)

    def test_export_csv_empty(self):
        count = self.eim.export_history_csv(self.tmp.name)
        self.assertEqual(count, 0)


class TestExportImportTxt(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        self.tmp.close()
        self.history = MockHistoryManager()
        self.eim = ExportImportManager(history_manager=self.history)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_export_txt(self):
        self.history.add("1+1", "2", "standard")
        count = self.eim.export_history_txt(self.tmp.name)
        self.assertEqual(count, 1)
        with open(self.tmp.name, "r") as f:
            content = f.read()
        self.assertIn("Calculation History", content)
        self.assertIn("1+1", content)


if __name__ == "__main__":
    unittest.main()
