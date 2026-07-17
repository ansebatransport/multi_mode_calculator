"""Fraction simplification and conversion."""
from math import gcd
from fractions import Fraction as PyFraction
from .recurring_decimal import RecurringDecimal


class FractionHelper:
    @staticmethod
    def decimal_to_fraction(value: float, max_denominator: int = 10000) -> tuple[int, int]:
        if value == int(value):
            return int(value), 1
        neg = -1 if value < 0 else 1
        value = abs(value)
        frac = PyFraction(value).limit_denominator(max_denominator)
        return neg * frac.numerator, frac.denominator

    @staticmethod
    def simplify(numerator: int, denominator: int) -> tuple[int, int]:
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if numerator == 0:
            return 0, 1
        g = gcd(abs(numerator), abs(denominator))
        num = numerator // g
        den = denominator // g
        if den < 0:
            num = -num
            den = -den
        return num, den

    @staticmethod
    def to_mixed(numerator: int, denominator: int) -> tuple[int, int, int]:
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        num, den = FractionHelper.simplify(numerator, denominator)
        whole = num // den
        remainder = abs(num) % den
        if num < 0 and whole == 0:
            return whole, -remainder, den
        return whole, remainder, den

    @staticmethod
    def add(n1: int, d1: int, n2: int, d2: int) -> tuple[int, int]:
        if d1 == 0 or d2 == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        num = n1 * d2 + n2 * d1
        den = d1 * d2
        return FractionHelper.simplify(num, den)

    @staticmethod
    def multiply(n1: int, d1: int, n2: int, d2: int) -> tuple[int, int]:
        if d1 == 0 or d2 == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        num = n1 * n2
        den = d1 * d2
        return FractionHelper.simplify(num, den)

    @staticmethod
    def divide(n1: int, d1: int, n2: int, d2: int) -> tuple[int, int]:
        if d1 == 0 or d2 == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if n2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        num = n1 * d2
        den = d1 * n2
        return FractionHelper.simplify(num, den)

    @staticmethod
    def subtract(n1: int, d1: int, n2: int, d2: int) -> tuple[int, int]:
        if d1 == 0 or d2 == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        num = n1 * d2 - n2 * d1
        den = d1 * d2
        return FractionHelper.simplify(num, den)

    @staticmethod
    def format_mixed(whole: int, num: int, den: int) -> str:
        if den == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if whole == 0 and num == 0:
            return "0"
        if whole == 0:
            return f"{num}/{den}"
        if num == 0:
            return str(whole)
        if whole < 0 and num > 0:
            return f"{whole} {num}/{den}"
        return f"{whole} {num}/{den}"

    @staticmethod
    def format_fraction(num: int, den: int) -> str:
        if den == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if den == 1:
            return str(num)
        return f"{num}/{den}"

    @staticmethod
    def is_repeating(value: float) -> tuple[bool, str]:
        result = RecurringDecimal.detect(value)
        return result["is_recurring"], result["notation"]
