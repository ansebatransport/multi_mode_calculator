import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.variables import VariableManager


class TestVariableManagerSetAndGet(unittest.TestCase):
    def setUp(self):
        self.vm = VariableManager()

    def test_set_and_get(self):
        self.vm.set("x", 10)
        self.assertEqual(self.vm.get("x"), 10.0)

    def test_get_undefined_raises(self):
        with self.assertRaises(KeyError):
            self.vm.get("undefined")

    def test_set_overwrites(self):
        self.vm.set("x", 5)
        self.vm.set("x", 20)
        self.assertEqual(self.vm.get("x"), 20.0)

    def test_set_converts_to_float(self):
        self.vm.set("a", 3)
        self.assertIsInstance(self.vm.get("a"), float)

    def test_set_negative_value(self):
        self.vm.set("neg", -42)
        self.assertEqual(self.vm.get("neg"), -42.0)

    def test_set_zero(self):
        self.vm.set("zero", 0)
        self.assertEqual(self.vm.get("zero"), 0.0)

    def test_set_float_value(self):
        self.vm.set("pi_approx", 3.14)
        self.assertAlmostEqual(self.vm.get("pi_approx"), 3.14)


class TestVariableManagerListVariables(unittest.TestCase):
    def setUp(self):
        self.vm = VariableManager()

    def test_list_empty(self):
        self.assertEqual(self.vm.list_all(), {})

    def test_list_multiple(self):
        self.vm.set("x", 1)
        self.vm.set("y", 2)
        self.vm.set("z", 3)
        result = self.vm.list_all()
        self.assertEqual(result, {"x": 1.0, "y": 2.0, "z": 3.0})

    def test_list_returns_copy(self):
        self.vm.set("x", 1)
        result = self.vm.list_all()
        result["x"] = 999
        self.assertEqual(self.vm.get("x"), 1.0)


class TestVariableManagerDelete(unittest.TestCase):
    def setUp(self):
        self.vm = VariableManager()

    def test_delete(self):
        self.vm.set("x", 5)
        self.vm.delete("x")
        with self.assertRaises(KeyError):
            self.vm.get("x")

    def test_delete_undefined_raises(self):
        with self.assertRaises(KeyError):
            self.vm.delete("nope")

    def test_delete_others_remain(self):
        self.vm.set("a", 1)
        self.vm.set("b", 2)
        self.vm.delete("a")
        self.assertEqual(self.vm.get("b"), 2.0)
        with self.assertRaises(KeyError):
            self.vm.get("a")


class TestVariableManagerClearAll(unittest.TestCase):
    def setUp(self):
        self.vm = VariableManager()

    def test_clear_all(self):
        self.vm.set("x", 1)
        self.vm.set("y", 2)
        self.vm.clear()
        self.assertEqual(self.vm.list_all(), {})

    def test_clear_empty(self):
        self.vm.clear()
        self.assertEqual(self.vm.list_all(), {})


class TestVariableManagerValidation(unittest.TestCase):
    def test_valid_names(self):
        self.assertTrue(VariableManager.validate_name("x"))
        self.assertTrue(VariableManager.validate_name("abc123"))
        self.assertTrue(VariableManager.validate_name("X"))
        self.assertTrue(VariableManager.validate_name("my_var"))

    def test_invalid_names(self):
        self.assertFalse(VariableManager.validate_name(""))
        self.assertFalse(VariableManager.validate_name("123"))
        self.assertFalse(VariableManager.validate_name("_x"))
        self.assertFalse(VariableManager.validate_name("a b"))

    def test_set_invalid_name_raises(self):
        with self.assertRaises(ValueError):
            self.vm = VariableManager()
            self.vm.set("123bad", 1)


class TestVariableManagerSerialization(unittest.TestCase):
    def setUp(self):
        self.vm = VariableManager()

    def test_to_dict(self):
        self.vm.set("x", 10)
        self.vm.set("y", 20)
        result = self.vm.to_dict()
        self.assertEqual(result, {"variables": {"x": 10.0, "y": 20.0}})

    def test_from_dict(self):
        self.vm.from_dict({"variables": {"a": 1.0, "b": 2.0}})
        self.assertEqual(self.vm.get("a"), 1.0)
        self.assertEqual(self.vm.get("b"), 2.0)

    def test_from_dict_empty(self):
        self.vm.from_dict({})
        self.assertEqual(self.vm.list_all(), {})

    def test_round_trip(self):
        self.vm.set("x", 42)
        self.vm.set("y", 3.14)
        data = self.vm.to_dict()
        vm2 = VariableManager()
        vm2.from_dict(data)
        self.assertEqual(vm2.list_all(), self.vm.list_all())


if __name__ == "__main__":
    unittest.main()
