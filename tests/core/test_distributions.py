import sys
import os
import math
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.distributions import DistributionCalculator


class TestDistributionCalculator(unittest.TestCase):
    def test_normal_pdf_standard(self):
        result = DistributionCalculator.normal_pdf(0, 0, 1)
        expected = 1 / math.sqrt(2 * math.pi)
        self.assertAlmostEqual(result, expected)

    def test_normal_pdf_shifted(self):
        result = DistributionCalculator.normal_pdf(2, 2, 1)
        expected = 1 / math.sqrt(2 * math.pi)
        self.assertAlmostEqual(result, expected)

    def test_normal_pdf_zero_sigma(self):
        with self.assertRaises(ValueError):
            DistributionCalculator.normal_pdf(0, 0, 0)

    def test_normal_cdf_standard(self):
        result = DistributionCalculator.normal_cdf(0, 0, 1)
        self.assertAlmostEqual(result, 0.5)

    def test_normal_cdf_negative_infinity(self):
        result = DistributionCalculator.normal_cdf(-100, 0, 1)
        self.assertAlmostEqual(result, 0.0, places=10)

    def test_normal_cdf_positive_infinity(self):
        result = DistributionCalculator.normal_cdf(100, 0, 1)
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_normal_cdf_symmetry(self):
        low = DistributionCalculator.normal_cdf(-1, 0, 1)
        high = DistributionCalculator.normal_cdf(1, 0, 1)
        self.assertAlmostEqual(low + high, 1.0)

    def test_binomial_pmf(self):
        result = DistributionCalculator.binomial_pmf(2, 4, 0.5)
        expected = math.comb(4, 2) * 0.5**2 * 0.5**2
        self.assertAlmostEqual(result, expected)

    def test_binomial_pmf_out_of_range(self):
        self.assertEqual(DistributionCalculator.binomial_pmf(-1, 5, 0.5), 0.0)
        self.assertEqual(DistributionCalculator.binomial_pmf(6, 5, 0.5), 0.0)

    def test_binomial_pmf_invalid_params(self):
        with self.assertRaises(ValueError):
            DistributionCalculator.binomial_pmf(2, -1, 0.5)
        with self.assertRaises(ValueError):
            DistributionCalculator.binomial_pmf(2, 5, 1.5)

    def test_binomial_mean(self):
        self.assertAlmostEqual(DistributionCalculator.binomial_mean(10, 0.5), 5.0)

    def test_binomial_variance(self):
        self.assertAlmostEqual(DistributionCalculator.binomial_variance(10, 0.5), 2.5)

    def test_poisson_pmf(self):
        result = DistributionCalculator.poisson_pmf(2, 3)
        expected = (3**2) * math.exp(-3) / math.factorial(2)
        self.assertAlmostEqual(result, expected)

    def test_poisson_pmf_negative_k(self):
        self.assertEqual(DistributionCalculator.poisson_pmf(-1, 3), 0.0)

    def test_poisson_pmf_invalid_lambda(self):
        with self.assertRaises(ValueError):
            DistributionCalculator.poisson_pmf(2, 0)
        with self.assertRaises(ValueError):
            DistributionCalculator.poisson_pmf(2, -1)

    def test_poisson_mean(self):
        self.assertEqual(DistributionCalculator.poisson_mean(5), 5)

    def test_poisson_variance(self):
        self.assertEqual(DistributionCalculator.poisson_variance(5), 5)

    def test_uniform_pdf_in_range(self):
        self.assertAlmostEqual(DistributionCalculator.uniform_pdf(0.5, 0, 1), 1.0)

    def test_uniform_pdf_out_of_range(self):
        self.assertEqual(DistributionCalculator.uniform_pdf(2, 0, 1), 0.0)
        self.assertEqual(DistributionCalculator.uniform_pdf(-1, 0, 1), 0.0)

    def test_uniform_pdf_invalid_range(self):
        with self.assertRaises(ValueError):
            DistributionCalculator.uniform_pdf(0.5, 1, 1)

    def test_uniform_cdf(self):
        self.assertAlmostEqual(DistributionCalculator.uniform_cdf(0.5, 0, 1), 0.5)
        self.assertAlmostEqual(DistributionCalculator.uniform_cdf(0, 0, 1), 0.0)
        self.assertAlmostEqual(DistributionCalculator.uniform_cdf(1, 0, 1), 1.0)

    def test_uniform_cdf_below(self):
        self.assertAlmostEqual(DistributionCalculator.uniform_cdf(-1, 0, 1), 0.0)

    def test_uniform_cdf_above(self):
        self.assertAlmostEqual(DistributionCalculator.uniform_cdf(2, 0, 1), 1.0)


if __name__ == "__main__":
    unittest.main()
