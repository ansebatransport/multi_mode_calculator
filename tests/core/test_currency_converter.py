import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.currency_converter import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.converter = CurrencyConverter(cache_path=self.tmp.name)

    def tearDown(self):
        self.tmp.close()
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_usd_to_eur(self):
        result = self.converter.convert(100, "USD", "EUR")
        self.assertAlmostEqual(result, 85.0)

    def test_eur_to_usd(self):
        result = self.converter.convert(85, "EUR", "USD")
        self.assertAlmostEqual(result, 100.0)

    def test_inverse_rate(self):
        usd_to_eur = self.converter.convert(1, "USD", "EUR")
        eur_to_usd = self.converter.convert(1, "EUR", "USD")
        self.assertAlmostEqual(usd_to_eur * eur_to_usd, 1.0)

    def test_chain_conversion(self):
        usd_to_gbp = self.converter.convert(1, "USD", "GBP")
        gbp_to_jpy = self.converter.convert(1, "GBP", "JPY")
        usd_to_jpy_direct = self.converter.convert(1, "USD", "JPY")
        usd_to_jpy_chain = usd_to_gbp * gbp_to_jpy
        self.assertAlmostEqual(usd_to_jpy_chain, usd_to_jpy_direct)

    def test_same_currency(self):
        result = self.converter.convert(100, "USD", "USD")
        self.assertAlmostEqual(result, 100.0)

    def test_unknown_currency_from(self):
        with self.assertRaises(ValueError):
            self.converter.convert(100, "XYZ", "USD")

    def test_unknown_currency_to(self):
        with self.assertRaises(ValueError):
            self.converter.convert(100, "USD", "XYZ")

    def test_set_rate(self):
        self.converter.set_rate("XYZ", 2.0)
        self.assertEqual(self.converter.get_rate("XYZ"), 2.0)

    def test_set_rate_negative(self):
        with self.assertRaises(ValueError):
            self.converter.set_rate("XYZ", -1)

    def test_get_all_rates(self):
        rates = self.converter.get_all_rates()
        self.assertIn("USD", rates)
        self.assertIn("EUR", rates)

    def test_get_currencies(self):
        currencies = self.converter.get_currencies()
        self.assertIn("USD", currencies)
        self.assertEqual(currencies, sorted(currencies))

    def test_default_rates_loaded(self):
        self.assertIsNotNone(self.converter.get_rate("USD"))
        self.assertIsNotNone(self.converter.get_rate("EUR"))


if __name__ == "__main__":
    unittest.main()
