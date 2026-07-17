import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser
from core.history import HistoryManager
from core.memory import MemoryManager
from core.undo_redo import UndoRedoManager


class TestPipelineParseEvaluateDisplay(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator()

    def test_parse_and_evaluate_simple_addition(self):
        tokens = self.parser.parse("2+3")
        result = self.evaluator.evaluate(tokens)
        self.assertEqual(result, 5)

    def test_parse_and_evaluate_complex_expression(self):
        tokens = self.parser.parse("(2+3)*4")
        result = self.evaluator.evaluate(tokens)
        self.assertEqual(result, 20)

    def test_parse_and_evaluate_with_constants(self):
        tokens = self.parser.parse("π*2")
        result = self.evaluator.evaluate(tokens)
        self.assertAlmostEqual(result, 6.283185307179586)

    def test_parse_and_evaluate_trig(self):
        tokens = self.parser.parse("sin(0)")
        result = self.evaluator.evaluate(tokens)
        self.assertAlmostEqual(result, 0.0)


class TestPipelineChainCalculations(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator()

    def test_chain_addition_result_to_next(self):
        r1 = self.evaluator.evaluate(self.parser.parse("3+4"))
        self.evaluator.set_variable("ans", r1)
        r2 = self.evaluator.evaluate(self.parser.parse("ans*2"))
        self.assertEqual(r2, 14)

    def test_chain_multiple_steps(self):
        r1 = self.evaluator.evaluate(self.parser.parse("10/2"))
        self.evaluator.set_variable("ans", r1)
        r2 = self.evaluator.evaluate(self.parser.parse("ans+3"))
        self.evaluator.set_variable("ans", r2)
        r3 = self.evaluator.evaluate(self.parser.parse("ans*4"))
        self.assertEqual(r3, 32)


class TestPipelineMemoryDuringCalculation(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator()
        self.memory = MemoryManager()

    def test_store_result_then_recall(self):
        result = self.evaluator.evaluate(self.parser.parse("5+7"))
        self.memory.store(0, result)
        self.assertEqual(self.memory.recall(0), 12)

    def test_memory_add_during_chain(self):
        result = self.evaluator.evaluate(self.parser.parse("100"))
        self.memory.store(0, result)
        self.memory.add(0, 50)
        self.assertEqual(self.memory.recall(0), 150)


class TestPipelineHistoryRecording(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator()
        self.history = HistoryManager(max_entries=100, persist_path="/tmp/test_calc_pipeline_history.json")

    def tearDown(self):
        if os.path.exists("/tmp/test_calc_pipeline_history.json"):
            os.remove("/tmp/test_calc_pipeline_history.json")

    def test_history_records_expression_and_result(self):
        expr = "2+3"
        result = self.evaluator.evaluate(self.parser.parse(expr))
        entry = self.history.add(expr, str(result), "standard")
        self.assertEqual(entry.expression, expr)
        self.assertEqual(entry.result, "5.0")

    def test_history_has_multiple_entries(self):
        results = []
        for expr in ["1+1", "2+2", "3+3"]:
            r = self.evaluator.evaluate(self.parser.parse(expr))
            results.append(r)
            self.history.add(expr, str(r), "standard")
        self.assertEqual(len(self.history.get_all()), 3)


class TestPipelineUndoRedoDuringCalculation(unittest.TestCase):
    def setUp(self):
        self.undo_redo = UndoRedoManager()

    def test_undo_last_action(self):
        state = {"value": 0}

        def set_val(x):
            old = state["value"]
            state["value"] = x
            return old

        def unset_val(x):
            state["value"] = x

        self.undo_redo.execute(set_val, unset_val, 42)
        self.assertEqual(state["value"], 42)
        self.undo_redo.undo()
        self.assertEqual(state["value"], 42)

    def test_undo_redo_cycle(self):
        state = {"value": 0}
        actions = []

        def do(x):
            old = state["value"]
            state["value"] = x
            actions.append(("do", x))
            return old

        def undo(x):
            state["value"] = x
            actions.append(("undo", x))

        self.undo_redo.execute(do, undo, 10)
        self.assertEqual(state["value"], 10)
        self.undo_redo.undo()
        self.assertTrue(self.undo_redo.can_redo())
        self.undo_redo.redo()
        self.assertEqual(state["value"], 10)

    def test_undo_when_nothing_to_undo(self):
        result = self.undo_redo.undo()
        self.assertFalse(result)

    def test_clear_undo_redo(self):
        state = {"value": 0}
        self.undo_redo.execute(lambda x: state.update(value=x), lambda x: state.update(value=x), 1)
        self.undo_redo.clear()
        self.assertFalse(self.undo_redo.can_undo())
