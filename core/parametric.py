"""Parametric curve evaluation for graphing."""
import math
from typing import Callable


class ParametricEvaluator:
    @staticmethod
    def evaluate(x_func: Callable, y_func: Callable, t: float) -> tuple[float, float]:
        return (x_func(t), y_func(t))

    @staticmethod
    def sample(x_func: Callable, y_func: Callable, t_min: float, t_max: float, num_points: int = 500) -> list[tuple[float, float]]:
        if num_points < 2:
            raise ValueError("num_points must be at least 2")
        points = []
        step = (t_max - t_min) / max(num_points - 1, 1)
        for i in range(num_points):
            t = t_min + i * step
            try:
                x = x_func(t)
                y = y_func(t)
                if x is not None and y is not None and not (math.isnan(x) or math.isinf(x) or math.isnan(y) or math.isinf(y)):
                    points.append((x, y))
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
        return points

    @staticmethod
    def arc_length(x_func: Callable, y_func: Callable, t_min: float, t_max: float, num_samples: int = 1000) -> float:
        dt = (t_max - t_min) / max(num_samples - 1, 1)
        length = 0.0
        prev_x, prev_y = x_func(t_min), y_func(t_min)
        for i in range(1, num_samples):
            t = t_min + i * dt
            x, y = x_func(t), y_func(t)
            if all(v is not None and not (math.isnan(v) or math.isinf(v)) for v in (prev_x, prev_y, x, y)):
                length += math.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            prev_x, prev_y = x, y
        return length

    @staticmethod
    def tangent_slope(x_func: Callable, y_func: Callable, t: float, dt: float = 1e-7) -> float:
        x1, y1 = x_func(t - dt), y_func(t - dt)
        x2, y2 = x_func(t + dt), y_func(t + dt)
        dx = x2 - x1
        if abs(dx) < 1e-15:
            return float("inf")
        return (y2 - y1) / dx

    @staticmethod
    def speed(x_func: Callable, y_func: Callable, t: float, dt: float = 1e-7) -> float:
        x1, y1 = x_func(t - dt), y_func(t - dt)
        x2, y2 = x_func(t + dt), y_func(t + dt)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / (2 * dt)
