import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import math
import unittest
from core.sequences import SequenceGenerator


class TestSequencesArithmetic(unittest.TestCase):
    def test_arithmetic_positive_diff(self):
        seq = SequenceGenerator.arithmetic(1, 2, 5)
        self.assertEqual(seq, [1, 3, 5, 7, 9])

    def test_arithmetic_negative_diff(self):
        seq = SequenceGenerator.arithmetic(10, -3, 4)
        self.assertEqual(seq, [10, 7, 4, 1])

    def test_arithmetic_single_term(self):
        seq = SequenceGenerator.arithmetic(5, 2, 1)
        self.assertEqual(seq, [5])

    def test_arithmetic_zero_diff(self):
        seq = SequenceGenerator.arithmetic(3, 0, 3)
        self.assertEqual(seq, [3, 3, 3])

    def test_arithmetic_n_terms_less_than_one(self):
        with self.assertRaises(ValueError):
            SequenceGenerator.arithmetic(1, 1, 0)


class TestSequencesGeometric(unittest.TestCase):
    def test_geometric_doubling(self):
        seq = SequenceGenerator.geometric(1, 2, 5)
        self.assertEqual(seq, [1, 2, 4, 8, 16])

    def test_geometric_fractional(self):
        seq = SequenceGenerator.geometric(16, 0.5, 4)
        self.assertEqual(seq, [16, 8, 4, 2])

    def test_geometric_negative_ratio(self):
        seq = SequenceGenerator.geometric(1, -2, 4)
        self.assertEqual(seq, [1, -2, 4, -8])

    def test_geometric_single_term(self):
        seq = SequenceGenerator.geometric(7, 3, 1)
        self.assertEqual(seq, [7])

    def test_geometric_n_terms_less_than_one(self):
        with self.assertRaises(ValueError):
            SequenceGenerator.geometric(1, 2, 0)


class TestSequencesFibonacci(unittest.TestCase):
    def test_fibonacci_first_ten(self):
        seq = SequenceGenerator.fibonacci(10)
        self.assertEqual(seq, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_fibonacci_one_term(self):
        seq = SequenceGenerator.fibonacci(1)
        self.assertEqual(seq, [0])

    def test_fibonacci_two_terms(self):
        seq = SequenceGenerator.fibonacci(2)
        self.assertEqual(seq, [0, 1])

    def test_fibonacci_n_terms_less_than_one(self):
        with self.assertRaises(ValueError):
            SequenceGenerator.fibonacci(0)


class TestSequencesCustom(unittest.TestCase):
    def test_custom_doubling(self):
        seq = SequenceGenerator.custom(1, lambda prev, i: prev * 2, 5)
        self.assertEqual(seq, [1, 2, 4, 8, 16])

    def test_custom_increment_by_index(self):
        seq = SequenceGenerator.custom(0, lambda prev, i: prev + i, 5)
        self.assertEqual(seq, [0, 1, 3, 6, 10])

    def test_custom_single_term(self):
        seq = SequenceGenerator.custom(42, lambda prev, i: prev, 1)
        self.assertEqual(seq, [42])

    def test_custom_n_terms_less_than_one(self):
        with self.assertRaises(ValueError):
            SequenceGenerator.custom(1, lambda p, i: p, 0)


class TestSequencesSums(unittest.TestCase):
    def test_sum_arithmetic(self):
        total = SequenceGenerator.sum_arithmetic(1, 1, 10)
        self.assertEqual(total, 55)

    def test_sum_geometric(self):
        total = SequenceGenerator.sum_geometric(1, 2, 4)
        self.assertEqual(total, 15)

    def test_sum_geometric_ratio_one(self):
        total = SequenceGenerator.sum_geometric(3, 1, 5)
        self.assertEqual(total, 15)

    def test_sum_geometric_fractional(self):
        total = SequenceGenerator.sum_geometric(100, 0.5, 3)
        self.assertAlmostEqual(total, 175.0)


class TestSequencesSpecial(unittest.TestCase):
    def test_factorial_sequence(self):
        seq = SequenceGenerator.factorial_sequence(5)
        self.assertEqual(seq, [1, 1, 2, 6, 24])

    def test_powers_of_two(self):
        seq = SequenceGenerator.powers_of_two(5)
        self.assertEqual(seq, [1, 2, 4, 8, 16])

    def test_triangular_numbers(self):
        seq = SequenceGenerator.triangular_numbers(5)
        self.assertEqual(seq, [1, 3, 6, 10, 15])
