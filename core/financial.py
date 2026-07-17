"""Financial calculator: TVM, amortization, cash flow, depreciation, bonds, break-even."""
import math
from typing import Optional

class FinancialCalculator:
    """Professional financial calculator with TVM, NPV/IRR, depreciation, bonds."""

    # ========== Time Value of Money (TVM) ==========

    @staticmethod
    def solve_tvm(
        n: Optional[float] = None,
        i_y: Optional[float] = None,
        pv: Optional[float] = None,
        pmt: Optional[float] = None,
        fv: Optional[float] = None,
        py: int = 12,
        cy: int = 12,
        mode: str = "END"
    ) -> dict:
        unknowns = [name for name, val in [('n', n), ('i_y', i_y), ('pv', pv), ('pmt', pmt), ('fv', fv)] if val is None]
        if len(unknowns) != 1:
            raise ValueError(f"Exactly one variable must be unknown, got {len(unknowns)}")

        r = (i_y / 100) / cy if i_y is not None else None
        periods_per_payment = cy / py if py > 0 else 1

        solved_for = unknowns[0]

        if solved_for == 'n':
            if r == 0:
                n_val = -(pv + fv) / pmt if pmt != 0 else 0
            else:
                mode_adj = 1 if mode == "END" else (1 + r)
                numerator = -(pv * r + pmt * mode_adj)
                denominator = fv * r + pmt * mode_adj
                if denominator == 0:
                    raise ValueError("Cannot solve for n: denominator is zero")
                n_val = math.log(numerator / denominator) / math.log(1 + r)
                n_val = n_val * periods_per_payment
            result = {'n': round(n_val, 6), 'i_y': i_y, 'pv': pv, 'pmt': pmt, 'fv': fv}

        elif solved_for == 'i_y':
            i_y_val = FinancialCalculator._solve_rate(n, pv, pmt, fv, py, cy, mode)
            result = {'n': n, 'i_y': round(i_y_val, 8), 'pv': pv, 'pmt': pmt, 'fv': fv}

        elif solved_for == 'pv':
            if r == 0:
                pv_val = -(fv + pmt * n)
            else:
                mode_adj = 1 if mode == "END" else (1 + r)
                n_periods = n * py / cy
                pv_val = -(fv / (1 + r) ** n_periods + pmt * mode_adj * ((1 - (1 + r) ** (-n_periods)) / r))
            result = {'n': n, 'i_y': i_y, 'pv': round(pv_val, 6), 'pmt': pmt, 'fv': fv}

        elif solved_for == 'pmt':
            if r == 0:
                pmt_val = -(pv + fv) / n
            else:
                n_periods = n * py / cy
                pmt_val = -(pv * r * (1 + r) ** n_periods + fv * r) / ((1 + r) ** n_periods - 1)
            result = {'n': n, 'i_y': i_y, 'pv': pv, 'pmt': round(pmt_val, 6), 'fv': fv}

        elif solved_for == 'fv':
            if r == 0:
                fv_val = -(pv + pmt * n)
            else:
                mode_adj = 1 if mode == "END" else (1 + r)
                n_periods = n * py / cy
                fv_val = -(pv * (1 + r) ** n_periods + pmt * mode_adj * ((1 + r) ** n_periods - 1) / r)
            result = {'n': n, 'i_y': i_y, 'pv': pv, 'pmt': pmt, 'fv': round(fv_val, 6)}

        result['solved_for'] = solved_for
        return result

    @staticmethod
    def _solve_rate(n, pv, pmt, fv, py, cy, mode, guess=0.05, max_iter=100, tol=1e-10):
        r = guess
        for _ in range(max_iter):
            n_periods = n * py / cy
            if r == 0:
                break
            pv_factor = (1 + r) ** (-n_periods)
            annuity = ((1 - pv_factor) / r) if mode == "END" else ((1 - pv_factor) / r) * (1 + r)
            f_val = pv + pmt * annuity + fv * pv_factor
            df = pmt * (-n_periods * (1 + r) ** (-n_periods - 1) / r - (1 - pv_factor) / (r ** 2))
            if mode == "BGN":
                df *= (1 + r)
            df += fv * (-n_periods * (1 + r) ** (-n_periods - 1))
            if abs(df) < 1e-20:
                break
            r = r - f_val / df
            if abs(f_val) < tol:
                break
        return r * 100

    # ========== Amortization Schedule ==========

    @staticmethod
    def amortization_schedule(
        principal: float,
        annual_rate: float,
        months: int,
        pmt: Optional[float] = None
    ) -> list[dict]:
        if months <= 0:
            return []

        monthly_rate = annual_rate / 100 / 12

        if pmt is None:
            if monthly_rate == 0:
                pmt = principal / months
            else:
                pmt = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-months))

        schedule = []
        balance = principal

        for month in range(1, months + 1):
            interest_paid = balance * monthly_rate
            principal_paid = pmt - interest_paid
            balance -= principal_paid

            if month == months:
                principal_paid += balance
                pmt_actual = principal_paid + interest_paid
                balance = 0
            else:
                pmt_actual = pmt

            schedule.append({
                'month': month,
                'payment': round(pmt_actual, 2),
                'principal_paid': round(principal_paid, 2),
                'interest_paid': round(interest_paid, 2),
                'balance': round(max(0, balance), 2),
            })

        return schedule

    # ========== Cash Flow Analysis ==========

    @staticmethod
    def npv(rate: float, cash_flows: list[float]) -> float:
        r = rate / 100
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows))

    @staticmethod
    def irr(cash_flows: list[float], guess: float = 10.0, max_iter: int = 1000, tol: float = 1e-8) -> float:
        r = guess / 100
        for _ in range(max_iter):
            f_val = sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows))
            df = sum(-t * cf / (1 + r) ** (t + 1) for t, cf in enumerate(cash_flows))
            if abs(df) < 1e-20:
                break
            r = r - f_val / df
            if abs(f_val) < tol:
                return r * 100
        raise ValueError("IRR did not converge")

    @staticmethod
    def mirr(cash_flows: list[float], finance_rate: float, reinvest_rate: float) -> float:
        n = len(cash_flows) - 1
        if n <= 0:
            raise ValueError("Need at least 2 cash flows")

        fr = finance_rate / 100
        rr = reinvest_rate / 100

        pv_negative = sum(cf / (1 + fr) ** t for t, cf in enumerate(cash_flows) if cf < 0)
        fv_positive = sum(cf * (1 + rr) ** (n - t) for t, cf in enumerate(cash_flows) if cf > 0)

        if pv_negative == 0 or fv_positive == 0:
            raise ValueError("Cannot compute MIRR")

        mirr_val = (-fv_positive / pv_negative) ** (1 / n) - 1
        return mirr_val * 100

    # ========== Depreciation ==========

    @staticmethod
    def straight_line(cost: float, salvage: float, life: int) -> list[dict]:
        if life <= 0:
            raise ValueError("Life must be positive")
        depreciable = cost - salvage
        annual = depreciable / life

        schedule = []
        book_value = cost
        for year in range(1, life + 1):
            dep = min(annual, book_value - salvage)
            book_value -= dep
            schedule.append({
                'year': year,
                'depreciation': round(dep, 2),
                'accumulated': round(cost - book_value, 2),
                'book_value': round(book_value, 2),
            })
        return schedule

    @staticmethod
    def declining_balance(cost: float, salvage: float, life: int, rate: Optional[float] = None) -> list[dict]:
        if life <= 0:
            raise ValueError("Life must be positive")
        if rate is None:
            rate = 2 / life

        schedule = []
        book_value = cost
        for year in range(1, life + 1):
            dep = book_value * rate
            if book_value - dep < salvage:
                dep = book_value - salvage
            book_value -= dep
            schedule.append({
                'year': year,
                'depreciation': round(dep, 2),
                'accumulated': round(cost - book_value, 2),
                'book_value': round(max(0, book_value), 2),
            })
        return schedule

    @staticmethod
    def sum_of_years(cost: float, salvage: float, life: int) -> list[dict]:
        if life <= 0:
            raise ValueError("Life must be positive")
        depreciable = cost - salvage
        syd = life * (life + 1) / 2

        schedule = []
        book_value = cost
        for year in range(1, life + 1):
            fraction = (life - year + 1) / syd
            dep = depreciable * fraction
            book_value -= dep
            schedule.append({
                'year': year,
                'depreciation': round(dep, 2),
                'accumulated': round(cost - book_value, 2),
                'book_value': round(max(0, book_value), 2),
            })
        return schedule

    # ========== Bond Calculations ==========

    @staticmethod
    def bond_price(
        face: float,
        coupon_rate: float,
        ytm: float,
        years: int,
        freq: int = 2
    ) -> dict:
        n = years * freq
        r = ytm / 100 / freq
        c = face * coupon_rate / 100 / freq

        if r == 0:
            dirty_price = face + c * n
        else:
            pv_coupons = c * (1 - (1 + r) ** (-n)) / r
            pv_face = face / (1 + r) ** n
            dirty_price = pv_coupons + pv_face

        current_yield = (face * coupon_rate / 100) / dirty_price * 100 if dirty_price > 0 else 0

        return {
            'dirty_price': round(dirty_price, 2),
            'clean_price': round(dirty_price, 2),
            'current_yield': round(current_yield, 4),
            'total_coupon': round(face * coupon_rate / 100, 2),
            'total_coupons_received': round(c * n, 2),
        }

    @staticmethod
    def bond_ytm(
        face: float,
        coupon_rate: float,
        price: float,
        years: int,
        freq: int = 2
    ) -> float:
        n = years * freq
        c = face * coupon_rate / 100 / freq

        ytm = coupon_rate
        for _ in range(200):
            r = ytm / 100 / freq
            if r == 0:
                break
            pv = c * (1 - (1 + r) ** (-n)) / r + face / (1 + r) ** n
            dpv = -c * (1 - (1 + r) ** (-n)) / (r ** 2) + c * n * (1 + r) ** (-n - 1) / r - face * n * (1 + r) ** (-n - 1)
            if abs(dpv) < 1e-20:
                break
            ytm = ytm - (pv - price) / dpv * 100
            if abs(pv - price) < 0.001:
                break
        return round(ytm, 4)

    # ========== Break-Even Analysis ==========

    @staticmethod
    def break_even(
        fixed_costs: float,
        price_per_unit: float,
        variable_cost_per_unit: float
    ) -> dict:
        if price_per_unit <= variable_cost_per_unit:
            raise ValueError("Price must exceed variable cost")

        contribution_margin = price_per_unit - variable_cost_per_unit
        be_units = math.ceil(fixed_costs / contribution_margin)
        be_revenue = be_units * price_per_unit

        return {
            'break_even_units': be_units,
            'break_even_revenue': round(be_revenue, 2),
            'contribution_margin': round(contribution_margin, 2),
            'contribution_margin_pct': round(contribution_margin / price_per_unit * 100, 2),
        }

    # ========== Profit & ROI ==========

    @staticmethod
    def profit_margin(revenue: float, cost: float) -> dict:
        if revenue == 0:
            return {'gross_profit': 0, 'gross_margin': 0, 'markup': 0}
        gross_profit = revenue - cost
        gross_margin = (gross_profit / revenue) * 100
        markup = (gross_profit / cost * 100) if cost > 0 else float('inf')
        return {
            'gross_profit': round(gross_profit, 2),
            'gross_margin': round(gross_margin, 2),
            'markup': round(markup, 2),
        }

    @staticmethod
    def roi(investment: float, return_value: float, years: float = 1.0) -> dict:
        if investment == 0:
            return {'roi': 0, 'annualized_roi': 0, 'total_return': 0}
        total_return = ((return_value - investment) / investment) * 100
        annualized = ((return_value / investment) ** (1 / years) - 1) * 100 if years > 0 else 0
        return {
            'roi': round(total_return, 2),
            'annualized_roi': round(annualized, 2),
            'total_return': round(return_value - investment, 2),
        }
