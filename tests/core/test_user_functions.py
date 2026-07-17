import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.user_functions import UserFunctionManager


class TestUserFunctionsCreate(unittest.TestCase):
    def setUp(self):
        self.manager = UserFunctionManager()

    def test_define_square(self):
        self.manager.define("f", ["x"], "x**2")
        result = self.manager.evaluate("f", [5])
        self.assertEqual(result, 25)

    def test_define_two_params(self):
        self.manager.define("g", ["x", "y"], "x + y")
        result = self.manager.evaluate("g", [3, 4])
        self.assertEqual(result, 7)

    def test_define_using_math(self):
        self.manager.define("h", ["x"], "math.sin(x)")
        result = self.manager.evaluate("h", [0])
        self.assertAlmostEqual(result, 0.0)

    def test_invalid_name_raises(self):
        with self.assertRaises(ValueError):
            self.manager.define("123bad", ["x"], "x")

    def test_no_params_raises(self):
        with self.assertRaises(ValueError):
            self.manager.define("f", [], "1")

    def test_invalid_param_name_raises(self):
        with self.assertRaises(ValueError):
            self.manager.define("f", ["1x"], "x")

    def test_invalid_expression_raises(self):
        with self.assertRaises(ValueError):
            self.manager.define("f", ["x"], "")

    def test_unsafe_name_raises(self):
        with self.assertRaises(ValueError):
            self.manager.define("f", ["x"], "__import__('os')")


class TestUserFunctionsEvaluate(unittest.TestCase):
    def setUp(self):
        self.manager = UserFunctionManager()
        self.manager.define("f", ["x"], "x**2")

    def test_evaluate_defined_func(self):
        result = self.manager.evaluate("f", [3])
        self.assertEqual(result, 9)

    def test_evaluate_undefined_func_raises(self):
        with self.assertRaises(ValueError):
            self.manager.evaluate("undefined", [1])

    def test_evaluate_wrong_arg_count_raises(self):
        with self.assertRaises(ValueError):
            self.manager.evaluate("f", [1, 2])


class TestUserFunctionsListDelete(unittest.TestCase):
    def setUp(self):
        self.manager = UserFunctionManager()
        self.manager.define("a", ["x"], "x")
        self.manager.define("b", ["x"], "x**2")

    def test_list_all(self):
        funcs = self.manager.list_all()
        self.assertIn("a", funcs)
        self.assertIn("b", funcs)
        self.assertEqual(funcs["a"]["expression"], "x")
        self.assertEqual(funcs["b"]["expression"], "x**2")

    def test_delete(self):
        self.manager.delete("a")
        self.assertNotIn("a", self.manager.list_all())

    def test_delete_undefined_raises(self):
        with self.assertRaises(ValueError):
            self.manager.delete("nonexistent")


class TestUserFunctionsEdit(unittest.TestCase):
    def setUp(self):
        self.manager = UserFunctionManager()
        self.manager.define("f", ["x"], "x")

    def test_edit_redefine(self):
        self.manager.define("f", ["x"], "x**3")
        self.assertEqual(self.manager.evaluate("f", [2]), 8)

    def test_edit_change_params(self):
        self.manager.define("f", ["a", "b"], "a * b")
        self.assertEqual(self.manager.evaluate("f", [4, 5]), 20)


class TestUserFunctionsGetMetadata(unittest.TestCase):
    def setUp(self):
        self.manager = UserFunctionManager()
        self.manager.define("f", ["x", "y"], "x + y")

    def test_get_params(self):
        params = self.manager.get_params("f")
        self.assertEqual(params, ["x", "y"])

    def test_get_expression(self):
        expr = self.manager.get_expression("f")
        self.assertEqual(expr, "x + y")

    def test_get_params_undefined_raises(self):
        with self.assertRaises(ValueError):
            self.manager.get_params("nonexistent")
