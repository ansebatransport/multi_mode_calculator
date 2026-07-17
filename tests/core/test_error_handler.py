import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.error_handler import (
    ErrorType, CalculatorError, ErrorHandler, ERROR_MESSAGES
)


class TestErrorHandlerDivisionByZero(unittest.TestCase):
    def test_division_by_zero_error(self):
        error = ErrorHandler.handle_division_by_zero()
        self.assertIsInstance(error, CalculatorError)
        self.assertEqual(error.error_type, ErrorType.DIVISION_BY_ZERO)
        self.assertEqual(error.message, "Cannot divide by zero")


class TestErrorHandlerSyntaxError(unittest.TestCase):
    def test_invalid_expression_error(self):
        error = ErrorHandler.handle_invalid_expression("2++")
        self.assertEqual(error.error_type, ErrorType.INVALID_EXPRESSION)
        self.assertIn("2++", error.message)

    def test_invalid_expression_empty(self):
        error = ErrorHandler.handle_invalid_expression()
        self.assertEqual(error.error_type, ErrorType.INVALID_EXPRESSION)
        self.assertEqual(error.message, "Invalid expression")


class TestErrorHandlerOverflow(unittest.TestCase):
    def test_overflow_error(self):
        error = ErrorHandler.handle_overflow()
        self.assertEqual(error.error_type, ErrorType.OVERFLOW)
        self.assertEqual(error.message, "Number too large to display")


class TestErrorHandlerDomainError(unittest.TestCase):
    def test_domain_error(self):
        error = ErrorHandler.handle_domain_error("sqrt of negative")
        self.assertEqual(error.error_type, ErrorType.DOMAIN_ERROR)
        self.assertIn("sqrt of negative", error.message)


class TestErrorHandlerFormatError(unittest.TestCase):
    def test_format_calculator_error(self):
        error = CalculatorError(ErrorType.DIVISION_BY_ZERO)
        formatted = ErrorHandler.format_error(error)
        self.assertEqual(formatted, "⚠ Cannot divide by zero")

    def test_format_calculator_error_with_detail(self):
        error = CalculatorError(ErrorType.INVALID_EXPRESSION, "bad token")
        formatted = ErrorHandler.format_error(error)
        self.assertIn("bad token", formatted)


class TestErrorHandlerFormatForDisplay(unittest.TestCase):
    def test_format_calculator_error_display(self):
        error = CalculatorError(ErrorType.DIVISION_BY_ZERO)
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ Cannot divide by zero")

    def test_format_zero_division_error(self):
        error = ZeroDivisionError()
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ Cannot divide by zero")

    def test_format_value_error(self):
        error = ValueError("bad value")
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ bad value")

    def test_format_overflow_error(self):
        error = OverflowError()
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ Number too large")

    def test_format_type_error(self):
        error = TypeError()
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ Invalid operation")

    def test_format_generic_exception(self):
        error = RuntimeError("something broke")
        result = ErrorHandler.format_error_for_display(error)
        self.assertEqual(result, "⚠ Error: something broke")

    def test_format_generic_exception_truncated(self):
        error = RuntimeError("x" * 100)
        result = ErrorHandler.format_error_for_display(error)
        self.assertLessEqual(len(result), 65)


class TestErrorHandlerErrorTypes(unittest.TestCase):
    def test_all_error_types_have_messages(self):
        for error_type in ErrorType:
            self.assertIn(error_type, ERROR_MESSAGES)

    def test_messages_are_non_empty(self):
        for error_type, msg in ERROR_MESSAGES.items():
            self.assertTrue(len(msg) > 0, f"Empty message for {error_type}")


class TestErrorHandlerCalculatorException(unittest.TestCase):
    def test_exception_is_exception_subclass(self):
        self.assertTrue(issubclass(CalculatorError, Exception))

    def test_exception_str(self):
        error = CalculatorError(ErrorType.DIVISION_BY_ZERO)
        self.assertEqual(str(error), "Cannot divide by zero")

    def test_exception_str_with_detail(self):
        error = CalculatorError(ErrorType.DOMAIN_ERROR, "x must be >= 0")
        self.assertIn("x must be >= 0", str(error))
