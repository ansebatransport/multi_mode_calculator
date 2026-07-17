"""Polar coordinate conversions and operations."""
import math


class PolarCoords:
    @staticmethod
    def cartesian_to_polar(x: float, y: float) -> tuple[float, float]:
        r = math.sqrt(x ** 2 + y ** 2)
        theta = math.atan2(y, x)
        return (r, theta)

    @staticmethod
    def polar_to_cartesian(r: float, theta: float) -> tuple[float, float]:
        return (r * math.cos(theta), r * math.sin(theta))

    @staticmethod
    def r_to_cartesian(theta: float, func) -> tuple[float, float]:
        r = func(theta)
        if r is None or math.isnan(r) or math.isinf(r):
            raise ValueError("Invalid radius value")
        return (r * math.cos(theta), r * math.sin(theta))

    @staticmethod
    def format_polar(r: float, theta: float) -> str:
        return f"({r:.4f}, {theta:.4f})"

    @staticmethod
    def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
        x1, y1 = PolarCoords.polar_to_cartesian(p1[0], p1[1])
        x2, y2 = PolarCoords.polar_to_cartesian(p2[0], p2[1])
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def rotate(r: float, theta: float, angle: float) -> tuple[float, float]:
        return (r, theta + angle)
