import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.worksheets import WorksheetCalculator


class TestWorksheetCalculator(unittest.TestCase):
    def test_simple_interest(self):
        result = WorksheetCalculator.simple_interest(1000, 5, 2)
        self.assertAlmostEqual(result, 100.0)

    def test_simple_interest_zero_rate(self):
        result = WorksheetCalculator.simple_interest(1000, 0, 2)
        self.assertAlmostEqual(result, 0.0)

    def test_simple_interest_negative(self):
        with self.assertRaises(ValueError):
            WorksheetCalculator.simple_interest(-1000, 5, 2)

    def test_compound_interest(self):
        result = WorksheetCalculator.compound_interest(1000, 5, 1, 1)
        self.assertAlmostEqual(result, 1050.0)

    def test_compound_interest_monthly(self):
        result = WorksheetCalculator.compound_interest(1000, 12, 12, 1)
        self.assertAlmostEqual(result, 1126.83, places=0)

    def test_compound_interest_invalid_periods(self):
        with self.assertRaises(ValueError):
            WorksheetCalculator.compound_interest(1000, 5, 0, 1)

    def test_compound_interest_negative(self):
        with self.assertRaises(ValueError):
            WorksheetCalculator.compound_interest(-1000, 5, 1, 1)

    def test_mortgage_payment(self):
        result = WorksheetCalculator.mortgage_monthly_payment(200000, 5, 30)
        self.assertGreater(result["monthly_payment"], 0)
        self.assertGreater(result["total_interest"], 0)
        self.assertGreater(result["total_payment"], result["monthly_payment"] * 360)

    def test_mortgage_zero_rate(self):
        result = WorksheetCalculator.mortgage_monthly_payment(12000, 0, 1)
        self.assertAlmostEqual(result["monthly_payment"], 1000.0)

    def test_mortgage_invalid_principal(self):
        with self.assertRaises(ValueError):
            WorksheetCalculator.mortgage_monthly_payment(-1000, 5, 30)

    def test_car_loan_payment(self):
        result = WorksheetCalculator.car_loan_payment(20000, 5, 60)
        self.assertGreater(result["monthly_payment"], 0)
        self.assertGreater(result["total_interest"], 0)
        self.assertGreater(result["total_payment"], result["monthly_payment"] * 60)

    def test_car_loan_zero_rate(self):
        result = WorksheetCalculator.car_loan_payment(12000, 0, 12)
        self.assertAlmostEqual(result["monthly_payment"], 1000.0)

    def test_lease_payment(self):
        result = WorksheetCalculator.lease_monthly_payment(30000, 18000, 0.00125, 36)
        self.assertGreater(result, 0)

    def test_fuel_economy_mpg(self):
        result = WorksheetCalculator.fuel_economy_mpg(300, 10)
        self.assertAlmostEqual(result, 30.0)

    def test_fuel_economy_zero_fuel(self):
        with self.assertRaises(ValueError):
            WorksheetCalculator.fuel_economy_mpg(300, 0)

    def test_fuel_economy_l100km(self):
        result = WorksheetCalculator.fuel_economy_l100km(100, 8)
        self.assertAlmostEqual(result, 8.0)

    def test_mpg_conversion(self):
        mpg = 30
        l100 = WorksheetCalculator.mpg_to_l100km(mpg)
        back = WorksheetCalculator.l100km_to_mpg(l100)
        self.assertAlmostEqual(back, mpg)


if __name__ == "__main__":
    unittest.main()
