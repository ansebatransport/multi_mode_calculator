import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.random_generator import RandomGenerator


class TestRandomGenerator(unittest.TestCase):
    def test_integer_in_range(self):
        for _ in range(50):
            val = RandomGenerator.integer(1, 10)
            self.assertGreaterEqual(val, 1)
            self.assertLessEqual(val, 10)

    def test_integer_same_min_max(self):
        self.assertEqual(RandomGenerator.integer(5, 5), 5)

    def test_uniform_in_range(self):
        for _ in range(50):
            val = RandomGenerator.uniform(2.5, 7.5)
            self.assertGreaterEqual(val, 2.5)
            self.assertLessEqual(val, 7.5)

    def test_normal_sample(self):
        for _ in range(50):
            val = RandomGenerator.normal(0, 1)
            self.assertIsInstance(val, float)

    def test_random_from_list(self):
        items = [10, 20, 30, 40, 50]
        for _ in range(50):
            val = RandomGenerator.sample(items, 1)[0]
            self.assertIn(val, items)

    def test_unique_random_values(self):
        items = list(range(20))
        result = RandomGenerator.sample(items, 5)
        self.assertEqual(len(result), 5)
        self.assertEqual(len(set(result)), 5)

    def test_seed_reproducibility(self):
        RandomGenerator.set_seed(42)
        a = [RandomGenerator.integer(1, 100) for _ in range(10)]
        RandomGenerator.set_seed(42)
        b = [RandomGenerator.integer(1, 100) for _ in range(10)]
        self.assertEqual(a, b)

    def test_range_validation_min_greater_than_max(self):
        with self.assertRaises(ValueError):
            RandomGenerator.integer(10, 1)

    def test_range_validation_uniform(self):
        with self.assertRaises(ValueError):
            RandomGenerator.uniform(10.0, 1.0)

    def test_sample_too_large(self):
        with self.assertRaises(ValueError):
            RandomGenerator.sample([1, 2], 5)

    def test_negative_normal_sigma(self):
        with self.assertRaises(ValueError):
            RandomGenerator.normal(0, -1)

    def test_exponential(self):
        for _ in range(50):
            val = RandomGenerator.exponential(1.0)
            self.assertGreater(val, 0)

    def test_exponential_invalid_lambda(self):
        with self.assertRaises(ValueError):
            RandomGenerator.exponential(0)

    def test_shuffle(self):
        items = [1, 2, 3, 4, 5]
        result = RandomGenerator.shuffle(items)
        self.assertEqual(sorted(result), sorted(items))

    def test_shuffle_does_not_modify_original(self):
        items = [1, 2, 3, 4, 5]
        original = items[:]
        RandomGenerator.shuffle(items)
        self.assertEqual(items, original)

    def test_beta(self):
        val = RandomGenerator.beta(2, 5)
        self.assertGreaterEqual(val, 0)
        self.assertLessEqual(val, 1)

    def test_beta_invalid(self):
        with self.assertRaises(ValueError):
            RandomGenerator.beta(0, 5)


if __name__ == "__main__":
    unittest.main()
