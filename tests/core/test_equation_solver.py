import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.equation_solver import EquationSolver


class TestEquationSolver(unittest.TestCase):
    def test_linear(self):
        roots = EquationSolver.linear(2, -4)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 2.0)

    def test_linear_negative(self):
        roots = EquationSolver.linear(-3, 6)
        self.assertAlmostEqual(roots[0], 2.0)

    def test_linear_zero_a(self):
        with self.assertRaises(ValueError):
            EquationSolver.linear(0, 5)

    def test_quadratic_perfect_square(self):
        roots = EquationSolver.quadratic(1, 0, -4)
        values = sorted([r.real for r in roots])
        self.assertAlmostEqual(values[0], -2.0)
        self.assertAlmostEqual(values[1], 2.0)

    def test_quadratic_complex_roots(self):
        roots = EquationSolver.quadratic(1, 0, 1)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(abs(roots[0].imag), 1.0)
        self.assertAlmostEqual(abs(roots[1].imag), 1.0)

    def test_quadratic_double_root(self):
        roots = EquationSolver.quadratic(1, -4, 4)
        self.assertAlmostEqual(roots[0].real, 2.0)
        self.assertAlmostEqual(roots[1].real, 2.0)

    def test_quadratic_degenerate(self):
        with self.assertRaises(ValueError):
            EquationSolver.quadratic(0, 0, 5)

    def test_cubic(self):
        roots = EquationSolver.cubic(1, -6, 11, -6)
        real_roots = sorted([r.real for r in roots])
        self.assertAlmostEqual(real_roots[0], 1.0)
        self.assertAlmostEqual(real_roots[1], 2.0)
        self.assertAlmostEqual(real_roots[2], 3.0)

    def test_system_2x2(self):
        x, y = EquationSolver.solve_system_2x2(2, 3, 8, 1, -1, 1)
        self.assertAlmostEqual(x, 2.2)
        self.assertAlmostEqual(y, 1.2)

    def test_system_2x2_no_solution(self):
        with self.assertRaises(ValueError):
            EquationSolver.solve_system_2x2(1, 2, 3, 2, 4, 6)

    def test_system_3x3(self):
        coeffs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        constants = [2, 3, -1]
        result = EquationSolver.solve_system_3x3(coeffs, constants)
        self.assertAlmostEqual(result[0], 2.0)
        self.assertAlmostEqual(result[1], 3.0)
        self.assertAlmostEqual(result[2], -1.0)

    def test_system_3x3_singular(self):
        coeffs = [[1, 1, 1], [2, 2, 2], [1, 0, 1]]
        constants = [6, 12, 4]
        with self.assertRaises(ValueError):
            EquationSolver.solve_system_3x3(coeffs, constants)

    def test_format_roots(self):
        roots = [complex(1, 0), complex(2, 0)]
        result = EquationSolver.format_roots(roots)
        self.assertIn("1", result)
        self.assertIn("2", result)

    def test_format_roots_complex(self):
        roots = [complex(0, 1)]
        result = EquationSolver.format_roots(roots)
        self.assertIn("i", result)


if __name__ == "__main__":
    unittest.main()
