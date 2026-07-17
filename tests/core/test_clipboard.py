import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.clipboard import ClipboardManager, ClipboardEntry


class TestClipboardManager(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self._tmp.close()
        self.cm = ClipboardManager(max_entries=5, persist_path=self._tmp.name)

    def tearDown(self):
        os.unlink(self._tmp.name)

    def test_copy(self):
        entry = self.cm.copy("42", "standard", label="result")
        self.assertIsInstance(entry, ClipboardEntry)
        self.assertEqual(entry.value, "42")
        self.assertEqual(entry.source_mode, "standard")
        self.assertEqual(entry.label, "result")

    def test_copy_no_label(self):
        entry = self.cm.copy("100", "scientific")
        self.assertEqual(entry.label, "")

    def test_paste_most_recent(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "standard")
        self.assertEqual(self.cm.paste(), "20")

    def test_paste_by_index(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "standard")
        self.assertEqual(self.cm.paste(0), "10")
        self.assertEqual(self.cm.paste(1), "20")

    def test_paste_negative_index(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "standard")
        self.assertEqual(self.cm.paste(-1), "20")
        self.assertEqual(self.cm.paste(-2), "10")

    def test_paste_empty(self):
        with self.assertRaises(IndexError):
            self.cm.paste()

    def test_clear(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "standard")
        self.cm.clear()
        self.assertEqual(len(self.cm.get_all()), 0)

    def test_max_entries(self):
        for i in range(10):
            self.cm.copy(str(i), "standard")
        all_entries = self.cm.get_all()
        self.assertEqual(len(all_entries), 5)
        self.assertEqual(all_entries[0].value, "5")
        self.assertEqual(all_entries[-1].value, "9")

    def test_source_mode_tracking(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "scientific")
        self.cm.copy("30", "programmer")
        all_entries = self.cm.get_all()
        modes = [e.source_mode for e in all_entries]
        self.assertEqual(modes, ["standard", "scientific", "programmer"])

    def test_delete(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "standard")
        self.cm.delete(0)
        all_entries = self.cm.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0].value, "20")

    def test_delete_empty(self):
        with self.assertRaises(IndexError):
            self.cm.delete(0)

    def test_get_all(self):
        self.cm.copy("10", "standard")
        self.cm.copy("20", "scientific")
        all_entries = self.cm.get_all()
        self.assertEqual(len(all_entries), 2)

    def test_persistence(self):
        self.cm.copy("42", "standard")
        cm2 = ClipboardManager(max_entries=5, persist_path=self._tmp.name)
        self.assertEqual(cm2.paste(), "42")

    def test_timestamp_exists(self):
        entry = self.cm.copy("42", "standard")
        self.assertGreater(entry.timestamp, 0)

    def test_label_preserved(self):
        entry = self.cm.copy("42", "standard", label="my_value")
        self.assertEqual(entry.label, "my_value")


if __name__ == "__main__":
    unittest.main()
