import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.history import HistoryManager, HistoryEntry


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self._tmp.close()
        self.hm = HistoryManager(max_entries=5, persist_path=self._tmp.name)

    def tearDown(self):
        os.unlink(self._tmp.name)

    def test_add_entry(self):
        entry = self.hm.add("2+3", "5", "standard")
        self.assertIsInstance(entry, HistoryEntry)
        self.assertEqual(entry.expression, "2+3")
        self.assertEqual(entry.result, "5")
        self.assertEqual(entry.mode, "standard")

    def test_get_all(self):
        self.hm.add("2+3", "5", "standard")
        self.hm.add("4*5", "20", "standard")
        all_entries = self.hm.get_all()
        self.assertEqual(len(all_entries), 2)

    def test_get_by_index(self):
        self.hm.add("2+3", "5", "standard")
        entry = self.hm.get(0)
        self.assertEqual(entry.expression, "2+3")

    def test_get_recent_entries(self):
        for i in range(5):
            self.hm.add(f"{i}+1", str(i + 1), "standard")
        all_entries = self.hm.get_all()
        self.assertEqual(len(all_entries), 5)
        self.assertEqual(all_entries[-1].expression, "4+1")

    def test_clear(self):
        self.hm.add("2+3", "5", "standard")
        self.hm.add("4*5", "20", "standard")
        self.hm.clear()
        self.assertEqual(len(self.hm.get_all()), 0)

    def test_max_entries(self):
        for i in range(10):
            self.hm.add(f"{i}+1", str(i + 1), "standard")
        all_entries = self.hm.get_all()
        self.assertEqual(len(all_entries), 5)
        self.assertEqual(all_entries[0].expression, "5+1")

    def test_search(self):
        self.hm.add("2+3", "5", "standard")
        self.hm.add("sqrt(9)", "3", "scientific")
        self.hm.add("4*5", "20", "standard")
        results = self.hm.search("sqrt")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].expression, "sqrt(9)")

    def test_search_case_insensitive(self):
        self.hm.add("SIN(30)", "0.5", "scientific")
        results = self.hm.search("sin")
        self.assertEqual(len(results), 1)

    def test_search_no_results(self):
        self.hm.add("2+3", "5", "standard")
        results = self.hm.search("xyz")
        self.assertEqual(len(results), 0)

    def test_delete(self):
        self.hm.add("2+3", "5", "standard")
        self.hm.add("4*5", "20", "standard")
        self.hm.delete(0)
        all_entries = self.hm.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0].expression, "4*5")

    def test_delete_empty(self):
        with self.assertRaises(IndexError):
            self.hm.delete(0)

    def test_get_empty(self):
        with self.assertRaises(IndexError):
            self.hm.get(0)

    def test_mode_filtering(self):
        self.hm.add("2+3", "5", "standard")
        self.hm.add("sin(30)", "0.5", "scientific")
        self.hm.add("4*5", "20", "standard")
        self.hm.add("log(100)", "2", "scientific")
        standard = [e for e in self.hm.get_all() if e.mode == "standard"]
        scientific = [e for e in self.hm.get_all() if e.mode == "scientific"]
        self.assertEqual(len(standard), 2)
        self.assertEqual(len(scientific), 2)

    def test_persistence(self):
        self.hm.add("2+3", "5", "standard")
        hm2 = HistoryManager(max_entries=5, persist_path=self._tmp.name)
        all_entries = hm2.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0].expression, "2+3")

    def test_timestamp_exists(self):
        entry = self.hm.add("2+3", "5", "standard")
        self.assertGreater(entry.timestamp, 0)


if __name__ == "__main__":
    unittest.main()
