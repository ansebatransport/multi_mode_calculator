"""Random number generation with various distributions."""
import random
import math


class RandomGenerator:
    @staticmethod
    def integer(min_val: int, max_val: int) -> int:
        if min_val > max_val:
            raise ValueError("min must be <= max")
        return random.randint(min_val, max_val)

    @staticmethod
    def uniform(min_val: float, max_val: float) -> float:
        if min_val > max_val:
            raise ValueError("min must be <= max")
        return random.uniform(min_val, max_val)

    @staticmethod
    def normal(mu: float = 0.0, sigma: float = 1.0) -> float:
        if sigma < 0:
            raise ValueError("sigma must be non-negative")
        return random.gauss(mu, sigma)

    @staticmethod
    def exponential(lam: float = 1.0) -> float:
        if lam <= 0:
            raise ValueError("lambda must be positive")
        return random.expovariate(lam)

    @staticmethod
    def set_seed(seed: int) -> None:
        random.seed(seed)

    @staticmethod
    def gaussian(mu: float = 0.0, sigma: float = 1.0) -> float:
        return random.gauss(mu, sigma)

    @staticmethod
    def triangular(low: float = 0.0, high: float = 1.0, mode: float = None) -> float:
        return random.triangular(low, high, mode)

    @staticmethod
    def beta(alpha: float, beta_val: float) -> float:
        if alpha <= 0 or beta_val <= 0:
            raise ValueError("alpha and beta must be positive")
        return random.betavariate(alpha, beta_val)

    @staticmethod
    def gamma(alpha: float, beta_val: float) -> float:
        if alpha <= 0 or beta_val <= 0:
            raise ValueError("alpha and beta must be positive")
        return random.gammavariate(alpha, beta_val)

    @staticmethod
    def shuffle(items: list) -> list:
        items = list(items)
        random.shuffle(items)
        return items

    @staticmethod
    def sample(population: list, k: int) -> list:
        if k > len(population):
            raise ValueError("k cannot be larger than population")
        return random.sample(population, k)

    @staticmethod
    def randbool(probability: float = 0.5) -> bool:
        if probability < 0 or probability > 1:
            raise ValueError("probability must be between 0 and 1")
        return random.random() < probability
