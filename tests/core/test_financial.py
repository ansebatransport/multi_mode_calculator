import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.financial import FinancialCalculator


class TestFinancialCalculator(unittest.TestCase):

    def test_solve_tvm_pmt(self):
        result = FinancialCalculator.solve_tvm(n=360, i_y=6, pv=200000, pmt=None, fv=0)
        self.assertIn("pmt", result)
        self.assertAlmostEqual(result["pmt"], -1199.10, delta=1.0)

    def test_solve_tvm_n(self):
        result = FinancialCalculator.solve_tvm(n=None, i_y=0, pv=-10000, pmt=200, fv=0)
        self.assertIn("n", result)
        self.assertEqual(result["n"], 50.0)

    def test_solve_tvm_iy(self):
        result = FinancialCalculator.solve_tvm(n=60, i_y=None, pv=-10000, pmt=200, fv=0)
        self.assertIn("i_y", result)
        self.assertIn("i_y", result)

    def test_solve_tvm_fv(self):
        result = FinancialCalculator.solve_tvm(n=60, i_y=5, pv=-10000, pmt=-200, fv=None)
        self.assertIn("fv", result)
        self.assertGreater(result["fv"], 0)

    def test_solve_tvm_pv(self):
        result = FinancialCalculator.solve_tvm(n=60, i_y=5, pv=None, pmt=-200, fv=0)
        self.assertIn("pv", result)

    def test_solve_tvm_multiple_unknowns(self):
        with self.assertRaises(ValueError):
            FinancialCalculator.solve_tvm(n=None, i_y=None, pv=1000, pmt=-100, fv=0)

    def test_amortization_schedule(self):
        schedule = FinancialCalculator.amortization_schedule(
            principal=100000, annual_rate=6, months=12
        )
        self.assertEqual(len(schedule), 12)
        first = schedule[0]
        self.assertEqual(first["month"], 1)
        self.assertGreater(first["payment"], 0)
        self.assertGreater(first["interest_paid"], 0)
        last = schedule[-1]
        self.assertEqual(last["month"], 12)
        self.assertAlmostEqual(last["balance"], 0, delta=0.01)

    def test_amortization_zero_months(self):
        schedule = FinancialCalculator.amortization_schedule(
            principal=100000, annual_rate=6, months=0
        )
        self.assertEqual(schedule, [])

    def test_npv(self):
        cash_flows = [-1000, 300, 420, 680]
        result = FinancialCalculator.npv(10, cash_flows)
        self.assertAlmostEqual(result, 130.73, delta=1.0)

    def test_npv_zero_rate(self):
        cash_flows = [-1000, 300, 400, 500]
        result = FinancialCalculator.npv(0, cash_flows)
        self.assertAlmostEqual(result, 200.0, delta=0.01)

    def test_irr(self):
        cash_flows = [-1000, 300, 420, 680]
        result = FinancialCalculator.irr(cash_flows)
        self.assertGreater(result, 0)

    def test_irr_simple(self):
        cash_flows = [-100, 110]
        result = FinancialCalculator.irr(cash_flows)
        self.assertAlmostEqual(result, 10.0, delta=0.5)

    def test_straight_line(self):
        schedule = FinancialCalculator.straight_line(10000, 1000, 5)
        self.assertEqual(len(schedule), 5)
        annual_dep = 9000 / 5
        self.assertAlmostEqual(schedule[0]["depreciation"], annual_dep, delta=0.01)
        self.assertAlmostEqual(schedule[-1]["book_value"], 1000, delta=0.01)
        total_dep = sum(s["depreciation"] for s in schedule)
        self.assertAlmostEqual(total_dep, 9000, delta=0.1)

    def test_straight_line_invalid_life(self):
        with self.assertRaises(ValueError):
            FinancialCalculator.straight_line(10000, 1000, 0)

    def test_declining_balance(self):
        schedule = FinancialCalculator.declining_balance(10000, 1000, 5)
        self.assertEqual(len(schedule), 5)
        self.assertGreater(schedule[0]["depreciation"], schedule[1]["depreciation"])
        self.assertAlmostEqual(schedule[-1]["book_value"], 1000, delta=1)

    def test_sum_of_years(self):
        schedule = FinancialCalculator.sum_of_years(10000, 1000, 5)
        self.assertEqual(len(schedule), 5)
        self.assertGreater(schedule[0]["depreciation"], schedule[-1]["depreciation"])
        total_dep = sum(s["depreciation"] for s in schedule)
        self.assertAlmostEqual(total_dep, 9000, delta=0.1)

    def test_bond_price(self):
        result = FinancialCalculator.bond_price(
            face=1000, coupon_rate=5, ytm=5, years=10, freq=2
        )
        self.assertAlmostEqual(result["dirty_price"], 1000, delta=1)

    def test_bond_price_discount(self):
        result = FinancialCalculator.bond_price(
            face=1000, coupon_rate=4, ytm=6, years=10, freq=2
        )
        self.assertLess(result["dirty_price"], 1000)

    def test_bond_price_premium(self):
        result = FinancialCalculator.bond_price(
            face=1000, coupon_rate=6, ytm=4, years=10, freq=2
        )
        self.assertGreater(result["dirty_price"], 1000)

    def test_break_even(self):
        result = FinancialCalculator.break_even(
            fixed_costs=10000, price_per_unit=50, variable_cost_per_unit=30
        )
        self.assertEqual(result["break_even_units"], 500)
        self.assertEqual(result["break_even_revenue"], 25000)
        self.assertEqual(result["contribution_margin"], 20)

    def test_break_even_invalid(self):
        with self.assertRaises(ValueError):
            FinancialCalculator.break_even(10000, 10, 20)

    def test_profit_margin(self):
        result = FinancialCalculator.profit_margin(100000, 60000)
        self.assertEqual(result["gross_profit"], 40000)
        self.assertAlmostEqual(result["gross_margin"], 40.0, places=1)

    def test_roi(self):
        result = FinancialCalculator.roi(10000, 15000, 2)
        self.assertEqual(result["roi"], 50.0)
        self.assertGreater(result["annualized_roi"], 0)

    def test_roi_zero_investment(self):
        result = FinancialCalculator.roi(0, 5000)
        self.assertEqual(result["roi"], 0)


if __name__ == "__main__":
    unittest.main()
