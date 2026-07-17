import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import tempfile
import unittest
from core.autosave import AutoSave


class TestAutoSaveBasic(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.asv = AutoSave(save_path=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_save_and_load(self):
        self.asv.save("x", 10)
        self.assertEqual(self.asv.load("x"), 10)

    def test_load_default(self):
        self.assertIsNone(self.asv.load("missing"))
        self.assertEqual(self.asv.load("missing", "fallback"), "fallback")

    def test_save_multiple(self):
        self.asv.save("a", 1)
        self.asv.save("b", 2)
        self.asv.save("c", 3)
        self.assertEqual(self.asv.load("a"), 1)
        self.assertEqual(self.asv.load("b"), 2)
        self.assertEqual(self.asv.load("c"), 3)

    def test_save_overwrite(self):
        self.asv.save("x", 10)
        self.asv.save("x", 20)
        self.assertEqual(self.asv.load("x"), 20)


class TestAutoSaveSaveAll(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.asv = AutoSave(save_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_save_all(self):
        self.asv.save_all({"a": 1, "b": 2, "c": 3})
        self.assertEqual(self.asv.load("a"), 1)
        self.assertEqual(self.asv.load("b"), 2)
        self.assertEqual(self.asv.load("c"), 3)

    def test_load_all(self):
        self.asv.save("x", 10)
        self.asv.save("y", 20)
        result = self.asv.load_all()
        self.assertEqual(result, {"x": 10, "y": 20})

    def test_load_all_returns_copy(self):
        self.asv.save("x", 10)
        result = self.asv.load_all()
        result["x"] = 999
        self.assertEqual(self.asv.load("x"), 10)


class TestAutoSavePersistence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_persists_across_instances(self):
        asv1 = AutoSave(save_path=self.tmp.name)
        asv1.save("x", 42)
        asv1.save("y", "hello")
        asv2 = AutoSave(save_path=self.tmp.name)
        self.assertEqual(asv2.load("x"), 42)
        self.assertEqual(asv2.load("y"), "hello")

    def test_write_creates_valid_json(self):
        asv = AutoSave(save_path=self.tmp.name)
        asv.save("key", "value")
        with open(self.tmp.name, "r") as f:
            data = json.load(f)
        self.assertEqual(data["key"], "value")


class TestAutoSaveClear(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.asv = AutoSave(save_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_clear(self):
        self.asv.save("x", 10)
        self.asv.clear()
        self.assertEqual(self.asv.load_all(), {})

    def test_clear_writes_empty_file(self):
        self.asv.save("x", 10)
        self.asv.clear()
        with open(self.tmp.name, "r") as f:
            data = json.load(f)
        self.assertEqual(data, {})


class TestAutoSaveMissingFile(unittest.TestCase):
    def test_missing_file(self):
        path = tempfile.mktemp(suffix=".json")
        asv = AutoSave(save_path=path)
        self.assertEqual(asv.load_all(), {})
        self.assertIsNone(asv.load("anything"))
        if os.path.exists(path):
            os.unlink(path)


class TestAutoSaveCorruptFile(unittest.TestCase):
    def test_corrupt_file(self):
        path = tempfile.mktemp(suffix=".json")
        with open(path, "w") as f:
            f.write("NOT VALID JSON {{{")
        asv = AutoSave(save_path=path)
        self.assertEqual(asv.load_all(), {})
        os.unlink(path)


class TestAutoSaveVariedTypes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.asv = AutoSave(save_path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_varied_types(self):
        self.asv.save("string", "hello")
        self.asv.save("int", 42)
        self.asv.save("float", 3.14)
        self.asv.save("list", [1, 2, 3])
        self.asv.save("dict", {"nested": True})
        self.asv.save("bool", True)
        self.asv.save("none", None)
        self.assertEqual(self.asv.load("string"), "hello")
        self.assertEqual(self.asv.load("int"), 42)
        self.assertAlmostEqual(self.asv.load("float"), 3.14)
        self.assertEqual(self.asv.load("list"), [1, 2, 3])
        self.assertEqual(self.asv.load("dict"), {"nested": True})
        self.assertEqual(self.asv.load("bool"), True)
        self.assertIsNone(self.asv.load("none"))


if __name__ == "__main__":
    unittest.main()
