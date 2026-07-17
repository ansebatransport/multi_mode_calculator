"""Equation solver for linear, quadratic, cubic equations and systems."""
import cmath
import math
from typing import Union


class EquationSolver:
    @staticmethod
    def linear(a: float, b: float) -> list[float]:
        if a == 0:
            raise ValueError("Not a linear equation (a=0)")
        return [-b / a]

    @staticmethod
    def quadratic(a: float, b: float, c: float) -> list[complex]:
        if a == 0:
            if b == 0:
                raise ValueError("Not a quadratic equation (a=0, b=0)")
            return [complex(-c / b)]
        discriminant = b ** 2 - 4 * a * c
        if discriminant >= 0:
            sqrt_d = math.sqrt(discriminant)
            return [(-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)]
        else:
            sqrt_d = cmath.sqrt(discriminant)
            return [(-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)]

    @staticmethod
    def cubic(a: float, b: float, c: float, d: float) -> list[complex]:
        if a == 0:
            return EquationSolver.quadratic(b, c, d)
        p = (3 * a * c - b ** 2) / (3 * a ** 2)
        q = (2 * b ** 3 - 9 * a * b * c + 27 * a ** 2 * d) / (27 * a ** 3)
        discriminant = (q / 2) ** 2 + (p / 3) ** 3
        roots = []
        if discriminant > 0:
            sqrt_d = math.sqrt(discriminant)
            u = (-q / 2 + sqrt_d) ** (1 / 3)
            v = (-q / 2 - sqrt_d) ** (1 / 3)
            x1 = u + v - b / (3 * a)
            roots.append(complex(x1))
            real_part = -(u + v) / 2 - b / (3 * a)
            imag_part = (u - v) * math.sqrt(3) / 2
            roots.append(complex(real_part, imag_part))
            roots.append(complex(real_part, -imag_part))
        elif discriminant == 0:
            u = (-q / 2) ** (1 / 3) if -q / 2 >= 0 else -((-q / 2) ** (1 / 3))
            x1 = 2 * u - b / (3 * a)
            x2 = -u - b / (3 * a)
            roots = [complex(x1), complex(x2), complex(x2)]
        else:
            r = math.sqrt(-(p ** 3) / 27)
            theta = math.acos(-q / (2 * r))
            for k in range(3):
                x = 2 * (r ** (1 / 3)) * math.cos((theta + 2 * math.pi * k) / 3) - b / (3 * a)
                roots.append(complex(x))
        return roots

    @staticmethod
    def solve_system_2x2(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) -> tuple[float, float]:
        det = a1 * b2 - a2 * b1
        if det == 0:
            raise ValueError("System has no unique solution (determinant is zero)")
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        return (x, y)

    @staticmethod
    def solve_system_3x3(coefficients: list[list[float]], constants: list[float]) -> list[float]:
        if len(coefficients) != 3 or any(len(row) != 3 for row in coefficients) or len(constants) != 3:
            raise ValueError("Expected 3x3 coefficient matrix and 3 constants")
        a, b, c = coefficients
        d = constants
        det = (a[0] * (b[1] * c[2] - b[2] * c[1])
               - a[1] * (b[0] * c[2] - b[2] * c[0])
               + a[2] * (b[0] * c[1] - b[1] * c[0]))
        if det == 0:
            raise ValueError("System has no unique solution (determinant is zero)")
        det_x = (d[0] * (b[1] * c[2] - b[2] * c[1])
                 - a[1] * (d[1] * c[2] - d[2] * c[0])
                 + a[2] * (d[1] * c[1] - b[1] * d[2]))
        det_y = (a[0] * (d[1] * c[2] - d[2] * c[1])
                 - d[0] * (b[0] * c[2] - b[2] * c[0])
                 + a[2] * (b[0] * d[2] - d[1] * c[0]))
        det_z = (a[0] * (b[1] * d[2] - b[2] * d[1])
                 - a[1] * (b[0] * d[2] - b[2] * d[0])
                 + d[0] * (b[0] * c[1] - b[1] * c[0]))
        return [det_x / det, det_y / det, det_z / det]

    @staticmethod
    def format_roots(roots: list[complex]) -> str:
        parts = []
        for r in roots:
            if abs(r.imag) < 1e-12:
                parts.append(f"{r.real:.6f}".rstrip("0").rstrip("."))
            else:
                real_str = f"{r.real:.6f}".rstrip("0").rstrip(".") if abs(r.real) > 1e-12 else "0"
                imag_str = f"{r.imag:.6f}".rstrip("0").rstrip(".")
                sign = "+" if r.imag >= 0 else "-"
                parts.append(f"{real_str} {sign} {abs(float(imag_str))}i")
        return ", ".join(parts)
