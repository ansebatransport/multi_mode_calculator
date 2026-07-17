import sys
import os
import unittest
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.engine import ExpressionEvaluator
from core.expression_parser import ShuntingYardParser, Token, TokenType


class TestExpressionEvaluator(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()
        self.evaluator = ExpressionEvaluator(angle_mode="degrees")

    def _eval(self, expression, angle_mode="degrees"):
        evaluator = ExpressionEvaluator(angle_mode=angle_mode)
        tokens = self.parser.parse(expression)
        return evaluator.evaluate(tokens)

    def test_basic_addition(self):
        self.assertEqual(self._eval("2+3"), 5.0)

    def test_basic_multiplication(self):
        self.assertEqual(self._eval("2*3*4"), 24.0)

    def test_operator_precedence(self):
        self.assertEqual(self._eval("2+3*4"), 14.0)

    def test_parentheses_override_precedence(self):
        self.assertEqual(self._eval("(2+3)*4"), 20.0)

    def test_nested_parentheses(self):
        self.assertEqual(self._eval("((2+3)*(4-1))"), 15.0)

    def test_division(self):
        self.assertAlmostEqual(self._eval("10/4"), 2.5)

    def test_division_by_zero(self):
        with self.assertRaises((ZeroDivisionError, ValueError)):
            self._eval("1/0")

    def test_trig_sin_degrees(self):
        self.assertAlmostEqual(self._eval("sin(30)"), 0.5, places=10)

    def test_trig_cos_degrees(self):
        self.assertAlmostEqual(self._eval("cos(60)"), 0.5, places=10)

    def test_trig_sin_radians(self):
        self.assertAlmostEqual(
            self._eval("sin(3.141592653589793/6)", angle_mode="radians"),
            0.5, places=10
        )

    def test_trig_asin_returns_degrees(self):
        result = self._eval("asin(0.5)")
        self.assertAlmostEqual(result, 30.0, places=10)

    def test_constant_pi(self):
        self.assertAlmostEqual(self._eval("π"), math.pi, places=10)

    def test_constant_e(self):
        self.assertAlmostEqual(self._eval("e"), math.e, places=10)

    def test_unary_minus(self):
        self.assertEqual(self._eval("-5"), -5.0)

    def test_unary_minus_in_expression(self):
        self.assertEqual(self._eval("-5+3"), -2.0)

    def test_power_operator(self):
        self.assertEqual(self._eval("2**3"), 8.0)

    def test_power_operator_caret(self):
        self.assertEqual(self._eval("2^3"), 8.0)

    def test_factorial(self):
        self.assertEqual(self._eval("5!"), 120.0)

    def test_factorial_zero(self):
        self.assertEqual(self._eval("0!"), 1.0)

    def test_modulo(self):
        self.assertEqual(self._eval("10%3"), 1.0)

    def test_sqrt(self):
        self.assertAlmostEqual(self._eval("sqrt(9)"), 3.0, places=10)

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            self.evaluator.quick_evaluate("")

    def test_unknown_token(self):
        with self.assertRaises(ValueError):
            tokens = [Token(TokenType.VARIABLE, "unknown_var")]
            self.evaluator.evaluate(tokens)

    def test_quick_evaluate_simple(self):
        self.assertEqual(self.evaluator.quick_evaluate("2+3"), 5.0)

    def test_angle_mode_setter(self):
        self.evaluator.angle_mode = "radians"
        self.assertEqual(self.evaluator.angle_mode, "radians")

    def test_invalid_angle_mode(self):
        with self.assertRaises(ValueError):
            self.evaluator.angle_mode = "invalid"

    def test_log10(self):
        self.assertAlmostEqual(self._eval("log(100)"), 2.0, places=10)

    def test_ln(self):
        self.assertAlmostEqual(self._eval("ln(e)"), 1.0, places=10)

    def test_abs(self):
        self.assertEqual(self._eval("abs(-5)"), 5.0)

    def test_floor(self):
        self.assertEqual(self._eval("floor(3.7)"), 3.0)

    def test_ceil(self):
        self.assertEqual(self._eval("ceil(3.2)"), 4.0)

    def test_multiple_operators(self):
        self.assertEqual(self._eval("1+2-3+4"), 4.0)

    def test_complex_expression(self):
        self.assertAlmostEqual(self._eval("2*sin(30)+1"), 2.0, places=10)


if __name__ == "__main__":
    unittest.main()
