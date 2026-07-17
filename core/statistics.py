"""Descriptive statistical calculations."""
import math
from collections import Counter


class Statistics:
    @staticmethod
    def mean(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return sum(data) / len(data)

    @staticmethod
    def median(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        s = sorted(data)
        n = len(s)
        mid = n // 2
        if n % 2 == 1:
            return s[mid]
        return (s[mid - 1] + s[mid]) / 2

    @staticmethod
    def mode(data: list[float]) -> list[float]:
        if not data:
            raise ValueError("Data cannot be empty")
        counts = Counter(data)
        max_count = max(counts.values())
        return sorted([k for k, v in counts.items() if v == max_count])

    @staticmethod
    def std_dev(data: list[float], population: bool = False) -> float:
        return math.sqrt(Statistics.variance(data, population))

    @staticmethod
    def variance(data: list[float], population: bool = False) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        if len(data) == 1 and not population:
            raise ValueError("Variance requires at least 2 data points for sample")
        mean = Statistics.mean(data)
        n = len(data)
        ss = sum((x - mean) ** 2 for x in data)
        return ss / n if population else ss / (n - 1)

    @staticmethod
    def sum(data: list[float]) -> float:
        return sum(data)

    @staticmethod
    def count(data: list[float]) -> int:
        return len(data)

    @staticmethod
    def minimum(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return min(data)

    @staticmethod
    def maximum(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return max(data)

    @staticmethod
    def range_val(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return max(data) - min(data)

    @staticmethod
    def quartile_q1(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return Statistics.percentile(data, 25)

    @staticmethod
    def quartile_q3(data: list[float]) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        return Statistics.percentile(data, 75)

    @staticmethod
    def iqr(data: list[float]) -> float:
        return Statistics.quartile_q3(data) - Statistics.quartile_q1(data)

    @staticmethod
    def percentile(data: list[float], p: float) -> float:
        if not data:
            raise ValueError("Data cannot be empty")
        if p < 0 or p > 100:
            raise ValueError("Percentile must be between 0 and 100")
        s = sorted(data)
        n = len(s)
        idx = (p / 100) * (n - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return s[lo]
        return s[lo] * (hi - idx) + s[hi] * (idx - lo)

    @staticmethod
    def all_stats(data: list[float]) -> dict:
        return {
            "mean": Statistics.mean(data),
            "median": Statistics.median(data),
            "mode": Statistics.mode(data),
            "std_dev": Statistics.std_dev(data),
            "variance": Statistics.variance(data),
            "sum": Statistics.sum(data),
            "count": Statistics.count(data),
            "minimum": Statistics.minimum(data),
            "maximum": Statistics.maximum(data),
            "range": Statistics.range_val(data),
            "q1": Statistics.quartile_q1(data),
            "q3": Statistics.quartile_q3(data),
            "iqr": Statistics.iqr(data),
        }
