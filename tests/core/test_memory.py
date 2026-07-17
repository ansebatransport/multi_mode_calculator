import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.memory import MemoryManager


class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.mem = MemoryManager()

    def test_initial_all_zero(self):
        for i in range(10):
            self.assertEqual(self.mem.recall(i), 0.0)

    def test_store_and_recall(self):
        self.mem.store(0, 42.5)
        self.assertEqual(self.mem.recall(0), 42.5)

    def test_store_multiple_registers(self):
        self.mem.store(0, 10)
        self.mem.store(1, 20)
        self.mem.store(2, 30)
        self.assertEqual(self.mem.recall(0), 10)
        self.assertEqual(self.mem.recall(1), 20)
        self.assertEqual(self.mem.recall(2), 30)

    def test_store_overwrites(self):
        self.mem.store(0, 10)
        self.mem.store(0, 99)
        self.assertEqual(self.mem.recall(0), 99)

    def test_add(self):
        self.mem.store(0, 10)
        self.mem.add(0, 5)
        self.assertEqual(self.mem.recall(0), 15)

    def test_add_to_zero(self):
        self.mem.add(0, 7)
        self.assertEqual(self.mem.recall(0), 7)

    def test_subtract(self):
        self.mem.store(0, 10)
        self.mem.subtract(0, 3)
        self.assertEqual(self.mem.recall(0), 7)

    def test_subtract_to_negative(self):
        self.mem.store(0, 5)
        self.mem.subtract(0, 10)
        self.assertEqual(self.mem.recall(0), -5)

    def test_clear_register(self):
        self.mem.store(3, 42)
        self.mem.clear(3)
        self.assertEqual(self.mem.recall(3), 0.0)

    def test_clear_does_not_affect_others(self):
        self.mem.store(0, 10)
        self.mem.store(1, 20)
        self.mem.clear(0)
        self.assertEqual(self.mem.recall(0), 0.0)
        self.assertEqual(self.mem.recall(1), 20)

    def test_clear_all(self):
        self.mem.store(0, 10)
        self.mem.store(5, 99)
        self.mem.store(9, 1)
        self.mem.clear_all()
        for i in range(10):
            self.assertEqual(self.mem.recall(i), 0.0)

    def test_out_of_range_high(self):
        with self.assertRaises(IndexError):
            self.mem.store(10, 1)

    def test_out_of_range_negative(self):
        with self.assertRaises(IndexError):
            self.mem.recall(-1)

    def test_out_of_range_add(self):
        with self.assertRaises(IndexError):
            self.mem.add(10, 5)

    def test_out_of_range_subtract(self):
        with self.assertRaises(IndexError):
            self.mem.subtract(10, 5)

    def test_out_of_range_clear(self):
        with self.assertRaises(IndexError):
            self.mem.clear(10)

    def test_to_dict(self):
        self.mem.store(0, 42)
        self.mem.store(9, 99)
        data = self.mem.to_dict()
        self.assertIn("registers", data)
        self.assertEqual(len(data["registers"]), 10)
        self.assertEqual(data["registers"][0], 42)
        self.assertEqual(data["registers"][9], 99)

    def test_from_dict(self):
        data = {"registers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
        self.mem.from_dict(data)
        self.assertEqual(self.mem.recall(0), 1)
        self.assertEqual(self.mem.recall(9), 10)

    def test_from_dict_invalid(self):
        with self.assertRaises(ValueError):
            self.mem.from_dict({"registers": [1, 2, 3]})


if __name__ == "__main__":
    unittest.main()
