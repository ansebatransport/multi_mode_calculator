"""Complex number operations."""
import cmath
import math


class ComplexCalculator:
    @staticmethod
    def create(real: float, imag: float) -> complex:
        return complex(real, imag)

    @staticmethod
    def add(a: complex, b: complex) -> complex:
        return a + b

    @staticmethod
    def subtract(a: complex, b: complex) -> complex:
        return a - b

    @staticmethod
    def multiply(a: complex, b: complex) -> complex:
        return a * b

    @staticmethod
    def divide(a: complex, b: complex) -> complex:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    @staticmethod
    def conjugate(z: complex) -> complex:
        return z.conjugate()

    @staticmethod
    def magnitude(z: complex) -> float:
        return abs(z)

    @staticmethod
    def phase(z: complex, in_degrees: bool = False) -> float:
        phi = cmath.phase(z)
        return math.degrees(phi) if in_degrees else phi

    @staticmethod
    def to_polar(z: complex) -> tuple[float, float]:
        return (abs(z), cmath.phase(z))

    @staticmethod
    def from_polar(r: float, theta: float) -> complex:
        return cmath.rect(r, theta)

    @staticmethod
    def format(z: complex, precision: int = 6) -> str:
        real = round(z.real, precision)
        imag = round(z.imag, precision)
        if imag == 0:
            return _fmt(real)
        if real == 0:
            return f"{_fmt(imag)}i"
        op = "+" if imag >= 0 else "-"
        return f"{_fmt(real)} {op} {_fmt(abs(imag))}i"


def _fmt(v: float) -> str:
    if v == int(v):
        return str(int(v))
    s = f"{v:.10f}".rstrip("0").rstrip(".")
    return s

    @staticmethod
    def sin(z: complex) -> complex:
        return cmath.sin(z)

    @staticmethod
    def cos(z: complex) -> complex:
        return cmath.cos(z)

    @staticmethod
    def tan(z: complex) -> complex:
        return cmath.tan(z)

    @staticmethod
    def log(z: complex) -> complex:
        return cmath.log(z)

    @staticmethod
    def sqrt(z: complex) -> complex:
        return cmath.sqrt(z)

    @staticmethod
    def power(z: complex, n: complex) -> complex:
        return z ** n

    @staticmethod
    def atan(z: complex) -> complex:
        return cmath.atan(z)

    @staticmethod
    def asin(z: complex) -> complex:
        return cmath.asin(z)

    @staticmethod
    def acos(z: complex) -> complex:
        return cmath.acos(z)

    @staticmethod
    def exp(z: complex) -> complex:
        return cmath.exp(z)
