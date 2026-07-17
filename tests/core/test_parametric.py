import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import math
import unittest
from core.parametric import ParametricEvaluator


class TestParametricEvaluate(unittest.TestCase):
    def test_evaluate_circle(self):
        x_func = lambda t: math.cos(t)
        y_func = lambda t: math.sin(t)
        x, y = ParametricEvaluator.evaluate(x_func, y_func, math.pi / 4)
        self.assertAlmostEqual(x, math.cos(math.pi / 4))
        self.assertAlmostEqual(y, math.sin(math.pi / 4))

    def test_evaluate_linear(self):
        x_func = lambda t: t
        y_func = lambda t: 2 * t
        x, y = ParametricEvaluator.evaluate(x_func, y_func, 3)
        self.assertEqual(x, 3)
        self.assertEqual(y, 6)


class TestParametricSample(unittest.TestCase):
    def test_sample_num_points(self):
        x_func = lambda t: math.cos(t)
        y_func = lambda t: math.sin(t)
        points = ParametricEvaluator.sample(x_func, y_func, 0, 2 * math.pi, 100)
        self.assertEqual(len(points), 100)

    def test_sample_circle_first_and_last(self):
        x_func = lambda t: math.cos(t)
        y_func = lambda t: math.sin(t)
        points = ParametricEvaluator.sample(x_func, y_func, 0, 2 * math.pi, 4)
        self.assertAlmostEqual(points[0][0], 1.0)
        self.assertAlmostEqual(points[0][1], 0.0)
        self.assertAlmostEqual(points[-1][0], 1.0, places=5)
        self.assertAlmostEqual(points[-1][1], 0.0, places=5)

    def test_sample_num_points_less_than_2_raises(self):
        with self.assertRaises(ValueError):
            ParametricEvaluator.sample(lambda t: t, lambda t: t, 0, 1, 1)

    def test_sample_lissajous_midpoint(self):
        x_func = lambda t: math.sin(2 * t)
        y_func = lambda t: math.sin(3 * t)
        points = ParametricEvaluator.sample(x_func, y_func, 0, 2 * math.pi, 50)
        self.assertTrue(len(points) > 0)

    def test_sample_handles_division_by_zero(self):
        x_func = lambda t: 1 / t if t != 0 else float("inf")
        y_func = lambda t: t
        points = ParametricEvaluator.sample(x_func, y_func, -1, 1, 10)
        self.assertTrue(len(points) > 0)

    def test_sample_discontinuity(self):
        x_func = lambda t: 0.0
        y_func = lambda t: 1 / (t - 2)
        points = ParametricEvaluator.sample(x_func, y_func, 0, 4, 10)
        self.assertTrue(len(points) > 0)


class TestParametricArcLength(unittest.TestCase):
    def test_arc_length_line(self):
        x_func = lambda t: t
        y_func = lambda t: 0
        length = ParametricEvaluator.arc_length(x_func, y_func, 0, 1, 100)
        self.assertAlmostEqual(length, 1.0, places=2)

    def test_arc_length_circle_quadrant(self):
        x_func = lambda t: math.cos(t)
        y_func = lambda t: math.sin(t)
        length = ParametricEvaluator.arc_length(x_func, y_func, 0, math.pi / 2, 1000)
        self.assertAlmostEqual(length, math.pi / 2, places=2)


class TestParametricTangentSlope(unittest.TestCase):
    def test_tangent_slope_line(self):
        x_func = lambda t: t
        y_func = lambda t: 2 * t
        slope = ParametricEvaluator.tangent_slope(x_func, y_func, 1)
        self.assertAlmostEqual(slope, 2.0, places=4)

    def test_tangent_slope_circle(self):
        x_func = lambda t: math.cos(t)
        y_func = lambda t: math.sin(t)
        slope = ParametricEvaluator.tangent_slope(x_func, y_func, 0)
        self.assertAlmostEqual(slope, float("inf"), places=4)

    def test_tangent_slope_vertical(self):
        x_func = lambda t: 0.0
        y_func = lambda t: t
        slope = ParametricEvaluator.tangent_slope(x_func, y_func, 1)
        self.assertEqual(slope, float("inf"))


class TestParametricSpeed(unittest.TestCase):
    def test_speed_constant(self):
        x_func = lambda t: t
        y_func = lambda t: 0
        speed = ParametricEvaluator.speed(x_func, y_func, 1)
        self.assertAlmostEqual(speed, 1.0, places=4)

    def test_speed_circle(self):
        x_func = lambda t: 2 * math.cos(t)
        y_func = lambda t: 2 * math.sin(t)
        speed = ParametricEvaluator.speed(x_func, y_func, 0)
        self.assertAlmostEqual(speed, 2.0, places=4)
