import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.undo_redo import UndoRedoManager


class TestUndoRedoBasic(unittest.TestCase):
    def setUp(self):
        self.mgr = UndoRedoManager()
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_execute(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 5)
        self.assertEqual(self.state["value"], 5)

    def test_undo(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 5)
        self.assertTrue(self.mgr.undo())
        self.assertEqual(self.state["value"], 0)

    def test_undo_returns_false_when_empty(self):
        self.assertFalse(self.mgr.undo())


class TestUndoRedoRedo(unittest.TestCase):
    def setUp(self):
        self.mgr = UndoRedoManager()
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_redo_after_undo(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 5)
        self.mgr.undo()
        self.assertTrue(self.mgr.redo())
        self.assertEqual(self.state["value"], 5)

    def test_redo_returns_false_when_empty(self):
        self.assertFalse(self.mgr.redo())

    def test_redo_multiple(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 1)
        self.mgr.execute(action, undo_action, 2)
        self.mgr.undo()
        self.mgr.undo()
        self.assertTrue(self.mgr.redo())
        self.assertEqual(self.state["value"], 1)
        self.assertTrue(self.mgr.redo())
        self.assertEqual(self.state["value"], 2)


class TestUndoRedoClearsRedo(unittest.TestCase):
    def setUp(self):
        self.mgr = UndoRedoManager()
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_new_push_clears_redo(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 5)
        self.mgr.undo()
        self.assertTrue(self.mgr.can_redo())
        self.mgr.execute(action, undo_action, 10)
        self.assertFalse(self.mgr.can_redo())


class TestUndoRedoMaxHistory(unittest.TestCase):
    def setUp(self):
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_max_history_limit(self):
        action, undo_action = self._make_pair()
        mgr = UndoRedoManager(max_history=3)
        mgr.execute(action, undo_action, 1)
        mgr.execute(action, undo_action, 2)
        mgr.execute(action, undo_action, 3)
        mgr.execute(action, undo_action, 4)
        count = 0
        while mgr.undo():
            count += 1
        self.assertEqual(count, 3)


class TestUndoRedoAvailability(unittest.TestCase):
    def setUp(self):
        self.mgr = UndoRedoManager()
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_can_undo(self):
        action, undo_action = self._make_pair()
        self.assertFalse(self.mgr.can_undo())
        self.mgr.execute(action, undo_action, 1)
        self.assertTrue(self.mgr.can_undo())

    def test_can_redo(self):
        action, undo_action = self._make_pair()
        self.assertFalse(self.mgr.can_redo())
        self.mgr.execute(action, undo_action, 1)
        self.mgr.undo()
        self.assertTrue(self.mgr.can_redo())

    def test_clear(self):
        action, undo_action = self._make_pair()
        self.mgr.execute(action, undo_action, 1)
        self.mgr.execute(action, undo_action, 2)
        self.mgr.clear()
        self.assertFalse(self.mgr.can_undo())
        self.assertFalse(self.mgr.can_redo())


class TestUndoRedoMultipleStates(unittest.TestCase):
    def setUp(self):
        self.mgr = UndoRedoManager()
        self.state = {"value": 0, "history": []}

    def _make_pair(self):
        def action(new_value):
            self.state["history"].append(self.state["value"])
            self.state["value"] = new_value
        def undo_action(new_value):
            self.state["value"] = self.state["history"].pop()
        return action, undo_action

    def test_multiple_undo_redo(self):
        action, undo_action = self._make_pair()
        for i in range(1, 6):
            self.mgr.execute(action, undo_action, i)
        self.assertEqual(self.state["value"], 5)
        self.mgr.undo()
        self.assertEqual(self.state["value"], 4)
        self.mgr.undo()
        self.assertEqual(self.state["value"], 3)
        self.mgr.redo()
        self.assertEqual(self.state["value"], 4)
        self.mgr.redo()
        self.assertEqual(self.state["value"], 5)


if __name__ == "__main__":
    unittest.main()
