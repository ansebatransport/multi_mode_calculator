import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.validators import InputValidator


class TestValidatorsNumberInput(unittest.TestCase):
    def test_valid_integer(self):
        self.assertTrue(InputValidator.validate_number_input("42"))

    def test_valid_decimal(self):
        self.assertTrue(InputValidator.validate_number_input("3.14"))

    def test_valid_negative(self):
        self.assertTrue(InputValidator.validate_number_input("-5"))

    def test_invalid_letters(self):
        self.assertFalse(InputValidator.validate_number_input("abc"))

    def test_invalid_symbols(self):
        self.assertFalse(InputValidator.validate_number_input("1+2"))

    def test_empty_string(self):
        self.assertTrue(InputValidator.validate_number_input(""))

    def test_no_negative_when_disallowed(self):
        self.assertFalse(InputValidator.validate_number_input("-3", allow_negative=False))


class TestValidatorsExpression(unittest.TestCase):
    def test_valid_expression(self):
        valid, msg = InputValidator.validate_expression("2 + 3")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_balanced_parens(self):
        valid, msg = InputValidator.validate_expression("(2 + 3) * 4")
        self.assertTrue(valid)

    def test_unmatched_open_paren(self):
        valid, msg = InputValidator.validate_expression("(2 + 3")
        self.assertFalse(valid)
        self.assertIn("opening", msg)

    def test_unmatched_close_paren(self):
        valid, msg = InputValidator.validate_expression("2 + 3)")
        self.assertFalse(valid)
        self.assertIn("closing", msg)

    def test_consecutive_operators(self):
        valid, msg = InputValidator.validate_expression("2 ++ 3")
        self.assertFalse(valid)
        self.assertIn("Consecutive", msg)

    def test_empty_expr(self):
        valid, msg = InputValidator.validate_expression("")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

    def test_nested_parens(self):
        valid, msg = InputValidator.validate_expression("((1 + 2) * 3)")
        self.assertTrue(valid)


class TestValidatorsBaseInput(unittest.TestCase):
    def test_valid_hex(self):
        self.assertTrue(InputValidator.validate_hex_input("1A2F"))

    def test_invalid_hex(self):
        self.assertFalse(InputValidator.validate_hex_input("1G2Z"))

    def test_valid_octal(self):
        self.assertTrue(InputValidator.validate_oct_input("755"))

    def test_invalid_octal(self):
        self.assertFalse(InputValidator.validate_oct_input("789"))

    def test_valid_binary(self):
        self.assertTrue(InputValidator.validate_bin_input("1010"))

    def test_invalid_binary(self):
        self.assertFalse(InputValidator.validate_bin_input("102"))

    def test_base_specific_valid(self):
        self.assertTrue(InputValidator.validate_base_input("123", 10))

    def test_base_specific_invalid(self):
        self.assertFalse(InputValidator.validate_base_input("89", 8))


class TestValidatorsGraphExpression(unittest.TestCase):
    def test_valid_graph_expr(self):
        valid, msg = InputValidator.validate_graph_expression("x^2")
        self.assertTrue(valid)

    def test_valid_graph_expr_power(self):
        valid, msg = InputValidator.validate_graph_expression("x^2 + 3*x")
        self.assertTrue(valid)

    def test_graph_expr_empty(self):
        valid, msg = InputValidator.validate_graph_expression("")
        self.assertFalse(valid)
        self.assertIn("empty", msg.lower())

    def test_graph_expr_no_x(self):
        valid, msg = InputValidator.validate_graph_expression("42")
        self.assertFalse(valid)
        self.assertIn("contain 'x'", msg)

    def test_graph_expr_contains_x(self):
        valid, msg = InputValidator.validate_graph_expression("sin(x)")
        self.assertTrue(valid)


class TestValidatorsVariableName(unittest.TestCase):
    def test_valid_name(self):
        valid, msg = InputValidator.validate_variable_name("myVar")
        self.assertTrue(valid)

    def test_invalid_start_digit(self):
        valid, msg = InputValidator.validate_variable_name("1var")
        self.assertFalse(valid)

    def test_empty_name(self):
        valid, msg = InputValidator.validate_variable_name("")
        self.assertFalse(valid)

    def test_reserved_name(self):
        valid, msg = InputValidator.validate_variable_name("sin")
        self.assertFalse(valid)

    def test_underscore_start(self):
        valid, msg = InputValidator.validate_variable_name("_tmp")
        self.assertTrue(valid)


class TestValidatorsHelpers(unittest.TestCase):
    def test_sanitize_multiplication(self):
        result = InputValidator.sanitize_expression("2×3")
        self.assertEqual(result, "2*3")

    def test_sanitize_division(self):
        result = InputValidator.sanitize_expression("6÷3")
        self.assertEqual(result, "6/3")

    def test_sanitize_minus(self):
        result = InputValidator.sanitize_expression("2−3")
        self.assertEqual(result, "2-3")

    def test_sanitize_mixed(self):
        result = InputValidator.sanitize_expression("2×3÷4−5")
        self.assertEqual(result, "2*3/4-5")

    def test_validate_financial_input_none(self):
        valid, msg = InputValidator.validate_financial_input(None, "rate")
        self.assertFalse(valid)
        self.assertIn("rate", msg)
