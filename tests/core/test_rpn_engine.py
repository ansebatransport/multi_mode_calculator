import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.rpn_engine import RPNEngine


class TestRPNEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RPNEngine()

    def test_push_and_peek(self):
        self.engine.push(42)
        self.assertEqual(self.engine.peek(), 42)
        self.assertEqual(self.engine.get_stack(), [42])

    def test_push_multiple(self):
        self.engine.push(1)
        self.engine.push(2)
        self.engine.push(3)
        self.assertEqual(self.engine.get_stack(), [1, 2, 3])

    def test_execute_add(self):
        self.engine.push(3)
        self.engine.push(4)
        self.engine.execute("+")
        self.assertEqual(self.engine.peek(), 7)

    def test_execute_subtract(self):
        self.engine.push(10)
        self.engine.push(3)
        self.engine.execute("-")
        self.assertEqual(self.engine.peek(), 7)

    def test_execute_multiply(self):
        self.engine.push(5)
        self.engine.push(6)
        self.engine.execute("*")
        self.assertEqual(self.engine.peek(), 30)

    def test_execute_divide(self):
        self.engine.push(10)
        self.engine.push(4)
        self.engine.execute("/")
        self.assertEqual(self.engine.peek(), 2.5)

    def test_execute_power(self):
        self.engine.push(2)
        self.engine.push(10)
        self.engine.execute("**")
        self.assertEqual(self.engine.peek(), 1024)

    def test_execute_modulo(self):
        self.engine.push(10)
        self.engine.push(3)
        self.engine.execute("%")
        self.assertEqual(self.engine.peek(), 1)

    def test_dup(self):
        self.engine.push(5)
        self.engine.dup()
        self.assertEqual(self.engine.get_stack(), [5, 5])

    def test_dup_empty_stack(self):
        with self.assertRaises(ValueError):
            self.engine.dup()

    def test_swap(self):
        self.engine.push(1)
        self.engine.push(2)
        self.engine.swap()
        self.assertEqual(self.engine.get_stack(), [2, 1])

    def test_swap_not_enough(self):
        self.engine.push(1)
        with self.assertRaises(ValueError):
            self.engine.swap()

    def test_drop(self):
        self.engine.push(1)
        self.engine.push(2)
        self.engine.drop()
        self.assertEqual(self.engine.get_stack(), [1])

    def test_drop_empty(self):
        with self.assertRaises(ValueError):
            self.engine.drop()

    def test_rot(self):
        self.engine.push(1)
        self.engine.push(2)
        self.engine.push(3)
        self.engine.rot()
        self.assertEqual(self.engine.get_stack(), [2, 3, 1])

    def test_rot_not_enough(self):
        self.engine.push(1)
        self.engine.push(2)
        with self.assertRaises(ValueError):
            self.engine.rot()

    def test_clear(self):
        self.engine.push(1)
        self.engine.push(2)
        self.engine.clear()
        self.assertEqual(self.engine.get_stack(), [])

    def test_evaluate_rpn_simple(self):
        result = self.engine.evaluate_rpn("3 4 +")
        self.assertEqual(result, 7)

    def test_evaluate_rpn_complex(self):
        result = self.engine.evaluate_rpn("5 1 2 + 4 * + 3 -")
        self.assertEqual(result, 14)

    def test_evaluate_rpn_single_number(self):
        result = self.engine.evaluate_rpn("42")
        self.assertEqual(result, 42)

    def test_evaluate_rpn_with_dup(self):
        result = self.engine.evaluate_rpn("5 dup *")
        self.assertEqual(result, 25)

    def test_evaluate_rpn_with_swap(self):
        result = self.engine.evaluate_rpn("3 8 swap -")
        self.assertEqual(result, 5)

    def test_evaluate_rpn_with_drop(self):
        result = self.engine.evaluate_rpn("1 2 3 drop +")
        self.assertEqual(result, 3)

    def test_evaluate_rpn_with_clear(self):
        result = self.engine.evaluate_rpn("5 3 clear 7")
        self.assertEqual(result, 7)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.engine.evaluate_rpn("5 0 /")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate_rpn("5 +")

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate_rpn("")

    def test_unknown_operator(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate_rpn("5 3 @")

    def test_execute_push_number(self):
        self.engine.execute("3.14")
        self.assertEqual(self.engine.peek(), 3.14)


if __name__ == "__main__":
    unittest.main()
