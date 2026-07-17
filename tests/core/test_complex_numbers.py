import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.complex_numbers import ComplexCalculator


class TestComplexCalculator(unittest.TestCase):
    def test_create(self):
        z = ComplexCalculator.create(3, 4)
        self.assertEqual(z, complex(3, 4))
        self.assertEqual(z.real, 3)
        self.assertEqual(z.imag, 4)

    def test_add(self):
        a = complex(3, 4)
        b = complex(1, 2)
        self.assertEqual(ComplexCalculator.add(a, b), complex(4, 6))

    def test_subtract(self):
        a = complex(5, 7)
        b = complex(2, 3)
        self.assertEqual(ComplexCalculator.subtract(a, b), complex(3, 4))

    def test_multiply(self):
        a = complex(2, 3)
        b = complex(1, -1)
        self.assertEqual(ComplexCalculator.multiply(a, b), complex(5, 1))

    def test_divide(self):
        a = complex(4, 2)
        b = complex(1, 1)
        result = ComplexCalculator.divide(a, b)
        self.assertAlmostEqual(result.real, 3)
        self.assertAlmostEqual(result.imag, -1)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            ComplexCalculator.divide(complex(1, 1), complex(0, 0))

    def test_magnitude(self):
        z = complex(3, 4)
        self.assertAlmostEqual(ComplexCalculator.magnitude(z), 5.0)

    def test_magnitude_zero(self):
        self.assertAlmostEqual(ComplexCalculator.magnitude(complex(0, 0)), 0.0)

    def test_phase(self):
        z = complex(1, 0)
        self.assertAlmostEqual(ComplexCalculator.phase(z), 0.0)
        z2 = complex(0, 1)
        self.assertAlmostEqual(ComplexCalculator.phase(z2), 1.5707963267948966)

    def test_phase_degrees(self):
        z = complex(0, 1)
        self.assertAlmostEqual(ComplexCalculator.phase(z, in_degrees=True), 90.0)

    def test_conjugate(self):
        z = complex(3, 4)
        self.assertEqual(ComplexCalculator.conjugate(z), complex(3, -4))

    def test_conjugate_real(self):
        z = complex(5, 0)
        self.assertEqual(ComplexCalculator.conjugate(z), complex(5, 0))

    def test_to_polar(self):
        z = complex(3, 4)
        r, theta = ComplexCalculator.to_polar(z)
        self.assertAlmostEqual(r, 5.0)
        self.assertAlmostEqual(theta, 0.9272952180016122)

    def test_from_polar(self):
        z = ComplexCalculator.from_polar(5, 0)
        self.assertAlmostEqual(z.real, 5.0)
        self.assertAlmostEqual(z.imag, 0.0)

    def test_polar_roundtrip(self):
        original = complex(3, 4)
        r, theta = ComplexCalculator.to_polar(original)
        result = ComplexCalculator.from_polar(r, theta)
        self.assertAlmostEqual(result.real, original.real)
        self.assertAlmostEqual(result.imag, original.imag)

    def test_add_negative_numbers(self):
        a = complex(-3, -4)
        b = complex(-1, -2)
        self.assertEqual(ComplexCalculator.add(a, b), complex(-4, -6))

    def test_multiply_by_zero(self):
        z = complex(5, 5)
        self.assertEqual(ComplexCalculator.multiply(z, complex(0, 0)), complex(0, 0))

    def test_format(self):
        z = complex(3, 4)
        result = ComplexCalculator.format(z)
        self.assertIn("3", result)
        self.assertIn("4", result)
        self.assertIn("i", result)


if __name__ == "__main__":
    unittest.main()
