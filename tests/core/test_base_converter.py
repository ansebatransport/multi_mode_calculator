import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.base_converter import BaseConverter


class TestBaseConverter(unittest.TestCase):

    def test_to_decimal_binary(self):
        self.assertEqual(BaseConverter.to_decimal("1010", 2), 10)

    def test_to_decimal_hex(self):
        self.assertEqual(BaseConverter.to_decimal("FF", 16), 255)

    def test_to_decimal_octal(self):
        self.assertEqual(BaseConverter.to_decimal("17", 8), 15)

    def test_to_decimal_decimal(self):
        self.assertEqual(BaseConverter.to_decimal("42", 10), 42)

    def test_to_decimal_negative(self):
        self.assertEqual(BaseConverter.to_decimal("-1010", 2), -10)

    def test_to_decimal_with_spaces(self):
        self.assertEqual(BaseConverter.to_decimal(" 1010 ", 2), 10)

    def test_from_decimal_binary(self):
        self.assertEqual(BaseConverter.from_decimal(10, 2), "1010")

    def test_from_decimal_hex(self):
        self.assertEqual(BaseConverter.from_decimal(255, 16), "FF")

    def test_from_decimal_octal(self):
        self.assertEqual(BaseConverter.from_decimal(15, 8), "17")

    def test_from_decimal_zero(self):
        self.assertEqual(BaseConverter.from_decimal(0, 2), "0")

    def test_from_decimal_negative(self):
        self.assertEqual(BaseConverter.from_decimal(-10, 2), "-1010")

    def test_hex_to_bin(self):
        self.assertEqual(BaseConverter.hex_to_bin("A"), "1010")

    def test_bin_to_hex(self):
        self.assertEqual(BaseConverter.bin_to_hex("11111111"), "FF")

    def test_oct_to_bin(self):
        self.assertEqual(BaseConverter.oct_to_bin("17"), "1111")

    def test_bin_to_oct(self):
        self.assertEqual(BaseConverter.bin_to_oct("11111111"), "377")

    def test_hex_to_oct(self):
        self.assertEqual(BaseConverter.hex_to_oct("FF"), "377")

    def test_oct_to_hex(self):
        self.assertEqual(BaseConverter.oct_to_hex("377"), "FF")

    def test_twos_complement_positive(self):
        self.assertEqual(BaseConverter.twos_complement(5, 8), "00000101")

    def test_twos_complement_negative(self):
        self.assertEqual(BaseConverter.twos_complement(-1, 8), "11111111")

    def test_twos_complement_negative_value(self):
        result = BaseConverter.twos_complement(-5, 8)
        self.assertEqual(len(result), 8)

    def test_sign_extend_positive(self):
        result = BaseConverter.sign_extend(0b00000101, 8)
        self.assertEqual(result, 5)

    def test_sign_extend_negative(self):
        result = BaseConverter.sign_extend(0b11111111, 8)
        self.assertEqual(result, -1)

    def test_to_all_bases(self):
        result = BaseConverter.to_all_bases(255)
        self.assertEqual(result["hex"], "FF")
        self.assertEqual(result["dec"], "255")
        self.assertEqual(result["oct"], "377")
        self.assertEqual(result["bin"], "11111111")

    def test_get_bit_length(self):
        self.assertEqual(BaseConverter.get_bit_length(0), 1)
        self.assertEqual(BaseConverter.get_bit_length(255), 8)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            BaseConverter.to_decimal("", 2)

    def test_invalid_base_too_low(self):
        with self.assertRaises(ValueError):
            BaseConverter.to_decimal("10", 1)

    def test_invalid_base_too_high(self):
        with self.assertRaises(ValueError):
            BaseConverter.to_decimal("10", 37)

    def test_invalid_digit_for_base(self):
        with self.assertRaises(ValueError):
            BaseConverter.to_decimal("FF", 2)

    def test_from_decimal_invalid_base(self):
        with self.assertRaises(ValueError):
            BaseConverter.from_decimal(10, 1)

    def test_twos_complement_out_of_range(self):
        with self.assertRaises(ValueError):
            BaseConverter.twos_complement(200, 8)

    def test_roundtrip_binary(self):
        for val in [0, 1, 42, 127, 255]:
            s = BaseConverter.from_decimal(val, 2)
            back = BaseConverter.to_decimal(s, 2)
            self.assertEqual(back, val)

    def test_roundtrip_hex(self):
        for val in [0, 1, 255, 4096, 65535]:
            s = BaseConverter.from_decimal(val, 16)
            back = BaseConverter.to_decimal(s, 16)
            self.assertEqual(back, val)


if __name__ == "__main__":
    unittest.main()
