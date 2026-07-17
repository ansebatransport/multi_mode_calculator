import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import os
import unittest
from core.history import HistoryManager
from core.clipboard import ClipboardManager


class TestHistoryClipboardAddToHistory(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_entries=100, persist_path="/tmp/test_hc_history.json")

    def tearDown(self):
        if os.path.exists("/tmp/test_hc_history.json"):
            os.remove("/tmp/test_hc_history.json")

    def test_add_to_history_from_calculation(self):
        entry = self.history.add("2+3", "5", "standard")
        self.assertEqual(entry.expression, "2+3")
        self.assertEqual(entry.result, "5")

    def test_add_multiple_history_entries(self):
        for expr, res in [("1+1", "2"), ("2*3", "6"), ("10-4", "6")]:
            self.history.add(expr, res, "scientific")
        self.assertEqual(len(self.history.get_all()), 3)


class TestHistoryClipboardCopyPaste(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_entries=100, persist_path="/tmp/test_hc_history2.json")
        self.clipboard = ClipboardManager(max_entries=20, persist_path="/tmp/test_hc_clipboard.json")

    def tearDown(self):
        for p in ["/tmp/test_hc_history2.json", "/tmp/test_hc_clipboard.json"]:
            if os.path.exists(p):
                os.remove(p)

    def test_copy_history_entry_to_clipboard(self):
        h_entry = self.history.add("5*5", "25", "standard")
        c_entry = self.clipboard.copy(h_entry.result, h_entry.mode, h_entry.expression)
        self.assertEqual(c_entry.value, "25")
        self.assertEqual(c_entry.source_mode, "standard")
        self.assertEqual(c_entry.label, "5*5")

    def test_paste_clipboard_into_new_calculation(self):
        self.history.add("10+20", "30", "standard")
        self.clipboard.copy("30", "standard", "10+20")
        pasted = self.clipboard.paste()
        self.assertEqual(pasted, "30")

    def test_copy_then_paste_multiple(self):
        self.history.add("1+1", "2", "standard")
        self.clipboard.copy("2", "standard", "1+1")
        self.history.add("3+3", "6", "scientific")
        self.clipboard.copy("6", "scientific", "3+3")
        self.assertEqual(self.clipboard.paste(0), "2")
        self.assertEqual(self.clipboard.paste(1), "6")
        self.assertEqual(self.clipboard.paste(-1), "6")

    def test_clipboard_get_all_entries(self):
        self.clipboard.copy("100", "standard", "result")
        self.clipboard.copy("200", "scientific", "result")
        entries = self.clipboard.get_all()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].value, "100")
        self.assertEqual(entries[1].value, "200")


class TestHistoryClipboardClearOperations(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_entries=100, persist_path="/tmp/test_hc_history3.json")
        self.clipboard = ClipboardManager(max_entries=20, persist_path="/tmp/test_hc_clipboard3.json")

    def tearDown(self):
        for p in ["/tmp/test_hc_history3.json", "/tmp/test_hc_clipboard3.json"]:
            if os.path.exists(p):
                os.remove(p)

    def test_clear_history_doesnt_affect_clipboard(self):
        self.history.add("1+2", "3", "standard")
        self.clipboard.copy("3", "standard", "1+2")
        self.history.clear()
        self.assertEqual(len(self.history.get_all()), 0)
        self.assertEqual(self.clipboard.paste(), "3")

    def test_clear_clipboard_doesnt_affect_history(self):
        self.history.add("4+5", "9", "standard")
        self.clipboard.copy("9", "standard", "4+5")
        self.clipboard.clear()
        with self.assertRaises(IndexError):
            self.clipboard.paste()
        self.assertEqual(len(self.history.get_all()), 1)

    def test_delete_from_history_preserves_clipboard(self):
        self.history.add("7+7", "14", "standard")
        self.clipboard.copy("14", "standard", "7+7")
        self.history.delete(0)
        self.assertEqual(len(self.history.get_all()), 0)
        self.assertEqual(self.clipboard.paste(0), "14")

    def test_delete_from_clipboard_preserves_history(self):
        self.history.add("8+8", "16", "standard")
        self.clipboard.copy("16", "standard", "8+8")
        self.clipboard.delete(0)
        with self.assertRaises(IndexError):
            self.clipboard.paste()
        self.assertEqual(len(self.history.get_all()), 1)


class TestHistoryClipboardSearchAndIndices(unittest.TestCase):
    def setUp(self):
        self.history = HistoryManager(max_entries=100, persist_path="/tmp/test_hc_history4.json")

    def tearDown(self):
        if os.path.exists("/tmp/test_hc_history4.json"):
            os.remove("/tmp/test_hc_history4.json")

    def test_search_history(self):
        self.history.add("sin(0)", "0", "scientific")
        self.history.add("cos(0)", "1", "scientific")
        results = self.history.search("sin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].result, "0")

    def test_get_history_by_index(self):
        self.history.add("first", "1", "standard")
        self.history.add("second", "2", "standard")
        self.assertEqual(self.history.get(0).expression, "first")
        self.assertEqual(self.history.get(1).expression, "second")

    def test_get_empty_history_raises(self):
        with self.assertRaises(IndexError):
            self.history.get(0)
