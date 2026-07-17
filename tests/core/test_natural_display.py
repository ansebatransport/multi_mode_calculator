import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.natural_display import NaturalDisplay


class TestNaturalDisplayFormatFraction(unittest.TestCase):
    def test_format_fraction_basic(self):
        result = NaturalDisplay.format_fraction(2, 3)
        self.assertEqual(result["type"], "fraction")
        self.assertEqual(result["numerator"], "2")
        self.assertEqual(result["denominator"], "3")
        self.assertEqual(result["display"], "2/3")

    def test_format_fraction_one(self):
        result = NaturalDisplay.format_fraction(5, 1)
        self.assertEqual(result["display"], "5/1")


class TestNaturalDisplayFormatRoot(unittest.TestCase):
    def test_format_sqrt(self):
        result = NaturalDisplay.format_root("4")
        self.assertEqual(result["type"], "root")
        self.assertEqual(result["index"], 2)
        self.assertEqual(result["display"], "\u221a(4)")

    def test_format_cuberoot(self):
        result = NaturalDisplay.format_root("27", 3)
        self.assertEqual(result["index"], 3)
        self.assertEqual(result["display"], "\u221b(27)")

    def test_format_custom_root(self):
        result = NaturalDisplay.format_root("x", 4)
        self.assertEqual(result["display"], "4\u221a(x)")


class TestNaturalDisplayFormatPower(unittest.TestCase):
    def test_format_power_simple(self):
        result = NaturalDisplay.format_power("x", "2")
        self.assertEqual(result["type"], "power")
        self.assertEqual(result["display"], "x^2")

    def test_format_power_negative(self):
        result = NaturalDisplay.format_power("x", "-1")
        self.assertEqual(result["display"], "x^-1")


class TestNaturalDisplayFormatSubscript(unittest.TestCase):
    def test_format_subscript(self):
        result = NaturalDisplay.format_subscript("a", "n")
        self.assertEqual(result["type"], "subscript")
        self.assertEqual(result["display"], "a_n")


class TestNaturalDisplayFormatLog(unittest.TestCase):
    def test_format_base10(self):
        result = NaturalDisplay.format_log("10", "100")
        self.assertEqual(result["display"], "log\u2081\u2080(100)")

    def test_format_natural_log(self):
        result = NaturalDisplay.format_log("e", "x")
        self.assertEqual(result["display"], "ln(x)")

    def test_format_custom_base(self):
        result = NaturalDisplay.format_log("2", "8")
        self.assertEqual(result["display"], "log_2(8)")


class TestNaturalDisplayToUnicode(unittest.TestCase):
    def test_simple_expression(self):
        result = NaturalDisplay.to_unicode("2+3")
        self.assertEqual(result, "2+3")

    def test_superscript(self):
        result = NaturalDisplay.to_unicode("x^2")
        self.assertIn("\u00b2", result)

    def test_subscript(self):
        result = NaturalDisplay.to_unicode("a_1")
        self.assertIn("\u2081", result)

    def test_superscript_multi_digit(self):
        result = NaturalDisplay.to_unicode("^12")
        self.assertIn("\u00b9\u00b2", result)

    def test_no_special_chars(self):
        result = NaturalDisplay.to_unicode("hello")
        self.assertEqual(result, "hello")

    def test_empty_string(self):
        result = NaturalDisplay.to_unicode("")
        self.assertEqual(result, "")
