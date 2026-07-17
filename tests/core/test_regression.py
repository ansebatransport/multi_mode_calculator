import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.regression import RegressionAnalyzer


class TestRegressionAnalyzer(unittest.TestCase):
    def test_linear_known_data(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = RegressionAnalyzer.linear(x, y)
        self.assertAlmostEqual(result["slope"], 2.0)
        self.assertAlmostEqual(result["intercept"], 0.0)
        self.assertAlmostEqual(result["r_squared"], 1.0)

    def test_linear_with_intercept(self):
        x = [0, 1, 2, 3, 4]
        y = [1, 3, 5, 7, 9]
        result = RegressionAnalyzer.linear(x, y)
        self.assertAlmostEqual(result["slope"], 2.0)
        self.assertAlmostEqual(result["intercept"], 1.0)

    def test_linear_imperfect_data(self):
        x = [1, 2, 3, 4, 5]
        y = [2.1, 3.9, 6.2, 7.8, 10.1]
        result = RegressionAnalyzer.linear(x, y)
        self.assertAlmostEqual(result["slope"], 2.0, places=0)
        self.assertGreater(result["r_squared"], 0.98)

    def test_linear_r_squared_perfect(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = RegressionAnalyzer.linear(x, y)
        self.assertAlmostEqual(result["r_squared"], 1.0)

    def test_predict_linear(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        coefficients = RegressionAnalyzer.linear(x, y)
        self.assertAlmostEqual(RegressionAnalyzer.predict(6, coefficients), 12.0)

    def test_predict_quadratic(self):
        coefficients = {"a": 1.0, "b": 0.0, "c": 0.0}
        self.assertAlmostEqual(RegressionAnalyzer.predict(3, coefficients), 9.0)

    def test_quadratic(self):
        x = [0, 1, 2, 3, 4]
        y = [0, 1, 4, 9, 16]
        result = RegressionAnalyzer.quadratic(x, y)
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("r_squared", result)
        self.assertIn("equation", result)

    def test_r_squared(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        r2 = RegressionAnalyzer.r_squared(x, y, lambda xi: 2 * xi)
        self.assertAlmostEqual(r2, 1.0)

    def test_empty_data(self):
        with self.assertRaises(ValueError):
            RegressionAnalyzer.linear([], [])

    def test_single_point(self):
        with self.assertRaises(ValueError):
            RegressionAnalyzer.linear([1], [2])

    def test_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            RegressionAnalyzer.linear([1, 2, 3], [1, 2])

    def test_predict_unknown_format(self):
        with self.assertRaises(ValueError):
            RegressionAnalyzer.predict(1, {"unknown": 1})


if __name__ == "__main__":
    unittest.main()
