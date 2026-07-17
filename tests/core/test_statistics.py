import sys
import os
import unittest
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.statistics import Statistics


class TestStatistics(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(Statistics.mean([1, 2, 3, 4, 5]), 3.0)

    def test_mean_single(self):
        self.assertEqual(Statistics.mean([10]), 10.0)

    def test_mean_floats(self):
        self.assertAlmostEqual(Statistics.mean([1.5, 2.5, 3.0]), 7.0 / 3)

    def test_median_odd(self):
        self.assertEqual(Statistics.median([3, 1, 2]), 2)

    def test_median_even(self):
        self.assertEqual(Statistics.median([1, 2, 3, 4]), 2.5)

    def test_median_single(self):
        self.assertEqual(Statistics.median([7]), 7)

    def test_mode_single(self):
        self.assertEqual(Statistics.mode([1, 2, 2, 3]), [2])

    def test_mode_multiple(self):
        result = Statistics.mode([1, 1, 2, 2, 3])
        self.assertEqual(result, [1, 2])

    def test_mode_all_same(self):
        result = Statistics.mode([5, 5, 5])
        self.assertEqual(result, [5])

    def test_std_dev_population(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = Statistics.std_dev(data, population=True)
        self.assertAlmostEqual(result, 2.0, places=5)

    def test_std_dev_sample(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = Statistics.std_dev(data, population=False)
        self.assertAlmostEqual(result, 2.138089935299395, places=10)

    def test_variance_population(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = Statistics.variance(data, population=True)
        self.assertAlmostEqual(result, 4.0, places=5)

    def test_variance_sample(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = Statistics.variance(data, population=False)
        self.assertAlmostEqual(result, 4.0 * 8 / 7, places=5)

    def test_variance_single_sample(self):
        with self.assertRaises(ValueError):
            Statistics.variance([5], population=False)

    def test_variance_single_population(self):
        self.assertEqual(Statistics.variance([5], population=True), 0.0)

    def test_percentile_50(self):
        data = list(range(1, 101))
        self.assertAlmostEqual(Statistics.percentile(data, 50), 50.5, places=5)

    def test_percentile_0(self):
        data = [10, 20, 30]
        self.assertEqual(Statistics.percentile(data, 0), 10)

    def test_percentile_100(self):
        data = [10, 20, 30]
        self.assertEqual(Statistics.percentile(data, 100), 30)

    def test_percentile_invalid(self):
        with self.assertRaises(ValueError):
            Statistics.percentile([1, 2, 3], 101)

    def test_quartile_q1(self):
        data = list(range(1, 101))
        q1 = Statistics.quartile_q1(data)
        self.assertAlmostEqual(q1, 25.75, places=2)

    def test_quartile_q3(self):
        data = list(range(1, 101))
        q3 = Statistics.quartile_q3(data)
        self.assertAlmostEqual(q3, 75.25, places=2)

    def test_iqr(self):
        data = list(range(1, 101))
        iqr = Statistics.iqr(data)
        self.assertGreater(iqr, 0)

    def test_all_stats(self):
        data = [1, 2, 3, 4, 5]
        result = Statistics.all_stats(data)
        self.assertIn("mean", result)
        self.assertIn("median", result)
        self.assertIn("mode", result)
        self.assertIn("std_dev", result)
        self.assertIn("variance", result)
        self.assertIn("sum", result)
        self.assertIn("count", result)
        self.assertIn("minimum", result)
        self.assertIn("maximum", result)
        self.assertIn("range", result)
        self.assertIn("q1", result)
        self.assertIn("q3", result)
        self.assertIn("iqr", result)
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["median"], 3.0)
        self.assertEqual(result["count"], 5)
        self.assertEqual(result["minimum"], 1)
        self.assertEqual(result["maximum"], 5)
        self.assertEqual(result["range"], 4)

    def test_sum(self):
        self.assertEqual(Statistics.sum([1, 2, 3, 4, 5]), 15)

    def test_count(self):
        self.assertEqual(Statistics.count([1, 2, 3]), 3)

    def test_minimum(self):
        self.assertEqual(Statistics.minimum([5, 3, 1, 4, 2]), 1)

    def test_maximum(self):
        self.assertEqual(Statistics.maximum([5, 3, 1, 4, 2]), 5)

    def test_range_val(self):
        self.assertEqual(Statistics.range_val([1, 5, 3]), 4)

    def test_empty_data_raises(self):
        with self.assertRaises(ValueError):
            Statistics.mean([])
        with self.assertRaises(ValueError):
            Statistics.median([])
        with self.assertRaises(ValueError):
            Statistics.mode([])
        with self.assertRaises(ValueError):
            Statistics.variance([])


if __name__ == "__main__":
    unittest.main()
