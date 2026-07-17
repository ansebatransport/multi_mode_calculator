import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.state_manager import StateManager
from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser


class TestModeSwitchingPreservesResult(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator()

    def test_switch_from_standard_to_scientific_keeps_result(self):
        result = self.evaluator.evaluate(self.parser.parse("2+3"))
        self.state_manager.save_state("standard", "result", result)
        self.state_manager.save_state("scientific", "result", self.state_manager.restore_state("scientific", "result"))
        self.state_manager.save_state("scientific", "result", result)
        restored = self.state_manager.restore_state("scientific", "result")
        self.assertEqual(restored, 5)

    def test_switch_back_restores_previous(self):
        self.evaluator.set_variable("ans", 42)
        self.state_manager.save_state("standard", "ans", 42)
        self.state_manager.save_state("graph", "ans", None)
        self.state_manager.save_state("standard", "ans", self.state_manager.restore_state("standard", "ans"))
        restored = self.state_manager.restore_state("standard", "ans")
        self.assertEqual(restored, 42)


class TestModeSwitchingProgrammerConversion(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_switch_to_programmer_converts_display(self):
        decimal_value = 255
        hex_value = hex(decimal_value)
        self.state_manager.save_state("programmer", "display_mode", "hex")
        self.state_manager.save_state("programmer", "value", hex_value)
        restored_val = self.state_manager.restore_state("programmer", "value")
        self.assertEqual(restored_val, "0xff")
        mode = self.state_manager.restore_state("programmer", "display_mode", "dec")
        self.assertEqual(mode, "hex")


class TestModeSwitchingGraph(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_switch_to_graph_doesnt_lose_state(self):
        calculator_state = {"expression": "2+3", "result": "5", "memory": [0.0] * 10}
        self.state_manager.save_state("standard", "calculator_state", calculator_state)
        self.state_manager.save_state("graph", "equations", ["x**2"])
        restored = self.state_manager.restore_state("standard", "calculator_state")
        self.assertEqual(restored["expression"], "2+3")
        self.assertEqual(restored["result"], "5")

    def test_graph_state_separate_from_calc(self):
        self.state_manager.save_state("graph", "equations", ["sin(x)", "cos(x)"])
        self.state_manager.save_state("standard", "result", 10)
        graph_equations = self.state_manager.restore_state("graph", "equations")
        self.assertEqual(graph_equations, ["sin(x)", "cos(x)"])


class TestModeSwitchingMultipleModes(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_three_mode_cycle(self):
        modes = ["standard", "scientific", "programmer"]
        for i, mode in enumerate(modes):
            self.state_manager.save_state(mode, "index", i)
        for mode in modes:
            val = self.state_manager.restore_state(mode, "index")
            self.assertIsNotNone(val)

    def test_switch_mode_clears_state(self):
        self.state_manager.save_state("scientific", "temp", "data")
        self.state_manager.clear_state("scientific")
        result = self.state_manager.restore_state("scientific", "temp", "not_found")
        self.assertEqual(result, "not_found")

    def test_get_mode_state_snapshot(self):
        self.state_manager.save_state("standard", "a", 1)
        self.state_manager.save_state("standard", "b", 2)
        snapshot = self.state_manager.get_mode_state("standard")
        self.assertEqual(snapshot, {"a": 1, "b": 2})


class TestModeSwitchingStateIsolation(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()

    def test_modes_dont_interfere(self):
        self.state_manager.save_state("standard", "result", 100)
        self.state_manager.save_state("scientific", "result", 200)
        std = self.state_manager.restore_state("standard", "result")
        sci = self.state_manager.restore_state("scientific", "result")
        self.assertEqual(std, 100)
        self.assertEqual(sci, 200)

    def test_clear_all(self):
        self.state_manager.save_state("standard", "x", 1)
        self.state_manager.save_state("scientific", "y", 2)
        self.state_manager.clear_all()
        self.assertEqual(self.state_manager.restore_state("standard", "x", None), None)
        self.assertEqual(self.state_manager.restore_state("scientific", "y", None), None)
