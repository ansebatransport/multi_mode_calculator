import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.recurring_decimal import RecurringDecimal


class TestRecurringDecimalDetect(unittest.TestCase):
    def test_one_third(self):
        result = RecurringDecimal.detect(1/3)
        self.assertTrue(result["is_recurring"])
        self.assertIn("3", result["repeating"])

    def test_two_thirds(self):
        result = RecurringDecimal.detect(2/3)
        self.assertTrue(result["is_recurring"])
        self.assertIn("6", result["repeating"])

    def test_detect_returns_dict_with_keys(self):
        result = RecurringDecimal.detect(0.14285714285714285)
        self.assertIn("is_recurring", result)
        self.assertIn("notation", result)
        self.assertIn("non_repeating", result)
        self.assertIn("repeating", result)
        self.assertIsInstance(result["notation"], str)

    def test_terminating_decimal(self):
        result = RecurringDecimal.detect(0.5)
        self.assertFalse(result["is_recurring"])

    def test_zero(self):
        result = RecurringDecimal.detect(0.0)
        self.assertFalse(result["is_recurring"])

    def test_one_sixth(self):
        result = RecurringDecimal.detect(1/6)
        self.assertTrue(result["is_recurring"])

    def test_one_ninth(self):
        result = RecurringDecimal.detect(1/9)
        self.assertTrue(result["is_recurring"])


class TestRecurringDecimalFractionToRecurring(unittest.TestCase):
    def test_one_third(self):
        result = RecurringDecimal.fraction_to_recurring(1, 3)
        self.assertEqual(result, "0.(3)")

    def test_two_thirds(self):
        result = RecurringDecimal.fraction_to_recurring(2, 3)
        self.assertEqual(result, "0.(6)")

    def test_one_sixth(self):
        result = RecurringDecimal.fraction_to_recurring(1, 6)
        self.assertIn("0.", result)
        self.assertIn("(6)", result)

    def test_one_seventh(self):
        result = RecurringDecimal.fraction_to_recurring(1, 7)
        self.assertIn("0.", result)
        self.assertIn("(", result)

    def test_one_ninth(self):
        result = RecurringDecimal.fraction_to_recurring(1, 9)
        self.assertEqual(result, "0.(1)")

    def test_five_ninths(self):
        result = RecurringDecimal.fraction_to_recurring(5, 9)
        self.assertEqual(result, "0.(5)")

    def test_one_whole(self):
        result = RecurringDecimal.fraction_to_recurring(1, 1)
        self.assertEqual(result, "1")

    def test_zero_numerator(self):
        result = RecurringDecimal.fraction_to_recurring(0, 5)
        self.assertEqual(result, "0")

    def test_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            RecurringDecimal.fraction_to_recurring(1, 0)

    def test_negative(self):
        result = RecurringDecimal.fraction_to_recurring(-1, 3)
        self.assertEqual(result, "-0.(3)")

    def test_mixed_number(self):
        result = RecurringDecimal.fraction_to_recurring(7, 3)
        self.assertIn("2.", result)

    def test_one_half(self):
        result = RecurringDecimal.fraction_to_recurring(1, 2)
        self.assertEqual(result, "0.5")


class TestRecurringDecimalAddition(unittest.TestCase):
    def test_add_recurring(self):
        a = RecurringDecimal.fraction_to_recurring(1, 3)
        b = RecurringDecimal.fraction_to_recurring(2, 3)
        self.assertEqual(a, "0.(3)")
        self.assertEqual(b, "0.(6)")

    def test_one_third_plus_one_sixth(self):
        from core.fractions import FractionHelper
        n, d = FractionHelper.add(1, 3, 1, 6)
        self.assertEqual(n, 1)
        self.assertEqual(d, 2)


class TestRecurringDecimalConvertToFloat(unittest.TestCase):
    def test_one_third(self):
        result = RecurringDecimal.fraction_to_recurring(1, 3)
        self.assertEqual(result, "0.(3)")
        self.assertAlmostEqual(float(result.replace(".", "").replace("(", "").replace(")", "")) / 10, 0.333, places=1)

    def test_one_ninth(self):
        result = RecurringDecimal.fraction_to_recurring(1, 9)
        self.assertEqual(result, "0.(1)")


class TestRecurringDecimalStringRepresentation(unittest.TestCase):
    def test_format_recurring(self):
        result = RecurringDecimal.format_recurring("0.", "3")
        self.assertEqual(result, "0.(3)")

    def test_format_recurring_long(self):
        result = RecurringDecimal.format_recurring("0.", "142857")
        self.assertEqual(result, "0.(142857)")

    def test_format_recurring_with_non_repeating(self):
        result = RecurringDecimal.format_recurring("0.1", "6")
        self.assertEqual(result, "0.1(6)")

    def test_fraction_to_recurring_format(self):
        result = RecurringDecimal.fraction_to_recurring(1, 3)
        self.assertEqual(result, "0.(3)")

    def test_fraction_to_recurring_with_non_repeating(self):
        result = RecurringDecimal.fraction_to_recurring(1, 6)
        self.assertTrue(result.startswith("0."))


class TestRecurringDecimalEdgeCases(unittest.TestCase):
    def test_very_large_numerator(self):
        result = RecurringDecimal.fraction_to_recurring(1000000, 3)
        self.assertIn(".", result)
        self.assertIn("(3)", result)

    def test_one(self):
        result = RecurringDecimal.fraction_to_recurring(1, 1)
        self.assertEqual(result, "1")

    def test_negative_zero(self):
        result = RecurringDecimal.fraction_to_recurring(0, 1)
        self.assertEqual(result, "0")


if __name__ == "__main__":
    unittest.main()
