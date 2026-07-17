import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import os
import tempfile
import unittest
from core.history import HistoryManager
from core.clipboard import ClipboardManager
from core.export_import import ExportImportManager


class TestExportImportHistoryRoundTrip(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.history = HistoryManager(
            max_entries=100,
            persist_path=os.path.join(self.tmpdir, "history.json"),
        )
        self.manager = ExportImportManager(history_manager=self.history)

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmpdir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(self.tmpdir)

    def test_export_and_import_history_json(self):
        self.history.add("2+2", "4", "standard")
        self.history.add("3*3", "9", "scientific")
        filepath = os.path.join(self.tmpdir, "history_export.json")
        count = self.manager.export_history_json(filepath)
        self.assertEqual(count, 2)
        self.history.clear()
        count = self.manager.import_history_json(filepath)
        self.assertEqual(count, 2)
        entries = self.history.get_all()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].expression, "2+2")
        self.assertEqual(entries[1].expression, "3*3")

    def test_export_history_csv(self):
        self.history.add("10/2", "5", "standard")
        filepath = os.path.join(self.tmpdir, "history_export.csv")
        count = self.manager.export_history_csv(filepath)
        self.assertEqual(count, 1)
        self.assertTrue(os.path.exists(filepath))

    def test_export_history_txt(self):
        self.history.add("1+1", "2", "standard")
        filepath = os.path.join(self.tmpdir, "history_export.txt")
        count = self.manager.export_history_txt(filepath)
        self.assertEqual(count, 1)
        self.assertTrue(os.path.exists(filepath))

    def test_import_restores_identical_data(self):
        self.history.add("5+5", "10", "standard")
        filepath = os.path.join(self.tmpdir, "export.json")
        self.manager.export_history_json(filepath)
        self.history.clear()
        self.manager.import_history_json(filepath)
        entry = self.history.get(0)
        self.assertEqual(entry.expression, "5+5")
        self.assertEqual(entry.result, "10")
        self.assertEqual(entry.mode, "standard")


class TestExportImportSession(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.history = HistoryManager(
            max_entries=100,
            persist_path=os.path.join(self.tmpdir, "history.json"),
        )
        self.clipboard = ClipboardManager(
            max_entries=20,
            persist_path=os.path.join(self.tmpdir, "clipboard.json"),
        )
        self.manager = ExportImportManager(
            history_manager=self.history,
            clipboard_manager=self.clipboard,
        )

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmpdir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(self.tmpdir)

    def test_export_import_session_round_trip(self):
        self.history.add("2*3", "6", "standard")
        self.clipboard.copy("6", "standard", "2*3")
        filepath = os.path.join(self.tmpdir, "session.json")
        self.manager.export_session(filepath)
        self.history.clear()
        self.clipboard.clear()
        self.manager.import_session(filepath)
        history_entries = self.history.get_all()
        clipboard_entries = self.clipboard.get_all()
        self.assertEqual(len(history_entries), 1)
        self.assertEqual(history_entries[0].expression, "2*3")
        self.assertEqual(len(clipboard_entries), 1)
        self.assertEqual(clipboard_entries[0].value, "6")

    def test_session_file_contains_both_sections(self):
        self.history.add("4+4", "8", "standard")
        self.clipboard.copy("8", "standard")
        filepath = os.path.join(self.tmpdir, "session2.json")
        self.manager.export_session(filepath)
        with open(filepath) as f:
            data = json.load(f)
        self.assertIn("history", data)
        self.assertIn("clipboard", data)

    def test_import_empty_session(self):
        filepath = os.path.join(self.tmpdir, "empty_session.json")
        with open(filepath, "w") as f:
            json.dump({}, f)
        self.manager.import_session(filepath)
        self.assertEqual(len(self.history.get_all()), 0)
        self.assertEqual(len(self.clipboard.get_all()), 0)


class TestExportImportPartialExport(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmpdir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(self.tmpdir)

    def test_export_only_history_no_clipboard(self):
        history = HistoryManager(
            max_entries=100,
            persist_path=os.path.join(self.tmpdir, "history.json"),
        )
        export_only = ExportImportManager(history_manager=history)
        history.add("1+2", "3", "standard")
        filepath = os.path.join(self.tmpdir, "history_only.json")
        export_only.export_history_json(filepath)
        import_only = ExportImportManager(
            history_manager=HistoryManager(
                max_entries=100,
                persist_path=os.path.join(self.tmpdir, "history2.json"),
            ),
        )
        import_only.import_history_json(filepath)
        self.assertEqual(len(import_only._history.get_all()), 1)

    def test_export_no_history_returns_zero(self):
        history = HistoryManager(
            max_entries=100,
            persist_path=os.path.join(self.tmpdir, "empty_hist.json"),
        )
        export_only = ExportImportManager(history_manager=history)
        count = export_only.export_history_csv(os.path.join(self.tmpdir, "empty.csv"))
        self.assertEqual(count, 0)

    def test_export_without_history_manager_raises(self):
        export_only = ExportImportManager(history_manager=None)
        filepath = os.path.join(self.tmpdir, "no_hist.json")
        with self.assertRaises(RuntimeError):
            export_only.export_history_json(filepath)


class TestExportImportVerifyIdentical(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        for root, dirs, files in os.walk(self.tmpdir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(self.tmpdir)

    def test_imported_history_values_match(self):
        history = HistoryManager(
            max_entries=100,
            persist_path=os.path.join(self.tmpdir, "h1.json"),
        )
        original = [
            ("sin(0)", "0", "scientific"),
            ("cos(0)", "1", "scientific"),
            ("5!", "120", "standard"),
        ]
        for expr, res, mode in original:
            history.add(expr, res, mode)
        mgr = ExportImportManager(history_manager=history)
        filepath = os.path.join(self.tmpdir, "export.json")
        mgr.export_history_json(filepath)
        history.clear()
        mgr.import_history_json(filepath)
        imported = history.get_all()
        self.assertEqual(len(imported), 3)
        for orig, entry in zip(original, imported):
            self.assertEqual(entry.expression, orig[0])
            self.assertEqual(entry.result, orig[1])
            self.assertEqual(entry.mode, orig[2])
