"""Probability distributions."""
import math
from typing import Optional


class DistributionCalculator:
    @staticmethod
    def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive")
        return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)

    @staticmethod
    def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive")
        return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

    @staticmethod
    def normal_inverse_cdf(p: float, mu: float = 0, sigma: float = 1) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive")
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1")
        return mu + sigma * math.sqrt(2) * _erfinv(2 * p - 1)

    @staticmethod
    def normal_probability(mu: float, sigma: float, lower: float, upper: float) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive")
        return DistributionCalculator.normal_cdf(upper, mu, sigma) - DistributionCalculator.normal_cdf(lower, mu, sigma)

    @staticmethod
    def binomial_pmf(k: int, n: int, p: float) -> float:
        if n < 0:
            raise ValueError("n must be non-negative")
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1")
        if k < 0 or k > n:
            return 0.0
        return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

    @staticmethod
    def binomial_cdf(k: int, n: int, p: float) -> float:
        if n < 0:
            raise ValueError("n must be non-negative")
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1")
        if k < 0:
            return 0.0
        if k >= n:
            return 1.0
        return sum(DistributionCalculator.binomial_pmf(i, n, p) for i in range(k + 1))

    @staticmethod
    def binomial_mean(n: int, p: float) -> float:
        return n * p

    @staticmethod
    def binomial_variance(n: int, p: float) -> float:
        return n * p * (1 - p)

    @staticmethod
    def poisson_pmf(k: int, lam: float) -> float:
        if lam <= 0:
            raise ValueError("Lambda must be positive")
        if k < 0:
            return 0.0
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    @staticmethod
    def poisson_cdf(k: int, lam: float) -> float:
        if lam <= 0:
            raise ValueError("Lambda must be positive")
        if k < 0:
            return 0.0
        return sum(DistributionCalculator.poisson_pmf(i, lam) for i in range(k + 1))

    @staticmethod
    def poisson_mean(lam: float) -> float:
        return lam

    @staticmethod
    def poisson_variance(lam: float) -> float:
        return lam

    @staticmethod
    def _factorial(n: int) -> float:
        return math.factorial(n)

    @staticmethod
    def uniform_pdf(x: float, a: float = 0, b: float = 1) -> float:
        if a >= b:
            raise ValueError("a must be less than b")
        return 1.0 / (b - a) if a <= x <= b else 0.0

    @staticmethod
    def uniform_cdf(x: float, a: float = 0, b: float = 1) -> float:
        if a >= b:
            raise ValueError("a must be less than b")
        if x < a:
            return 0.0
        if x > b:
            return 1.0
        return (x - a) / (b - a)


def _erfinv(x: float) -> float:
    if x < -1 or x > 1:
        raise ValueError("x must be between -1 and 1")
    if x == -1:
        return -float("inf")
    if x == 1:
        return float("inf")
    w = -math.log((1 - x) * (1 + x))
    if w < 5:
        w = w - 2.5
        p = 2.81022636e-08
        p = 3.43273939e-07 + p * w
        p = -3.5233877e-06 + p * w
        p = -4.39150654e-06 + p * w
        p = 0.00021858087 + p * w
        p = -0.00125372503 + p * w
        p = -0.00417768164 + p * w
        p = 0.246640727 + p * w
        p = 1.50140941 + p * w
        return p * math.tanh(x * (1 + x * x) * 2.0)
    else:
        w = math.sqrt(w) - 3
        p = -0.000200214257
        p = 0.000100950558 + p * w
        p = 0.00134934322 + p * w
        p = -0.00367342844 + p * w
        p = 0.00573950773 + p * w
        p = -0.0076224613 + p * w
        p = 0.00943887047 + p * w
        p = 1.00167406 + p * w
        p = 2.83297682 + p * w
        return p * x
