"""Date arithmetic and calculations."""
from datetime import datetime, timedelta
from typing import Optional


class DateCalculator:
    @staticmethod
    def difference(start: str, end: str, fmt: str = "%Y-%m-%d") -> dict:
        d1 = DateCalculator._parse_date(start, fmt)
        d2 = DateCalculator._parse_date(end, fmt)
        diff = d2 - d1
        total_days = diff.days
        weeks = total_days // 7
        rem_days = total_days % 7
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30
        return {
            "days": total_days,
            "weeks_days": f"{weeks} weeks, {rem_days} days",
            "years_months_days": f"{years} years, {months} months, {days} days",
            "hours": total_days * 24,
        }

    @staticmethod
    def add_days(date_str: str, days: int, fmt: str = "%Y-%m-%d") -> str:
        d = DateCalculator._parse_date(date_str, fmt)
        result = d + timedelta(days=days)
        return result.strftime(fmt)

    @staticmethod
    def subtract_days(date_str: str, days: int, fmt: str = "%Y-%m-%d") -> str:
        return DateCalculator.add_days(date_str, -days, fmt)

    @staticmethod
    def business_days(start: str, end: str, fmt: str = "%Y-%m-%d") -> int:
        d1 = DateCalculator._parse_date(start, fmt)
        d2 = DateCalculator._parse_date(end, fmt)
        if d1 > d2:
            d1, d2 = d2, d1
        count = 0
        current = d1
        while current <= d2:
            if current.weekday() < 5:
                count += 1
            current += timedelta(days=1)
        return count

    @staticmethod
    def age(birth_date: str, fmt: str = "%Y-%m-%d") -> dict:
        birth = DateCalculator._parse_date(birth_date, fmt)
        today = datetime.now()
        years = today.year - birth.year
        months = today.month - birth.month
        days = today.day - birth.day
        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - datetime(prev_year, prev_month, 1)).days if prev_month < 12 else (datetime(prev_year + 1, 1, 1) - datetime(prev_year, 12, 1)).days
            days += days_in_prev_month
        if months < 0:
            years -= 1
            months += 12
        return {"years": years, "months": months, "days": days}

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def _parse_date(date_str: str, fmt: str) -> datetime:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date_str}. Expected format: {fmt}") from e
