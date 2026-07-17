import sys
import os
import math
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.unit_converter import UnitConverter


class TestUnitConverter(unittest.TestCase):
    def setUp(self):
        self.converter = UnitConverter()

    def test_meters_to_feet(self):
        result = self.converter.convert(1, "Meter", "Foot", "Length")
        self.assertAlmostEqual(result, 3.28084, places=3)

    def test_kg_to_pounds(self):
        result = self.converter.convert(1, "Kilogram", "Pound", "Weight")
        self.assertAlmostEqual(result, 2.20462, places=3)

    def test_celsius_to_fahrenheit(self):
        result = self.converter.convert(100, "Celsius", "Fahrenheit", "Temperature")
        self.assertAlmostEqual(result, 212.0)

    def test_fahrenheit_to_celsius(self):
        result = self.converter.convert(32, "Fahrenheit", "Celsius", "Temperature")
        self.assertAlmostEqual(result, 0.0)

    def test_celsius_to_kelvin(self):
        result = self.converter.convert(0, "Celsius", "Kelvin", "Temperature")
        self.assertAlmostEqual(result, 273.15)

    def test_kelvin_to_celsius(self):
        result = self.converter.convert(273.15, "Kelvin", "Celsius", "Temperature")
        self.assertAlmostEqual(result, 0.0)

    def test_liters_to_gallons(self):
        result = self.converter.convert(1, "Liter", "Gallon (US)", "Volume")
        self.assertAlmostEqual(result, 0.26417, places=3)

    def test_sq_meters_to_sq_feet(self):
        result = self.converter.convert(1, "Square Meter", "Square Foot", "Area")
        self.assertAlmostEqual(result, 10.7639, places=2)

    def test_kmh_to_mph(self):
        result = self.converter.convert(100, "Kilometers per Hour", "Miles per Hour", "Speed")
        self.assertAlmostEqual(result, 62.1371, places=2)

    def test_same_unit(self):
        result = self.converter.convert(42, "Meter", "Meter", "Length")
        self.assertAlmostEqual(result, 42.0)

    def test_unknown_unit(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, "Furlong", "Meter", "Length")

    def test_unknown_category(self):
        with self.assertRaises(ValueError):
            self.converter.get_units("Nonexistent")

    def test_get_categories(self):
        cats = self.converter.get_categories()
        self.assertIn("Length", cats)
        self.assertIn("Temperature", cats)

    def test_celsius_to_fahrenheit_zero(self):
        result = self.converter.convert(0, "Celsius", "Fahrenheit", "Temperature")
        self.assertAlmostEqual(result, 32.0)


if __name__ == "__main__":
    unittest.main()
