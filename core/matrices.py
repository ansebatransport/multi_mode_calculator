"""Matrix operations for 2x2 and 3x3 matrices."""
from typing import Union
import math

Matrix = list[list[float]]


class MatrixCalculator:
    @staticmethod
    def create(rows: int, cols: int, values: list[float] = None) -> Matrix:
        if rows < 1 or cols < 1:
            raise ValueError("Matrix dimensions must be positive")
        if values is None:
            return [[0.0] * cols for _ in range(rows)]
        if len(values) != rows * cols:
            raise ValueError(f"Expected {rows * cols} values, got {len(values)}")
        return [[values[r * cols + c] for c in range(cols)] for r in range(rows)]

    @staticmethod
    def identity(n: int) -> Matrix:
        if n < 1:
            raise ValueError("Size must be positive")
        return [[1.0 if r == c else 0.0 for c in range(n)] for r in range(n)]

    @staticmethod
    def add(a: Matrix, b: Matrix) -> Matrix:
        MatrixCalculator._validate_operation(a, b, "add")
        return [[a[r][c] + b[r][c] for c in range(len(a[0]))] for r in range(len(a))]

    @staticmethod
    def subtract(a: Matrix, b: Matrix) -> Matrix:
        MatrixCalculator._validate_operation(a, b, "subtract")
        return [[a[r][c] - b[r][c] for c in range(len(a[0]))] for r in range(len(a))]

    @staticmethod
    def multiply(a: Matrix, b: Matrix) -> Matrix:
        rows_a, cols_a = len(a), len(a[0])
        rows_b, cols_b = len(b), len(b[0])
        if cols_a != rows_b:
            raise ValueError(f"Cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}")
        result = [[0.0] * cols_b for _ in range(rows_a)]
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    @staticmethod
    def scalar_multiply(matrix: Matrix, scalar: float) -> Matrix:
        return [[matrix[r][c] * scalar for c in range(len(matrix[0]))] for r in range(len(matrix))]

    @staticmethod
    def determinant(matrix: Matrix) -> float:
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        if n == 3:
            a, b, c = matrix[0]
            d, e, f = matrix[1]
            g, h, i = matrix[2]
            return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        raise ValueError("Determinant only supported for 1x1, 2x2, 3x3 matrices")

    @staticmethod
    def inverse(matrix: Matrix) -> Matrix:
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        if n == 1:
            if matrix[0][0] == 0:
                raise ValueError("Matrix is singular")
            return [[1.0 / matrix[0][0]]]
        if n == 2:
            det = MatrixCalculator.determinant(matrix)
            if det == 0:
                raise ValueError("Matrix is singular")
            return [
                [matrix[1][1] / det, -matrix[0][1] / det],
                [-matrix[1][0] / det, matrix[0][0] / det],
            ]
        if n == 3:
            det = MatrixCalculator.determinant(matrix)
            if det == 0:
                raise ValueError("Matrix is singular")
            a, b, c = matrix[0]
            d, e, f = matrix[1]
            g, h, i = matrix[2]
            inv_det = 1.0 / det
            return [
                [(e * i - f * h) * inv_det, (c * h - b * i) * inv_det, (b * f - c * e) * inv_det],
                [(f * g - d * i) * inv_det, (a * i - c * g) * inv_det, (c * d - a * f) * inv_det],
                [(d * h - e * g) * inv_det, (b * g - a * h) * inv_det, (a * e - b * d) * inv_det],
            ]
        raise ValueError("Inverse only supported for 1x1, 2x2, 3x3 matrices")

    @staticmethod
    def transpose(matrix: Matrix) -> Matrix:
        rows, cols = len(matrix), len(matrix[0])
        return [[matrix[r][c] for r in range(rows)] for c in range(cols)]

    @staticmethod
    def rank(matrix: Matrix) -> int:
        m = [row[:] for row in matrix]
        rows, cols = len(m), len(m[0])
        r = 0
        for col in range(cols):
            pivot = None
            for row in range(r, rows):
                if abs(m[row][col]) > 1e-10:
                    pivot = row
                    break
            if pivot is None:
                continue
            m[r], m[pivot] = m[pivot], m[r]
            piv_val = m[r][col]
            for c in range(col, cols):
                m[r][c] /= piv_val
            for row in range(rows):
                if row != r and abs(m[row][col]) > 1e-10:
                    factor = m[row][col]
                    for c in range(col, cols):
                        m[row][c] -= factor * m[r][c]
            r += 1
            if r == rows:
                break
        return r

    @staticmethod
    def trace(matrix: Matrix) -> float:
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        return sum(matrix[i][i] for i in range(n))

    @staticmethod
    def format(matrix: Matrix, precision: int = 4) -> str:
        rows = []
        for row in matrix:
            formatted = [f"{v:.{precision}f}" for v in row]
            rows.append("[" + ", ".join(formatted) + "]")
        return "\n".join(rows)

    @staticmethod
    def _validate_operation(a: Matrix, b: Matrix, operation: str) -> None:
        if not a or not b:
            raise ValueError("Matrices cannot be empty")
        if len(a) != len(b) or len(a[0]) != len(b[0]):
            raise ValueError(f"Cannot {operation} matrices of different dimensions")
