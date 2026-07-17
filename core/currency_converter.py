"""Currency conversion with offline caching."""
import json
import os
from datetime import datetime
from typing import Optional


class CurrencyConverter:
    DEFAULT_RATES = {
        "USD": 1.0, "EUR": 0.85, "GBP": 0.73, "JPY": 110.0,
        "CAD": 1.25, "AUD": 1.35, "CHF": 0.92, "CNY": 6.45,
        "INR": 74.5, "BRL": 5.2, "KRW": 1150.0, "MXN": 20.0,
    }

    def __init__(self, cache_path: str = None):
        self._cache_path = cache_path or os.path.expanduser("~/.calc_currency.json")
        self._rates: dict[str, float] = self.DEFAULT_RATES.copy()
        self._last_updated: Optional[str] = None
        self._load_cache()

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        if from_currency not in self._rates:
            raise ValueError(f"Unknown currency: {from_currency}")
        if to_currency not in self._rates:
            raise ValueError(f"Unknown currency: {to_currency}")
        usd_amount = amount / self._rates[from_currency]
        return usd_amount * self._rates[to_currency]

    def set_rate(self, currency: str, rate: float) -> None:
        if rate <= 0:
            raise ValueError("Rate must be positive")
        self._rates[currency.upper()] = rate
        self._save_cache()

    def get_rate(self, currency: str) -> Optional[float]:
        return self._rates.get(currency.upper())

    def get_all_rates(self) -> dict[str, float]:
        return self._rates.copy()

    def get_currencies(self) -> list[str]:
        return sorted(self._rates.keys())

    def _load_cache(self) -> None:
        try:
            if os.path.exists(self._cache_path):
                with open(self._cache_path, "r") as f:
                    data = json.load(f)
                self._rates.update(data.get("rates", {}))
                self._last_updated = data.get("last_updated")
        except (json.JSONDecodeError, IOError):
            pass

    def _save_cache(self) -> None:
        try:
            data = {
                "rates": self._rates,
                "last_updated": datetime.now().isoformat(),
            }
            with open(self._cache_path, "w") as f:
                json.dump(data, f)
            self._last_updated = data["last_updated"]
        except IOError:
            pass
