import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from core.constants_lib import ConstantsLibrary, Constant, CONSTANTS_LIBRARY


class TestConstantsLibraryGetByName(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_get_by_name_speed_of_light(self):
        c = self.lib.get_by_name("Speed of Light")
        self.assertAlmostEqual(c.value, 299792458)

    def test_get_by_name_planck_constant(self):
        c = self.lib.get_by_name("Planck's Constant")
        self.assertAlmostEqual(c.value, 6.62607015e-34)

    def test_get_by_name_case_insensitive(self):
        c = self.lib.get_by_name("speed of light")
        self.assertAlmostEqual(c.value, 299792458)

    def test_get_by_name_not_found(self):
        with self.assertRaises(KeyError):
            self.lib.get_by_name("Nonexistent Constant")

    def test_get_by_name_pi(self):
        c = self.lib.get_by_name("Pi")
        self.assertAlmostEqual(c.value, 3.141592653589793, places=10)

    def test_get_by_name_avogadro(self):
        c = self.lib.get_by_name("Avogadro's Number")
        self.assertAlmostEqual(c.value, 6.02214076e23)


class TestConstantsLibraryGetBySymbol(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_get_by_symbol_pi(self):
        c = self.lib.get_by_symbol("\u03c0")
        self.assertAlmostEqual(c.value, 3.141592653589793, places=10)

    def test_get_by_symbol_speed_of_light(self):
        c = self.lib.get_by_symbol("c")
        self.assertAlmostEqual(c.value, 299792458)

    def test_get_by_symbol_not_found(self):
        with self.assertRaises(KeyError):
            self.lib.get_by_symbol("NONEXISTENT")


class TestConstantsLibraryCategories(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_get_categories(self):
        cats = self.lib.get_categories()
        self.assertIn("Mathematical", cats)
        self.assertIn("Physical", cats)
        self.assertIn("Chemical", cats)
        self.assertIn("Astronomical", cats)
        self.assertIn("Engineering", cats)

    def test_get_by_category_physical(self):
        phys = self.lib.get_by_category("Physical")
        self.assertGreater(len(phys), 0)
        values = [c.name for c in phys]
        self.assertIn("Speed of Light", values)
        self.assertIn("Planck's Constant", values)

    def test_get_by_category_not_found(self):
        with self.assertRaises(KeyError):
            self.lib.get_by_category("Nonexistent")

    def test_get_by_category_mathematical(self):
        math_consts = self.lib.get_by_category("Mathematical")
        self.assertGreater(len(math_consts), 0)


class TestConstantsLibrarySearch(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_search_by_name(self):
        results = self.lib.search("speed")
        self.assertGreater(len(results), 0)
        names = [c.name for c in results]
        self.assertIn("Speed of Light", names)

    def test_search_by_symbol(self):
        results = self.lib.search("pi")
        self.assertGreater(len(results), 0)

    def test_search_no_results(self):
        results = self.lib.search("zzznonexistent")
        self.assertEqual(len(results), 0)

    def test_search_case_insensitive(self):
        results = self.lib.search("LIGHT")
        self.assertGreater(len(results), 0)

    def test_search_by_category(self):
        results = self.lib.search("Physical")
        self.assertGreater(len(results), 0)


class TestConstantsLibraryGetAll(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_get_all(self):
        all_consts = self.lib.get_all()
        self.assertEqual(len(all_consts), len(CONSTANTS_LIBRARY))

    def test_get_all_returns_list_of_constants(self):
        all_consts = self.lib.get_all()
        for c in all_consts:
            self.assertIsInstance(c, Constant)


class TestConstantValues(unittest.TestCase):
    def setUp(self):
        self.lib = ConstantsLibrary()

    def test_speed_of_light_value(self):
        c = self.lib.get_by_name("Speed of Light")
        self.assertEqual(c.value, 299792458)
        self.assertEqual(c.unit, "m/s")
        self.assertEqual(c.symbol, "c")

    def test_planck_constant_value(self):
        c = self.lib.get_by_name("Planck's Constant")
        self.assertAlmostEqual(c.value, 6.62607015e-34)
        self.assertEqual(c.symbol, "h")

    def test_gravitational_constant_value(self):
        c = self.lib.get_by_name("Gravitational Constant")
        self.assertAlmostEqual(c.value, 6.6743e-11)

    def test_boltzmann_constant_value(self):
        c = self.lib.get_by_name("Boltzmann Constant")
        self.assertAlmostEqual(c.value, 1.380649e-23)

    def test_euler_number_value(self):
        c = self.lib.get_by_name("Euler's Number")
        self.assertAlmostEqual(c.value, 2.718281828459045, places=10)

    def test_golden_ratio_value(self):
        c = self.lib.get_by_name("Golden Ratio")
        self.assertAlmostEqual(c.value, 1.618033988749895, places=10)

    def test_standard_gravity_value(self):
        c = self.lib.get_by_name("Standard Gravity")
        self.assertAlmostEqual(c.value, 9.80665)


class TestConstantDataclass(unittest.TestCase):
    def test_constant_is_frozen(self):
        c = Constant("Test", "T", 1.0, "u", "Cat")
        with self.assertRaises(AttributeError):
            c.value = 2.0


if __name__ == "__main__":
    unittest.main()
