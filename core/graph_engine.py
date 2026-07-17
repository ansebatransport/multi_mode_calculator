"""Graph rendering math core — sampling, intersections, viewport management."""
import math
from typing import Callable, Optional


class GraphViewport:
    def __init__(self, x_min: float = -10, x_max: float = 10, y_min: float = -10, y_max: float = 10):
        if x_min >= x_max or y_min >= y_max:
            raise ValueError("min must be less than max")
        self._initial = (x_min, x_max, y_min, y_max)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def zoom_in(self, factor: float = 1.2, center_x: float = None, center_y: float = None):
        if factor <= 0:
            raise ValueError("Factor must be positive")
        cx = center_x or (self.x_min + self.x_max) / 2
        cy = center_y or (self.y_min + self.y_max) / 2
        x_range = self.x_range() / factor / 2
        y_range = self.y_range() / factor / 2
        self.x_min = cx - x_range
        self.x_max = cx + x_range
        self.y_min = cy - y_range
        self.y_max = cy + y_range

    def zoom_out(self, factor: float = 1.2, center_x: float = None, center_y: float = None):
        self.zoom_in(1.0 / factor, center_x, center_y)

    def pan(self, dx: float, dy: float):
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def reset(self):
        self.x_min, self.x_max, self.y_min, self.y_max = self._initial

    def x_range(self) -> float:
        return self.x_max - self.x_min

    def y_range(self) -> float:
        return self.y_max - self.y_min


class GraphEngine:
    @staticmethod
    def sample(func: Callable[[float], float], viewport: GraphViewport, num_points: int = 500) -> list[tuple[float, float]]:
        points = []
        step = viewport.x_range() / max(num_points - 1, 1)
        for i in range(num_points):
            x = viewport.x_min + i * step
            y = GraphEngine._safe_eval(func, x)
            if y is not None:
                points.append((x, y))
        return points

    @staticmethod
    def adaptive_sample(func: Callable[[float], float], viewport: GraphViewport, tolerance: float = 0.5) -> list[tuple[float, float]]:
        x_points = [viewport.x_min, viewport.x_max]
        i = 0
        while i < len(x_points) - 1:
            x1, x2 = x_points[i], x_points[i + 1]
            xm = (x1 + x2) / 2
            y1 = GraphEngine._safe_eval(func, x1)
            y2 = GraphEngine._safe_eval(func, x2)
            ym = GraphEngine._safe_eval(func, xm)
            if y1 is not None and y2 is not None and ym is not None:
                y_linear = (y1 + y2) / 2
                if abs(ym - y_linear) > tolerance:
                    x_points.insert(i + 1, xm)
                    continue
            i += 1
        points = []
        for x in x_points:
            y = GraphEngine._safe_eval(func, x)
            if y is not None:
                points.append((x, y))
        return points

    @staticmethod
    def find_roots(func: Callable[[float], float], viewport: GraphViewport, num_samples: int = 1000) -> list[float]:
        roots = []
        step = viewport.x_range() / max(num_samples - 1, 1)
        prev_x = viewport.x_min
        prev_y = GraphEngine._safe_eval(func, prev_x)
        for i in range(1, num_samples):
            x = viewport.x_min + i * step
            y = GraphEngine._safe_eval(func, x)
            if prev_y is not None and y is not None:
                if prev_y == 0:
                    roots.append(prev_x)
                elif prev_y * y < 0:
                    root = GraphEngine._bisect(func, prev_x, x)
                    if root is not None:
                        roots.append(root)
            prev_x, prev_y = x, y
        if prev_y == 0:
            roots.append(prev_x)
        return roots

    @staticmethod
    def find_intersections(func1: Callable, func2: Callable, viewport: GraphViewport) -> list[tuple[float, float]]:
        diff = lambda x: func1(x) - func2(x)
        x_roots = GraphEngine.find_roots(diff, viewport)
        points = []
        for x in x_roots:
            y = func1(x)
            if viewport.y_min <= y <= viewport.y_max:
                points.append((x, y))
        return points

    @staticmethod
    def find_extrema(func: Callable[[float], float], viewport: GraphViewport) -> list[tuple[float, float, str]]:
        extrema = []
        num_points = 1000
        step = viewport.x_range() / max(num_points - 1, 1)
        points = []
        for i in range(num_points):
            x = viewport.x_min + i * step
            y = GraphEngine._safe_eval(func, x)
            if y is not None:
                points.append((x, y))
        for i in range(1, len(points) - 1):
            x_prev, y_prev = points[i - 1]
            x_cur, y_cur = points[i]
            x_next, y_next = points[i + 1]
            if y_cur > y_prev and y_cur > y_next:
                x_opt = GraphEngine._refine_extremum(func, x_prev, x_cur, x_next, True)
                y_opt = GraphEngine._safe_eval(func, x_opt)
                if y_opt is not None:
                    extrema.append((x_opt, y_opt, "max"))
            elif y_cur < y_prev and y_cur < y_next:
                x_opt = GraphEngine._refine_extremum(func, x_prev, x_cur, x_next, False)
                y_opt = GraphEngine._safe_eval(func, x_opt)
                if y_opt is not None:
                    extrema.append((x_opt, y_opt, "min"))
        return extrema

    @staticmethod
    def sample_polar(func: Callable[[float], float], viewport: GraphViewport, num_points: int = 500) -> list[tuple[float, float]]:
        points = []
        for i in range(num_points):
            theta = 2 * math.pi * i / max(num_points - 1, 1)
            r = GraphEngine._safe_eval(func, theta)
            if r is not None and r >= 0:
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                if viewport.x_min <= x <= viewport.x_max and viewport.y_min <= y <= viewport.y_max:
                    points.append((x, y))
        return points

    @staticmethod
    def sample_parametric(x_func: Callable, y_func: Callable, t_min: float = 0, t_max: float = 2 * math.pi, num_points: int = 500) -> list[tuple[float, float]]:
        points = []
        step = (t_max - t_min) / max(num_points - 1, 1)
        for i in range(num_points):
            t = t_min + i * step
            x = GraphEngine._safe_eval(x_func, t)
            y = GraphEngine._safe_eval(y_func, t)
            if x is not None and y is not None:
                points.append((x, y))
        return points

    @staticmethod
    def _safe_eval(func: Callable, x: float) -> Optional[float]:
        try:
            y = func(x)
            if y is None or math.isnan(y) or math.isinf(y):
                return None
            return y
        except (ValueError, ZeroDivisionError, OverflowError):
            return None

    @staticmethod
    def _bisect(func: Callable, a: float, b: float, max_iter: int = 50, tol: float = 1e-12) -> Optional[float]:
        fa = func(a)
        fb = func(b)
        if fa == 0:
            return a
        if fb == 0:
            return b
        if fa * fb > 0:
            return None
        for _ in range(max_iter):
            m = (a + b) / 2
            fm = func(m)
            if fm == 0 or (b - a) < tol:
                return m
            if fa * fm < 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        return (a + b) / 2

    @staticmethod
    def _refine_extremum(func: Callable, x1: float, x2: float, x3: float, is_max: bool) -> float:
        for _ in range(10):
            y1, y2, y3 = func(x1), func(x2), func(x3)
            if y1 is None or y2 is None or y3 is None:
                return x2
            denom = 2 * (y1 - 2 * y2 + y3)
            if abs(denom) < 1e-15:
                return x2
            x_opt = x2 - ((y3 - y1) / denom) * (x3 - x2)
            if not (x1 <= x_opt <= x3):
                return x2
            x1, x2, x3 = x2, x_opt, x3 if x_opt > x2 else x1
        return x2
