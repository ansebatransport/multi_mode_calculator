import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.fractions import FractionHelper


class TestFractionSimplify(unittest.TestCase):
    def test_simplify_basic(self):
        self.assertEqual(FractionHelper.simplify(4, 8), (1, 2))

    def test_simplify_already_simplified(self):
        self.assertEqual(FractionHelper.simplify(3, 5), (3, 5))

    def test_simplify_zero_numerator(self):
        self.assertEqual(FractionHelper.simplify(0, 5), (0, 1))

    def test_simplify_negative_numerator(self):
        self.assertEqual(FractionHelper.simplify(-4, 8), (-1, 2))

    def test_simplify_negative_denominator(self):
        self.assertEqual(FractionHelper.simplify(4, -8), (-1, 2))

    def test_simplify_both_negative(self):
        self.assertEqual(FractionHelper.simplify(-4, -8), (1, 2))

    def test_simplify_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.simplify(1, 0)

    def test_simplify_large_values(self):
        self.assertEqual(FractionHelper.simplify(1000000, 2000000), (1, 2))


class TestFractionAdd(unittest.TestCase):
    def test_add_same_denominator(self):
        self.assertEqual(FractionHelper.add(1, 3, 1, 3), (2, 3))

    def test_add_different_denominators(self):
        self.assertEqual(FractionHelper.add(1, 4, 1, 3), (7, 12))

    def test_add_with_one(self):
        self.assertEqual(FractionHelper.add(1, 1, 1, 2), (3, 2))

    def test_add_zero(self):
        self.assertEqual(FractionHelper.add(3, 4, 0, 1), (3, 4))

    def test_add_negative(self):
        self.assertEqual(FractionHelper.add(1, 2, -1, 4), (1, 4))

    def test_add_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.add(1, 0, 1, 2)


class TestFractionSubtract(unittest.TestCase):
    def test_subtract_basic(self):
        self.assertEqual(FractionHelper.subtract(3, 4, 1, 4), (1, 2))

    def test_subtract_same(self):
        self.assertEqual(FractionHelper.subtract(2, 3, 2, 3), (0, 1))

    def test_subtract_result_negative(self):
        self.assertEqual(FractionHelper.subtract(1, 4, 3, 4), (-1, 2))

    def test_subtract_different_denominators(self):
        self.assertEqual(FractionHelper.subtract(3, 5, 1, 3), (4, 15))


class TestFractionMultiply(unittest.TestCase):
    def test_multiply_basic(self):
        self.assertEqual(FractionHelper.multiply(1, 2, 1, 3), (1, 6))

    def test_multiply_whole_numbers(self):
        self.assertEqual(FractionHelper.multiply(2, 1, 3, 1), (6, 1))

    def test_multiply_with_one(self):
        self.assertEqual(FractionHelper.multiply(3, 4, 1, 1), (3, 4))

    def test_multiply_with_zero(self):
        self.assertEqual(FractionHelper.multiply(3, 4, 0, 5), (0, 1))

    def test_multiply_negative(self):
        self.assertEqual(FractionHelper.multiply(1, 2, -1, 3), (-1, 6))


class TestFractionDivide(unittest.TestCase):
    def test_divide_basic(self):
        self.assertEqual(FractionHelper.divide(1, 2, 1, 3), (3, 2))

    def test_divide_same(self):
        self.assertEqual(FractionHelper.divide(3, 4, 3, 4), (1, 1))

    def test_divide_by_one(self):
        self.assertEqual(FractionHelper.divide(5, 7, 1, 1), (5, 7))

    def test_divide_zero_numerator(self):
        self.assertEqual(FractionHelper.divide(0, 5, 2, 3), (0, 1))

    def test_divide_by_zero_numerator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.divide(1, 2, 0, 3)

    def test_divide_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.divide(1, 2, 1, 0)


class TestFractionToDecimal(unittest.TestCase):
    def test_half(self):
        n, d = FractionHelper.decimal_to_fraction(0.5)
        self.assertEqual(n, 1)
        self.assertEqual(d, 2)

    def test_quarter(self):
        n, d = FractionHelper.decimal_to_fraction(0.25)
        self.assertEqual(n, 1)
        self.assertEqual(d, 4)

    def test_integer(self):
        n, d = FractionHelper.decimal_to_fraction(5.0)
        self.assertEqual(n, 5)
        self.assertEqual(d, 1)

    def test_negative(self):
        n, d = FractionHelper.decimal_to_fraction(-0.5)
        self.assertEqual(n, -1)
        self.assertEqual(d, 2)

    def test_zero(self):
        n, d = FractionHelper.decimal_to_fraction(0.0)
        self.assertEqual(n, 0)
        self.assertEqual(d, 1)

    def test_one_third_approx(self):
        n, d = FractionHelper.decimal_to_fraction(1/3)
        self.assertEqual(n, 1)
        self.assertEqual(d, 3)

    def test_two_thirds_approx(self):
        n, d = FractionHelper.decimal_to_fraction(2/3)
        self.assertEqual(n, 2)
        self.assertEqual(d, 3)


class TestFractionToMixed(unittest.TestCase):
    def test_proper_fraction(self):
        self.assertEqual(FractionHelper.to_mixed(3, 4), (0, 3, 4))

    def test_improper_fraction(self):
        self.assertEqual(FractionHelper.to_mixed(7, 4), (1, 3, 4))

    def test_exact_whole(self):
        self.assertEqual(FractionHelper.to_mixed(8, 4), (2, 0, 1))

    def test_zero_numerator(self):
        self.assertEqual(FractionHelper.to_mixed(0, 5), (0, 0, 1))

    def test_negative_fraction(self):
        result = FractionHelper.to_mixed(-7, 4)
        self.assertEqual(result, (-2, 3, 4))

    def test_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.to_mixed(1, 0)


class TestFractionFormatMixed(unittest.TestCase):
    def test_format_mixed_whole_only(self):
        self.assertEqual(FractionHelper.format_mixed(3, 0, 4), "3")

    def test_format_mixed_fraction_only(self):
        self.assertEqual(FractionHelper.format_mixed(0, 3, 4), "3/4")

    def test_format_mixed_both(self):
        self.assertEqual(FractionHelper.format_mixed(2, 3, 4), "2 3/4")

    def test_format_mixed_zero(self):
        self.assertEqual(FractionHelper.format_mixed(0, 0, 4), "0")

    def test_format_mixed_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.format_mixed(1, 2, 0)


class TestFractionFormatFraction(unittest.TestCase):
    def test_format_whole(self):
        self.assertEqual(FractionHelper.format_fraction(5, 1), "5")

    def test_format_fraction(self):
        self.assertEqual(FractionHelper.format_fraction(3, 4), "3/4")

    def test_format_negative(self):
        self.assertEqual(FractionHelper.format_fraction(-3, 4), "-3/4")

    def test_format_zero_denominator_raises(self):
        with self.assertRaises(ZeroDivisionError):
            FractionHelper.format_fraction(1, 0)


if __name__ == "__main__":
    unittest.main()
