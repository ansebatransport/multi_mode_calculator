"""Regression analysis."""
import math


class RegressionAnalyzer:
    @staticmethod
    def linear(x: list[float], y: list[float]) -> dict:
        RegressionAnalyzer._validate_data(x, y)
        n = len(x)
        sx = sum(x)
        sy = sum(y)
        sxx = sum(xi * xi for xi in x)
        sxy = sum(x[i] * y[i] for i in range(n))
        slope = (n * sxy - sx * sy) / (n * sxx - sx * sx) if (n * sxx - sx * sx) != 0 else 0
        intercept = (sy - slope * sx) / n
        y_mean = sy / n
        ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "equation": f"y = {slope:.4f}x + {intercept:.4f}",
        }

    @staticmethod
    def quadratic(x: list[float], y: list[float]) -> dict:
        RegressionAnalyzer._validate_data(x, y)
        n = len(x)
        sx = sum(x)
        sy = sum(y)
        sx2 = sum(xi ** 2 for xi in x)
        sx3 = sum(xi ** 3 for xi in x)
        sx4 = sum(xi ** 4 for xi in x)
        sxy = sum(x[i] * y[i] for i in range(n))
        sx2y = sum(x[i] ** 2 * y[i] for i in range(n))
        denom = n * (sx2 * sx4 - sx3 * sx3) - sx * (sx * sx4 - sx2 * sx3) + sx2 * (sx * sx3 - sx2 * sx2)
        if denom == 0:
            raise ValueError("Cannot fit quadratic (singular matrix)")
        a_num = n * (sx2 * sx2y - sx3 * sxy) - sx * (sx * sx2y - sx2 * sxy) + sx2 * (sx * sxy - sx2 * sy)
        b_num = n * (sx * sx2y - sx2 * sxy) - sx * (sx * sx2y - sx3 * sxy) + sx2 * (sx * sxy - sx2 * sy)
        # Actually solve properly with Cramer's rule
        det = denom
        a = (n * (sx2 * sx2y - sx3 * sxy) - sx * (sx * sx2y - sx2 * sxy) + sx2 * (sx * sxy - sx2 * sy)) / det
        c = (sx2 * (sx * sx2y - sx2 * sxy) - sx * (sx * sx2y - sx3 * sxy) + n * (sx * sxy - sx2 * sy)) / det
        # Solve for b:
        mat = [
            [n, sx, sx2],
            [sx, sx2, sx3],
            [sx2, sx3, sx4],
        ]
        rhs = [sy, sxy, sx2y]
        det_b = mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1]) \
                - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0]) \
                + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0])
        rhs_b = [rhs[0], rhs[1], rhs[2]]
        b_num2 = mat[0][0] * (rhs_b[1] * mat[2][2] - mat[1][2] * rhs_b[2]) \
                 - mat[0][1] * (rhs_b[0] * mat[2][2] - mat[1][2] * rhs_b[2]) \
                 + mat[0][2] * (rhs_b[0] * mat[2][1] - rhs_b[1] * mat[2][0])
        b = b_num2 / det_b if det_b != 0 else 0
        y_mean = sy / n
        ss_res = sum((y[i] - (a * x[i] ** 2 + b * x[i] + c)) ** 2 for i in range(n))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        return {
            "a": a,
            "b": b,
            "c": c,
            "r_squared": r_squared,
            "equation": f"y = {a:.4f}x\u00b2 + {b:.4f}x + {c:.4f}",
        }

    @staticmethod
    def predict(x: float, coefficients: dict) -> float:
        if "slope" in coefficients and "intercept" in coefficients:
            return coefficients["slope"] * x + coefficients["intercept"]
        if "a" in coefficients and "b" in coefficients and "c" in coefficients:
            return coefficients["a"] * x ** 2 + coefficients["b"] * x + coefficients["c"]
        raise ValueError("Unknown coefficient format")

    @staticmethod
    def r_squared(x: list[float], y: list[float], predict_func) -> float:
        RegressionAnalyzer._validate_data(x, y)
        y_mean = sum(y) / len(y)
        ss_res = sum((y[i] - predict_func(x[i])) ** 2 for i in range(len(y)))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(len(y)))
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    @staticmethod
    def _validate_data(x: list[float], y: list[float]) -> None:
        if not x or not y:
            raise ValueError("Data cannot be empty")
        if len(x) != len(y):
            raise ValueError(f"x and y must have same length, got {len(x)} and {len(y)}")
        if len(x) < 2:
            raise ValueError("Need at least 2 data points")
