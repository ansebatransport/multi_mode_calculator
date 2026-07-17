import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.date_calculator import DateCalculator


class TestDateCalculator(unittest.TestCase):
    def test_difference_days(self):
        result = DateCalculator.difference("2024-01-01", "2024-01-10")
        self.assertEqual(result["days"], 9)

    def test_difference_hours(self):
        result = DateCalculator.difference("2024-01-01", "2024-01-03")
        self.assertEqual(result["hours"], 48)

    def test_difference_weeks(self):
        result = DateCalculator.difference("2024-01-01", "2024-01-15")
        self.assertIn("2 weeks", result["weeks_days"])

    def test_add_days(self):
        result = DateCalculator.add_days("2024-01-01", 10)
        self.assertEqual(result, "2024-01-11")

    def test_add_days_cross_month(self):
        result = DateCalculator.add_days("2024-01-25", 10)
        self.assertEqual(result, "2024-02-04")

    def test_subtract_days(self):
        result = DateCalculator.subtract_days("2024-01-15", 5)
        self.assertEqual(result, "2024-01-10")

    def test_subtract_days_cross_month(self):
        result = DateCalculator.subtract_days("2024-02-05", 10)
        self.assertEqual(result, "2024-01-26")

    def test_business_days(self):
        count = DateCalculator.business_days("2024-01-01", "2024-01-05")
        self.assertEqual(count, 5)

    def test_business_days_with_weekend(self):
        count = DateCalculator.business_days("2024-01-05", "2024-01-08")
        self.assertEqual(count, 2)

    def test_business_days_reversed(self):
        count = DateCalculator.business_days("2024-01-08", "2024-01-05")
        self.assertEqual(count, 2)

    def test_is_leap_year(self):
        self.assertTrue(DateCalculator.is_leap_year(2024))
        self.assertFalse(DateCalculator.is_leap_year(2023))

    def test_is_leap_year_century(self):
        self.assertFalse(DateCalculator.is_leap_year(1900))

    def test_is_leap_year_400(self):
        self.assertTrue(DateCalculator.is_leap_year(2000))

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            DateCalculator._parse_date("01/01/2024", "%Y-%m-%d")

    def test_difference_negative(self):
        result = DateCalculator.difference("2024-01-10", "2024-01-01")
        self.assertEqual(result["days"], -9)


if __name__ == "__main__":
    unittest.main()
