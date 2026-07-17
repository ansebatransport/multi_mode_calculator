"""Worksheet templates for common calculations."""
import math


class WorksheetCalculator:
    @staticmethod
    def fuel_economy_mpg(distance: float, fuel: float) -> float:
        if fuel == 0:
            raise ValueError("Fuel cannot be zero")
        if distance < 0 or fuel < 0:
            raise ValueError("Distance and fuel must be non-negative")
        return distance / fuel

    @staticmethod
    def fuel_economy_l100km(distance: float, fuel: float) -> float:
        if distance == 0:
            raise ValueError("Distance cannot be zero")
        if distance < 0 or fuel < 0:
            raise ValueError("Distance and fuel must be non-negative")
        return (fuel / distance) * 100

    @staticmethod
    def mpg_to_l100km(mpg: float) -> float:
        if mpg <= 0:
            raise ValueError("MPG must be positive")
        return 235.214 / mpg

    @staticmethod
    def l100km_to_mpg(l100km: float) -> float:
        if l100km <= 0:
            raise ValueError("L/100km must be positive")
        return 235.214 / l100km

    @staticmethod
    def mortgage_monthly_payment(principal: float, annual_rate: float, years: int) -> dict:
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if annual_rate < 0:
            raise ValueError("Annual rate cannot be negative")
        if years <= 0:
            raise ValueError("Years must be positive")
        monthly_rate = annual_rate / 100 / 12
        n_payments = years * 12
        if monthly_rate == 0:
            monthly = principal / n_payments
        else:
            monthly = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
        total = monthly * n_payments
        return {
            "monthly_payment": round(monthly, 2),
            "total_payment": round(total, 2),
            "total_interest": round(total - principal, 2),
        }

    @staticmethod
    def lease_monthly_payment(cap_cost: float, residual_value: float, money_factor: float, months: int) -> float:
        if cap_cost <= 0:
            raise ValueError("Capitalized cost must be positive")
        if residual_value < 0:
            raise ValueError("Residual value cannot be negative")
        if money_factor < 0:
            raise ValueError("Money factor cannot be negative")
        if months <= 0:
            raise ValueError("Months must be positive")
        depreciation = (cap_cost - residual_value) / months
        finance = (cap_cost + residual_value) * money_factor
        return round(depreciation + finance, 2)

    @staticmethod
    def car_loan_payment(principal: float, annual_rate: float, months: int) -> dict:
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if annual_rate < 0:
            raise ValueError("Annual rate cannot be negative")
        if months <= 0:
            raise ValueError("Months must be positive")
        monthly_rate = annual_rate / 100 / 12
        if monthly_rate == 0:
            monthly = principal / months
        else:
            monthly = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total = monthly * months
        return {
            "monthly_payment": round(monthly, 2),
            "total_payment": round(total, 2),
            "total_interest": round(total - principal, 2),
        }

    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> float:
        if principal < 0 or rate < 0 or time < 0:
            raise ValueError("Principal, rate, and time must be non-negative")
        return round(principal * (rate / 100) * time, 2)

    @staticmethod
    def compound_interest(principal: float, rate: float, n: int, time: float) -> float:
        if principal < 0 or rate < 0 or time < 0:
            raise ValueError("Principal, rate, and time must be non-negative")
        if n <= 0:
            raise ValueError("Compounding periods per year must be positive")
        amount = principal * (1 + (rate / 100) / n) ** (n * time)
        return round(amount, 2)
