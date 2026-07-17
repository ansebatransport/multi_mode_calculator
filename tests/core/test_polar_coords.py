import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import math
import unittest
from core.polar_coords import PolarCoords


class TestPolarCoordsCartesianToPolar(unittest.TestCase):
    def test_cartesian_to_polar_first_quadrant(self):
        r, theta = PolarCoords.cartesian_to_polar(1, 1)
        self.assertAlmostEqual(r, math.sqrt(2))
        self.assertAlmostEqual(theta, math.pi / 4)

    def test_cartesian_to_polar_origin(self):
        r, theta = PolarCoords.cartesian_to_polar(0, 0)
        self.assertAlmostEqual(r, 0.0)
        self.assertAlmostEqual(theta, 0.0)

    def test_cartesian_to_polar_negative_x(self):
        r, theta = PolarCoords.cartesian_to_polar(-1, 0)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(theta, math.pi)

    def test_cartesian_to_polar_negative_y(self):
        r, theta = PolarCoords.cartesian_to_polar(0, -1)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(theta, -math.pi / 2)

    def test_cartesian_to_polar_negative_both(self):
        r, theta = PolarCoords.cartesian_to_polar(-1, -1)
        self.assertAlmostEqual(r, math.sqrt(2))
        self.assertAlmostEqual(theta, -3 * math.pi / 4)


class TestPolarCoordsPolarToCartesian(unittest.TestCase):
    def test_polar_to_cartesian_first_quadrant(self):
        x, y = PolarCoords.polar_to_cartesian(1, math.pi / 4)
        self.assertAlmostEqual(x, math.sqrt(2) / 2)
        self.assertAlmostEqual(y, math.sqrt(2) / 2)

    def test_polar_to_cartesian_origin(self):
        x, y = PolarCoords.polar_to_cartesian(0, 0)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)

    def test_polar_to_cartesian_negative_r(self):
        x, y = PolarCoords.polar_to_cartesian(-1, 0)
        self.assertAlmostEqual(x, -1.0)
        self.assertAlmostEqual(y, 0.0)


class TestPolarCoordsRoundTrip(unittest.TestCase):
    def test_round_trip_quadrant1(self):
        x0, y0 = 3.0, 4.0
        r, theta = PolarCoords.cartesian_to_polar(x0, y0)
        x1, y1 = PolarCoords.polar_to_cartesian(r, theta)
        self.assertAlmostEqual(x0, x1)
        self.assertAlmostEqual(y0, y1)

    def test_round_trip_quadrant2(self):
        x0, y0 = -3.0, 4.0
        r, theta = PolarCoords.cartesian_to_polar(x0, y0)
        x1, y1 = PolarCoords.polar_to_cartesian(r, theta)
        self.assertAlmostEqual(x0, x1)
        self.assertAlmostEqual(y0, y1)

    def test_round_trip_quadrant3(self):
        x0, y0 = -3.0, -4.0
        r, theta = PolarCoords.cartesian_to_polar(x0, y0)
        x1, y1 = PolarCoords.polar_to_cartesian(r, theta)
        self.assertAlmostEqual(x0, x1)
        self.assertAlmostEqual(y0, y1)

    def test_round_trip_quadrant4(self):
        x0, y0 = 3.0, -4.0
        r, theta = PolarCoords.cartesian_to_polar(x0, y0)
        x1, y1 = PolarCoords.polar_to_cartesian(r, theta)
        self.assertAlmostEqual(x0, x1)
        self.assertAlmostEqual(y0, y1)


class TestPolarCoordsFormatPolar(unittest.TestCase):
    def test_format_polar(self):
        result = PolarCoords.format_polar(1.4142, 0.7854)
        self.assertEqual(result, "(1.4142, 0.7854)")


class TestPolarCoordsDistance(unittest.TestCase):
    def test_distance_same_point(self):
        d = PolarCoords.distance((1, 0), (1, 0))
        self.assertAlmostEqual(d, 0.0)

    def test_distance_opposite(self):
        d = PolarCoords.distance((1, 0), (1, math.pi))
        self.assertAlmostEqual(d, 2.0)


class TestPolarCoordsRotate(unittest.TestCase):
    def test_rotate_90_degrees(self):
        r, theta = PolarCoords.rotate(1, 0, math.pi / 2)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(theta, math.pi / 2)

    def test_rotate_full_circle(self):
        r, theta = PolarCoords.rotate(1, 0, 2 * math.pi)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(theta, 2 * math.pi)
