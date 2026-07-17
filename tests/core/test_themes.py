import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import unittest
from unittest.mock import patch
from core.themes import ThemeManager


class TestThemeManagerDefault(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'):
            self.manager = ThemeManager(default_theme="dark")

    def test_default_theme_is_dark(self):
        self.assertEqual(self.manager.current, "dark")

    def test_default_theme_light(self):
        with patch.object(ThemeManager, '_load'):
            manager = ThemeManager(default_theme="light")
        self.assertEqual(manager.current, "light")


class TestThemeManagerToggle(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'), patch.object(ThemeManager, '_save'):
            self.manager = ThemeManager()

    def test_toggle_dark_to_light(self):
        self.manager._current_theme = "dark"
        result = self.manager.toggle()
        self.assertEqual(result, "light")
        self.assertEqual(self.manager.current, "light")

    def test_toggle_light_to_dark(self):
        self.manager._current_theme = "light"
        result = self.manager.toggle()
        self.assertEqual(result, "dark")
        self.assertEqual(self.manager.current, "dark")


class TestThemeManagerGetColor(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'):
            self.manager = ThemeManager()

    def test_get_existing_color_dark(self):
        color = self.manager.get_color("bg")
        self.assertEqual(color, "#1e1e2e")

    def test_get_color_light(self):
        self.manager._current_theme = "light"
        color = self.manager.get_color("bg")
        self.assertEqual(color, "#f5f5f5")

    def test_get_missing_color_returns_fallback(self):
        color = self.manager.get_color("nonexistent")
        self.assertEqual(color, "#ffffff")


class TestThemeManagerSetTheme(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'), patch.object(ThemeManager, '_save'):
            self.manager = ThemeManager()

    def test_set_valid_theme(self):
        self.manager.set_theme("light")
        self.assertEqual(self.manager.current, "light")

    def test_set_invalid_theme_raises(self):
        with self.assertRaises(ValueError):
            self.manager.set_theme("neon")

    def test_set_unknown_theme_raises(self):
        with self.assertRaises(ValueError):
            self.manager.set_theme("")


class TestThemeManagerCustomThemes(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'):
            self.manager = ThemeManager()

    def test_register_custom_theme(self):
        palette = {"bg": "#000000", "text": "#ffffff"}
        self.manager.register_custom_theme("custom", palette)
        self.manager.set_theme("custom")
        self.assertEqual(self.manager.get_color("bg"), "#000000")
        self.assertEqual(self.manager.get_color("text"), "#ffffff")

    def test_custom_theme_missing_color(self):
        palette = {"bg": "#000000"}
        self.manager.register_custom_theme("custom", palette)
        self.manager.set_theme("custom")
        self.assertEqual(self.manager.get_color("nonexistent"), "#ffffff")


class TestThemeManagerPersistence(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'), patch.object(ThemeManager, '_save'):
            self.manager = ThemeManager()

    def test_to_dict(self):
        d = {"theme": self.manager.current}
        self.assertEqual(d["theme"], "dark")

    def test_from_dict(self):
        self.manager._current_theme = "light"
        self.assertEqual(self.manager.current, "light")


class TestThemeManagerGetPalette(unittest.TestCase):
    def setUp(self):
        with patch.object(ThemeManager, '_load'):
            self.manager = ThemeManager()

    def test_get_palette_dark_has_keys(self):
        palette = self.manager.get_palette()
        self.assertIn("bg", palette)
        self.assertIn("text", palette)
        self.assertIn("accent", palette)

    def test_get_palette_light(self):
        self.manager._current_theme = "light"
        palette = self.manager.get_palette()
        self.assertEqual(palette["bg"], "#f5f5f5")
