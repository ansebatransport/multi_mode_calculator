import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.state_manager import StateManager


class TestStateManagerSetAndGet(unittest.TestCase):
    def setUp(self):
        self.sm = StateManager()

    def test_save_and_restore(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.assertEqual(self.sm.restore_state("graph", "zoom"), 2.0)

    def test_restore_default_when_missing(self):
        self.assertIsNone(self.sm.restore_state("graph", "zoom"))
        self.assertEqual(self.sm.restore_state("graph", "zoom", "fallback"), "fallback")

    def test_save_multiple_keys(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.sm.save_state("graph", "pan_x", 100)
        self.sm.save_state("graph", "pan_y", 50)
        self.assertEqual(self.sm.restore_state("graph", "zoom"), 2.0)
        self.assertEqual(self.sm.restore_state("graph", "pan_x"), 100)
        self.assertEqual(self.sm.restore_state("graph", "pan_y"), 50)

    def test_different_modes_independent(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.sm.save_state("stats", "zoom", 5.0)
        self.assertEqual(self.sm.restore_state("graph", "zoom"), 2.0)
        self.assertEqual(self.sm.restore_state("stats", "zoom"), 5.0)


class TestStateManagerNotifications(unittest.TestCase):
    def test_state_values_persist(self):
        sm = StateManager()
        sm.save_state("mode_a", "key1", "hello")
        sm.save_state("mode_a", "key2", 42)
        self.assertEqual(sm.restore_state("mode_a", "key1"), "hello")
        self.assertEqual(sm.restore_state("mode_a", "key2"), 42)

    def test_overwrite_state(self):
        sm = StateManager()
        sm.save_state("mode_a", "key1", "old")
        sm.save_state("mode_a", "key1", "new")
        self.assertEqual(sm.restore_state("mode_a", "key1"), "new")


class TestStateManagerReset(unittest.TestCase):
    def setUp(self):
        self.sm = StateManager()

    def test_clear_mode(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.sm.clear_state("graph")
        self.assertIsNone(self.sm.restore_state("graph", "zoom"))

    def test_clear_nonexistent_mode(self):
        self.sm.clear_state("nope")
        self.assertIsNone(self.sm.restore_state("nope", "key"))

    def test_clear_all(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.sm.save_state("stats", "mean", 5.0)
        self.sm.clear_all()
        self.assertIsNone(self.sm.restore_state("graph", "zoom"))
        self.assertIsNone(self.sm.restore_state("stats", "mean"))


class TestStateManagerGetModeState(unittest.TestCase):
    def setUp(self):
        self.sm = StateManager()

    def test_get_mode_state(self):
        self.sm.save_state("graph", "zoom", 2.0)
        self.sm.save_state("graph", "pan", 10)
        state = self.sm.get_mode_state("graph")
        self.assertEqual(state, {"zoom": 2.0, "pan": 10})

    def test_get_mode_state_empty(self):
        state = self.sm.get_mode_state("nope")
        self.assertEqual(state, {})

    def test_get_mode_state_returns_copy(self):
        self.sm.save_state("graph", "zoom", 2.0)
        state = self.sm.get_mode_state("graph")
        state["zoom"] = 999
        self.assertEqual(self.sm.restore_state("graph", "zoom"), 2.0)


class TestStateManagerExportImport(unittest.TestCase):
    def test_save_restore_various_types(self):
        sm = StateManager()
        sm.save_state("m", "str_val", "hello")
        sm.save_state("m", "int_val", 42)
        sm.save_state("m", "float_val", 3.14)
        sm.save_state("m", "list_val", [1, 2, 3])
        sm.save_state("m", "dict_val", {"a": 1})
        self.assertEqual(sm.restore_state("m", "str_val"), "hello")
        self.assertEqual(sm.restore_state("m", "int_val"), 42)
        self.assertAlmostEqual(sm.restore_state("m", "float_val"), 3.14)
        self.assertEqual(sm.restore_state("m", "list_val"), [1, 2, 3])
        self.assertEqual(sm.restore_state("m", "dict_val"), {"a": 1})


if __name__ == "__main__":
    unittest.main()
