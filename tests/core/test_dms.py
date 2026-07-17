import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.dms import DMSConverter


class TestDMSToDecimal(unittest.TestCase):
    def test_150_5(self):
        d, m, s = 150, 30, 0
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertAlmostEqual(result, 150.5)

    def test_45_30_15(self):
        d, m, s = 45, 30, 15
        result = DMSConverter.dms_to_decimal(d, m, s)
        expected = 45 + 30/60 + 15/3600
        self.assertAlmostEqual(result, expected, places=4)

    def test_zero(self):
        result = DMSConverter.dms_to_decimal(0, 0, 0)
        self.assertEqual(result, 0)

    def test_360(self):
        result = DMSConverter.dms_to_decimal(360, 0, 0)
        self.assertEqual(result, 360)

    def test_minutes_only(self):
        result = DMSConverter.dms_to_decimal(0, 30, 0)
        self.assertAlmostEqual(result, 0.5)

    def test_seconds_only(self):
        result = DMSConverter.dms_to_decimal(0, 0, 30)
        self.assertAlmostEqual(result, 30/3600)

    def test_invalid_minutes_high(self):
        with self.assertRaises(ValueError):
            DMSConverter.dms_to_decimal(0, 60, 0)

    def test_invalid_minutes_negative(self):
        with self.assertRaises(ValueError):
            DMSConverter.dms_to_decimal(0, -1, 0)

    def test_invalid_seconds_high(self):
        with self.assertRaises(ValueError):
            DMSConverter.dms_to_decimal(0, 0, 60)

    def test_invalid_seconds_negative(self):
        with self.assertRaises(ValueError):
            DMSConverter.dms_to_decimal(0, 0, -1)


class TestDecimalToDMS(unittest.TestCase):
    def test_150_5(self):
        d, m, s = DMSConverter.decimal_to_dms(150.5)
        self.assertEqual(d, 150)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 0)

    def test_45(self):
        d, m, s = DMSConverter.decimal_to_dms(45.0)
        self.assertEqual(d, 45)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 0)

    def test_zero(self):
        d, m, s = DMSConverter.decimal_to_dms(0.0)
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 0)

    def test_360(self):
        d, m, s = DMSConverter.decimal_to_dms(360.0)
        self.assertEqual(d, 360)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 0)

    def test_fractional(self):
        d, m, s = DMSConverter.decimal_to_dms(0.5)
        self.assertEqual(d, 0)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 0)

    def test_complex(self):
        d, m, s = DMSConverter.decimal_to_dms(45.5138888889)
        self.assertEqual(d, 45)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 50, delta=1)


class TestDMSRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        original = 150.5
        d, m, s = DMSConverter.decimal_to_dms(original)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertAlmostEqual(result, original, places=4)

    def test_round_trip_complex(self):
        original = 45 + 30/60 + 15/3600
        d, m, s = DMSConverter.decimal_to_dms(original)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertAlmostEqual(result, original, places=4)

    def test_round_trip_zero(self):
        d, m, s = DMSConverter.decimal_to_dms(0.0)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertEqual(result, 0)

    def test_round_trip_360(self):
        d, m, s = DMSConverter.decimal_to_dms(360.0)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertEqual(result, 360)


class TestDMSNegativeAngles(unittest.TestCase):
    def test_negative_decimal(self):
        d, m, s = DMSConverter.decimal_to_dms(-150.5)
        self.assertEqual(d, -150)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 0)

    def test_negative_dms_to_decimal(self):
        result = DMSConverter.dms_to_decimal(-150, 30, 0)
        self.assertAlmostEqual(result, -150.5)

    def test_negative_round_trip(self):
        original = -45.75
        d, m, s = DMSConverter.decimal_to_dms(original)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertAlmostEqual(result, original, places=4)


class TestDMSFormat(unittest.TestCase):
    def test_format(self):
        result = DMSConverter.format_dms(150, 30, 0)
        self.assertEqual(result, "150\u00b0 30' 0\"")

    def test_format_complex(self):
        result = DMSConverter.format_dms(45, 30, 15)
        self.assertEqual(result, "45\u00b0 30' 15\"")

    def test_format_zero(self):
        result = DMSConverter.format_dms(0, 0, 0)
        self.assertEqual(result, "0\u00b0 0' 0\"")

    def test_format_invalid_minutes(self):
        with self.assertRaises(ValueError):
            DMSConverter.format_dms(0, 60, 0)

    def test_format_invalid_seconds(self):
        with self.assertRaises(ValueError):
            DMSConverter.format_dms(0, 0, 60)


class TestDMSParse(unittest.TestCase):
    def test_parse_standard(self):
        d, m, s = DMSConverter.parse_dms("150\u00b0 30' 0\"")
        self.assertEqual(d, 150)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 0)

    def test_parse_complex(self):
        d, m, s = DMSConverter.parse_dms("45\u00b0 30' 15\"")
        self.assertEqual(d, 45)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 15)

    def test_parse_with_d(self):
        d, m, s = DMSConverter.parse_dms("45d 30m 15s")
        self.assertEqual(d, 45)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 15)

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            DMSConverter.parse_dms("invalid")

    def test_parse_fractional_seconds(self):
        d, m, s = DMSConverter.parse_dms("45\u00b0 30' 15.5\"")
        self.assertEqual(d, 45)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 15.5)


class TestDMSEdgeCases(unittest.TestCase):
    def test_zero_decimal(self):
        d, m, s = DMSConverter.decimal_to_dms(0)
        self.assertEqual((d, m, s), (0, 0, 0))

    def test_zero_dms_to_decimal(self):
        result = DMSConverter.dms_to_decimal(0, 0, 0)
        self.assertEqual(result, 0)

    def test_360_round_trip(self):
        d, m, s = DMSConverter.decimal_to_dms(360)
        result = DMSConverter.dms_to_decimal(d, m, s)
        self.assertEqual(result, 360)

    def test_very_small_angle(self):
        d, m, s = DMSConverter.decimal_to_dms(0.001)
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 3.6, delta=0.1)

    def test_very_large_angle(self):
        d, m, s = DMSConverter.decimal_to_dms(720.5)
        self.assertEqual(d, 720)
        self.assertEqual(m, 30)
        self.assertAlmostEqual(s, 0)


if __name__ == "__main__":
    unittest.main()
