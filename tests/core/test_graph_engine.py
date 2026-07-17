import sys
import os
import unittest
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.graph_engine import GraphEngine, GraphViewport


class TestGraphViewport(unittest.TestCase):
    def test_creation_default(self):
        vp = GraphViewport()
        self.assertEqual(vp.x_min, -10)
        self.assertEqual(vp.x_max, 10)
        self.assertEqual(vp.y_min, -10)
        self.assertEqual(vp.y_max, 10)

    def test_creation_custom(self):
        vp = GraphViewport(-5, 5, -3, 3)
        self.assertEqual(vp.x_min, -5)
        self.assertEqual(vp.x_max, 5)
        self.assertEqual(vp.y_min, -3)
        self.assertEqual(vp.y_max, 3)

    def test_invalid_viewport(self):
        with self.assertRaises(ValueError):
            GraphViewport(10, 5, -10, 10)

    def test_x_range(self):
        vp = GraphViewport(-10, 10, -10, 10)
        self.assertEqual(vp.x_range(), 20)

    def test_y_range(self):
        vp = GraphViewport(-10, 10, -10, 10)
        self.assertEqual(vp.y_range(), 20)

    def test_zoom_in(self):
        vp = GraphViewport(-10, 10, -10, 10)
        vp.zoom_in(factor=2.0)
        self.assertAlmostEqual(vp.x_min, -5.0)
        self.assertAlmostEqual(vp.x_max, 5.0)
        self.assertAlmostEqual(vp.y_min, -5.0)
        self.assertAlmostEqual(vp.y_max, 5.0)

    def test_zoom_out(self):
        vp = GraphViewport(-10, 10, -10, 10)
        vp.zoom_out(factor=2.0)
        self.assertAlmostEqual(vp.x_min, -20.0)
        self.assertAlmostEqual(vp.x_max, 20.0)

    def test_zoom_in_invalid_factor(self):
        vp = GraphViewport()
        with self.assertRaises(ValueError):
            vp.zoom_in(factor=-1)

    def test_pan(self):
        vp = GraphViewport(-10, 10, -10, 10)
        vp.pan(5, -3)
        self.assertAlmostEqual(vp.x_min, -5.0)
        self.assertAlmostEqual(vp.x_max, 15.0)
        self.assertAlmostEqual(vp.y_min, -13.0)
        self.assertAlmostEqual(vp.y_max, 7.0)

    def test_reset(self):
        vp = GraphViewport(-5, 5, -3, 3)
        vp.pan(10, 10)
        vp.reset()
        self.assertEqual(vp.x_min, -5)
        self.assertEqual(vp.x_max, 5)
        self.assertEqual(vp.y_min, -3)
        self.assertEqual(vp.y_max, 3)


class TestGraphEngine(unittest.TestCase):
    def setUp(self):
        self.vp = GraphViewport(-10, 10, -10, 10)

    def test_sample_y_equals_x(self):
        points = GraphEngine.sample(lambda x: x, self.vp, num_points=5)
        self.assertEqual(len(points), 5)
        for x, y in points:
            self.assertAlmostEqual(x, y, places=10)

    def test_sample_constant_function(self):
        points = GraphEngine.sample(lambda x: 5, self.vp, num_points=10)
        self.assertEqual(len(points), 10)
        for x, y in points:
            self.assertAlmostEqual(y, 5.0, places=10)

    def test_sample_filters_nan(self):
        def bad_func(x):
            if x == 0:
                return float('nan')
            return x
        points = GraphEngine.sample(bad_func, self.vp, num_points=21)
        for x, y in points:
            self.assertFalse(math.isnan(y))

    def test_adaptive_sample_linear(self):
        points = GraphEngine.adaptive_sample(lambda x: x, self.vp, tolerance=0.5)
        self.assertGreater(len(points), 0)
        for x, y in points:
            self.assertAlmostEqual(x, y, places=5)

    def test_adaptive_sample_nonlinear(self):
        points = GraphEngine.adaptive_sample(
            lambda x: x**2, self.vp, tolerance=0.5
        )
        self.assertGreater(len(points), 2)

    def test_find_roots_y_x2_minus_4(self):
        roots = GraphEngine.find_roots(lambda x: x**2 - 4, self.vp)
        self.assertEqual(len(roots), 2)
        roots_sorted = sorted(roots)
        self.assertAlmostEqual(roots_sorted[0], -2.0, places=6)
        self.assertAlmostEqual(roots_sorted[1], 2.0, places=6)

    def test_find_roots_linear(self):
        roots = GraphEngine.find_roots(lambda x: x - 3, self.vp)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 3.0, places=6)

    def test_find_roots_no_roots(self):
        roots = GraphEngine.find_roots(lambda x: x**2 + 1, self.vp)
        self.assertEqual(len(roots), 0)

    def test_find_intersections_y_eq_x_and_y_eq_2(self):
        intersections = GraphEngine.find_intersections(
            lambda x: x, lambda x: 2, self.vp
        )
        self.assertEqual(len(intersections), 1)
        self.assertAlmostEqual(intersections[0][0], 2.0, places=6)
        self.assertAlmostEqual(intersections[0][1], 2.0, places=6)

    def test_find_extrema_sin(self):
        vp = GraphViewport(-2 * math.pi, 2 * math.pi, -2, 2)
        extrema = GraphEngine.find_extrema(math.sin, vp)
        self.assertGreater(len(extrema), 0)
        has_max = any(e[2] == "max" for e in extrema)
        has_min = any(e[2] == "min" for e in extrema)
        self.assertTrue(has_max)
        self.assertTrue(has_min)

    def test_find_extrema_cubic(self):
        extrema = GraphEngine.find_extrema(lambda x: x**3 - 3 * x, self.vp)
        self.assertGreater(len(extrema), 0)

    def test_sample_polar_circle(self):
        vp = GraphViewport(-3, 3, -3, 3)
        points = GraphEngine.sample_polar(lambda theta: 2, vp, num_points=200)
        self.assertGreater(len(points), 0)
        for x, y in points:
            dist = math.sqrt(x**2 + y**2)
            self.assertAlmostEqual(dist, 2.0, places=1)

    def test_sample_parametric_circle(self):
        x_func = lambda t: 3 * math.cos(t)
        y_func = lambda t: 3 * math.sin(t)
        vp = GraphViewport(-5, 5, -5, 5)
        points = GraphEngine.sample_parametric(x_func, y_func, 0, 2 * math.pi, 200)
        self.assertGreater(len(points), 0)
        for x, y in points:
            dist = math.sqrt(x**2 + y**2)
            self.assertAlmostEqual(dist, 3.0, places=1)

    def test_safe_eval_invalid_function(self):
        def raise_on_everything(x):
            raise ValueError("bad")
        result = GraphEngine._safe_eval(raise_on_everything, 1.0)
        self.assertIsNone(result)

    def test_safe_eval_returns_none(self):
        result = GraphEngine._safe_eval(lambda x: None, 1.0)
        self.assertIsNone(result)

    def test_safe_eval_infinite(self):
        result = GraphEngine._safe_eval(lambda x: float('inf'), 1.0)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
