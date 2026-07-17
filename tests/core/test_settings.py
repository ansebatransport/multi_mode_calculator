import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import tempfile
import unittest
from core.settings import SettingsManager, Settings, AngleMode, NumberBase, DisplayFormat


class TestSettingsDefaults(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.mgr = SettingsManager(persist_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_default_angle_mode(self):
        self.assertEqual(self.mgr.get("angle_mode"), "degrees")

    def test_default_number_base(self):
        self.assertEqual(self.mgr.get("number_base"), 10)

    def test_default_display_format(self):
        self.assertEqual(self.mgr.get("display_format"), "standard")

    def test_default_decimal_places(self):
        self.assertEqual(self.mgr.get("decimal_places"), 10)

    def test_default_theme(self):
        self.assertEqual(self.mgr.get("theme"), "dark")

    def test_get_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.mgr.get("nonexistent")

    def test_set_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.mgr.set("nonexistent", "value")


class TestSettingsAngleMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.mgr = SettingsManager(persist_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_change_to_radians(self):
        self.mgr.set("angle_mode", "radians")
        self.assertEqual(self.mgr.angle_mode, "radians")

    def test_change_to_gradians(self):
        self.mgr.set("angle_mode", "gradians")
        self.assertEqual(self.mgr.angle_mode, "gradians")


class TestSettingsNumberBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.mgr = SettingsManager(persist_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_change_to_hex(self):
        self.mgr.set("number_base", 16)
        self.assertEqual(self.mgr.get("number_base"), 16)

    def test_change_to_binary(self):
        self.mgr.set("number_base", 2)
        self.assertEqual(self.mgr.get("number_base"), 2)

    def test_change_to_octal(self):
        self.mgr.set("number_base", 8)
        self.assertEqual(self.mgr.get("number_base"), 8)


class TestSettingsDisplayFormat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.mgr = SettingsManager(persist_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_change_to_scientific(self):
        self.mgr.set("display_format", "scientific")
        self.assertEqual(self.mgr.display_format, "scientific")

    def test_change_to_engineering(self):
        self.mgr.set("display_format", "engineering")
        self.assertEqual(self.mgr.display_format, "engineering")

    def test_change_to_fraction(self):
        self.mgr.set("display_format", "fraction")
        self.assertEqual(self.mgr.display_format, "fraction")


class TestSettingsReset(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.mgr = SettingsManager(persist_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_reset_to_defaults(self):
        self.mgr.set("angle_mode", "radians")
        self.mgr.set("display_format", "scientific")
        self.mgr.reset()
        self.assertEqual(self.mgr.angle_mode, "degrees")
        self.assertEqual(self.mgr.display_format, "standard")


class TestSettingsPersistence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_save_and_load(self):
        mgr = SettingsManager(persist_path=self.tmp.name)
        mgr.set("angle_mode", "radians")
        mgr.set("display_format", "scientific")
        mgr2 = SettingsManager(persist_path=self.tmp.name)
        self.assertEqual(mgr2.angle_mode, "radians")
        self.assertEqual(mgr2.display_format, "scientific")


class TestSettingsToDict(unittest.TestCase):
    def test_to_dict_contains_keys(self):
        settings = Settings()
        from dataclasses import asdict
        d = asdict(settings)
        self.assertIn("angle_mode", d)
        self.assertIn("number_base", d)
        self.assertIn("display_format", d)
        self.assertIn("theme", d)


if __name__ == "__main__":
    unittest.main()
