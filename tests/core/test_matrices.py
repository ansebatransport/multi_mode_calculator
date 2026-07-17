import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.matrices import MatrixCalculator


class TestMatrixCalculator(unittest.TestCase):
    def test_create_from_values(self):
        m = MatrixCalculator.create(2, 2, [1, 2, 3, 4])
        self.assertEqual(m, [[1, 2], [3, 4]])

    def test_create_zeros(self):
        m = MatrixCalculator.create(2, 3)
        self.assertEqual(m, [[0, 0, 0], [0, 0, 0]])

    def test_create_invalid_values_count(self):
        with self.assertRaises(ValueError):
            MatrixCalculator.create(2, 2, [1, 2, 3])

    def test_create_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            MatrixCalculator.create(0, 2)

    def test_identity(self):
        I = MatrixCalculator.identity(3)
        self.assertEqual(I, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_identity_1x1(self):
        I = MatrixCalculator.identity(1)
        self.assertEqual(I, [[1]])

    def test_add(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = MatrixCalculator.add(a, b)
        self.assertEqual(result, [[6, 8], [10, 12]])

    def test_subtract(self):
        a = [[5, 6], [7, 8]]
        b = [[1, 2], [3, 4]]
        result = MatrixCalculator.subtract(a, b)
        self.assertEqual(result, [[4, 4], [4, 4]])

    def test_add_dimension_mismatch(self):
        a = [[1, 2], [3, 4]]
        b = [[1, 2, 3]]
        with self.assertRaises(ValueError):
            MatrixCalculator.add(a, b)

    def test_multiply(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = MatrixCalculator.multiply(a, b)
        self.assertEqual(result, [[19, 22], [43, 50]])

    def test_multiply_identity(self):
        a = [[1, 2], [3, 4]]
        I = MatrixCalculator.identity(2)
        result = MatrixCalculator.multiply(a, I)
        self.assertEqual(result, a)

    def test_multiply_dimension_mismatch(self):
        a = [[1, 2, 3]]
        b = [[1], [2]]
        with self.assertRaises(ValueError):
            MatrixCalculator.multiply(a, b)

    def test_scalar_multiply(self):
        m = [[1, 2], [3, 4]]
        result = MatrixCalculator.scalar_multiply(m, 3)
        self.assertEqual(result, [[3, 6], [9, 12]])

    def test_transpose(self):
        m = [[1, 2, 3], [4, 5, 6]]
        result = MatrixCalculator.transpose(m)
        self.assertEqual(result, [[1, 4], [2, 5], [3, 6]])

    def test_transpose_square(self):
        m = [[1, 2], [3, 4]]
        result = MatrixCalculator.transpose(m)
        self.assertEqual(result, [[1, 3], [2, 4]])

    def test_determinant_2x2(self):
        m = [[1, 2], [3, 4]]
        self.assertAlmostEqual(MatrixCalculator.determinant(m), -2.0)

    def test_determinant_3x3(self):
        m = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
        self.assertAlmostEqual(MatrixCalculator.determinant(m), -306.0)

    def test_inverse_2x2(self):
        m = [[1, 2], [3, 4]]
        inv = MatrixCalculator.inverse(m)
        self.assertAlmostEqual(inv[0][0], -2.0)
        self.assertAlmostEqual(inv[0][1], 1.0)
        self.assertAlmostEqual(inv[1][0], 1.5)
        self.assertAlmostEqual(inv[1][1], -0.5)

    def test_inverse_times_original(self):
        m = [[2, 5], [1, 3]]
        inv = MatrixCalculator.inverse(m)
        product = MatrixCalculator.multiply(m, inv)
        I = MatrixCalculator.identity(2)
        for r in range(2):
            for c in range(2):
                self.assertAlmostEqual(product[r][c], I[r][c])

    def test_inverse_singular(self):
        m = [[1, 2], [2, 4]]
        with self.assertRaises(ValueError):
            MatrixCalculator.inverse(m)

    def test_inverse_3x3(self):
        m = [[2, 5, 3], [1, -2, -1], [1, 3, 2]]
        inv = MatrixCalculator.inverse(m)
        product = MatrixCalculator.multiply(m, inv)
        I = MatrixCalculator.identity(3)
        for r in range(3):
            for c in range(3):
                self.assertAlmostEqual(product[r][c], I[r][c], places=10)

    def test_determinant_1x1(self):
        m = [[5]]
        self.assertEqual(MatrixCalculator.determinant(m), 5.0)


if __name__ == "__main__":
    unittest.main()
