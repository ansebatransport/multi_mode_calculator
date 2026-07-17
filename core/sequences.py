"""Arithmetic and geometric sequence generation."""
import math
from typing import Callable


class SequenceGenerator:
    @staticmethod
    def arithmetic(start: float, common_diff: float, n_terms: int) -> list[float]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        return [start + i * common_diff for i in range(n_terms)]

    @staticmethod
    def geometric(start: float, common_ratio: float, n_terms: int) -> list[float]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        return [start * (common_ratio ** i) for i in range(n_terms)]

    @staticmethod
    def fibonacci(n_terms: int) -> list[int]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        if n_terms == 1:
            return [0]
        seq = [0, 1]
        for _ in range(2, n_terms):
            seq.append(seq[-1] + seq[-2])
        return seq[:n_terms]

    @staticmethod
    def factorial_sequence(n_terms: int) -> list[int]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        return [math.factorial(i) for i in range(n_terms)]

    @staticmethod
    def powers_of_two(n_terms: int) -> list[int]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        return [2 ** i for i in range(n_terms)]

    @staticmethod
    def custom(start: float, func: Callable, n_terms: int) -> list[float]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        seq = [start]
        for i in range(1, n_terms):
            seq.append(func(seq[-1], i))
        return seq[:n_terms]

    @staticmethod
    def sum_arithmetic(start: float, common_diff: float, n_terms: int) -> float:
        seq = SequenceGenerator.arithmetic(start, common_diff, n_terms)
        return sum(seq)

    @staticmethod
    def sum_geometric(start: float, common_ratio: float, n_terms: int) -> float:
        if common_ratio == 1:
            return start * n_terms
        return start * (1 - common_ratio ** n_terms) / (1 - common_ratio)

    @staticmethod
    def triangular_numbers(n_terms: int) -> list[int]:
        if n_terms < 1:
            raise ValueError("n_terms must be at least 1")
        return [i * (i + 1) // 2 for i in range(1, n_terms + 1)]
