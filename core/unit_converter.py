"""Unit conversion across categories."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Unit:
    name: str
    symbol: str
    to_base: float
    category: str


UNITS: dict[str, list[Unit]] = {
    "Length": [
        Unit("Meter", "m", 1.0, "Length"),
        Unit("Kilometer", "km", 1000.0, "Length"),
        Unit("Centimeter", "cm", 0.01, "Length"),
        Unit("Millimeter", "mm", 0.001, "Length"),
        Unit("Mile", "mi", 1609.344, "Length"),
        Unit("Yard", "yd", 0.9144, "Length"),
        Unit("Foot", "ft", 0.3048, "Length"),
        Unit("Inch", "in", 0.0254, "Length"),
        Unit("Nautical Mile", "nmi", 1852.0, "Length"),
    ],
    "Weight": [
        Unit("Kilogram", "kg", 1.0, "Weight"),
        Unit("Gram", "g", 0.001, "Weight"),
        Unit("Milligram", "mg", 1e-6, "Weight"),
        Unit("Metric Ton", "t", 1000.0, "Weight"),
        Unit("Pound", "lb", 0.453592, "Weight"),
        Unit("Ounce", "oz", 0.0283495, "Weight"),
        Unit("Stone", "st", 6.35029, "Weight"),
    ],
    "Temperature": [
        Unit("Celsius", "°C", 1.0, "Temperature"),
        Unit("Fahrenheit", "°F", 1.0, "Temperature"),
        Unit("Kelvin", "K", 1.0, "Temperature"),
    ],
    "Area": [
        Unit("Square Meter", "m²", 1.0, "Area"),
        Unit("Square Kilometer", "km²", 1e6, "Area"),
        Unit("Square Mile", "mi²", 2589988.1, "Area"),
        Unit("Square Yard", "yd²", 0.836127, "Area"),
        Unit("Square Foot", "ft²", 0.092903, "Area"),
        Unit("Square Inch", "in²", 0.00064516, "Area"),
        Unit("Acre", "ac", 4046.86, "Area"),
        Unit("Hectare", "ha", 10000.0, "Area"),
    ],
    "Volume": [
        Unit("Liter", "L", 1.0, "Volume"),
        Unit("Milliliter", "mL", 0.001, "Volume"),
        Unit("Cubic Meter", "m³", 1000.0, "Volume"),
        Unit("Gallon (US)", "gal", 3.78541, "Volume"),
        Unit("Quart (US)", "qt", 0.946353, "Volume"),
        Unit("Pint (US)", "pt", 0.473176, "Volume"),
        Unit("Cup (US)", "cup", 0.236588, "Volume"),
        Unit("Fluid Ounce (US)", "fl oz", 0.0295735, "Volume"),
        Unit("Cubic Foot", "ft³", 28.3168, "Volume"),
    ],
    "Speed": [
        Unit("Meters per Second", "m/s", 1.0, "Speed"),
        Unit("Kilometers per Hour", "km/h", 0.277778, "Speed"),
        Unit("Miles per Hour", "mph", 0.44704, "Speed"),
        Unit("Knot", "kn", 0.514444, "Speed"),
    ],
    "Data Storage": [
        Unit("Byte", "B", 1.0, "Data Storage"),
        Unit("Kilobyte", "KB", 1024.0, "Data Storage"),
        Unit("Megabyte", "MB", 1048576.0, "Data Storage"),
        Unit("Gigabyte", "GB", 1073741824.0, "Data Storage"),
        Unit("Terabyte", "TB", 1099511627776.0, "Data Storage"),
        Unit("Petabyte", "PB", 1125899906842624.0, "Data Storage"),
        Unit("Bit", "bit", 0.125, "Data Storage"),
    ],
    "Time": [
        Unit("Second", "s", 1.0, "Time"),
        Unit("Millisecond", "ms", 0.001, "Time"),
        Unit("Minute", "min", 60.0, "Time"),
        Unit("Hour", "h", 3600.0, "Time"),
        Unit("Day", "d", 86400.0, "Time"),
        Unit("Week", "wk", 604800.0, "Time"),
        Unit("Month", "mo", 2629800.0, "Time"),
        Unit("Year", "yr", 31557600.0, "Time"),
    ],
    "Pressure": [
        Unit("Pascal", "Pa", 1.0, "Pressure"),
        Unit("Kilopascal", "kPa", 1000.0, "Pressure"),
        Unit("Bar", "bar", 100000.0, "Pressure"),
        Unit("Atmosphere", "atm", 101325.0, "Pressure"),
        Unit("PSI", "psi", 6894.76, "Pressure"),
        Unit("Millimeter of Mercury", "mmHg", 133.322, "Pressure"),
    ],
    "Energy": [
        Unit("Joule", "J", 1.0, "Energy"),
        Unit("Kilojoule", "kJ", 1000.0, "Energy"),
        Unit("Calorie", "cal", 4.184, "Energy"),
        Unit("Kilocalorie", "kcal", 4184.0, "Energy"),
        Unit("Watt Hour", "Wh", 3600.0, "Energy"),
        Unit("Kilowatt Hour", "kWh", 3600000.0, "Energy"),
        Unit("Electronvolt", "eV", 1.60218e-19, "Energy"),
        Unit("BTU", "BTU", 1055.06, "Energy"),
    ],
    "Angle": [
        Unit("Degree", "°", 1.0, "Angle"),
        Unit("Radian", "rad", 57.2958, "Angle"),
        Unit("Gradian", "grad", 0.9, "Angle"),
    ],
}


class UnitConverter:
    def __init__(self):
        self._units = UNITS

    def convert(self, value: float, from_unit: str, to_unit: str, category: str) -> float:
        if category == "Temperature":
            return self._convert_temperature(value, from_unit, to_unit)
        if category == "Angle":
            src = self.get_unit(from_unit, category)
            dst = self.get_unit(to_unit, category)
            if from_unit == to_unit:
                return value
            if from_unit == "Radian":
                return math.degrees(value) if to_unit == "Degree" else value * (200 / math.pi) if to_unit == "Gradian" else value
            if from_unit == "Gradian":
                return value * 0.9 if to_unit == "Degree" else math.radians(value * 0.9) if to_unit == "Radian" else value
            if from_unit == "Degree":
                return math.radians(value) if to_unit == "Radian" else value / 0.9 if to_unit == "Gradian" else value
            return value
        src = self.get_unit(from_unit, category)
        dst = self.get_unit(to_unit, category)
        base_value = value * src.to_base
        return base_value / dst.to_base

    def get_categories(self) -> list[str]:
        return list(self._units.keys())

    def get_units(self, category: str) -> list[Unit]:
        if category not in self._units:
            raise ValueError(f"Unknown category: {category}")
        return self._units[category]

    def get_unit(self, name: str, category: str) -> Unit:
        for unit in self.get_units(category):
            if unit.name == name or unit.symbol == name:
                return unit
        raise ValueError(f"Unknown unit '{name}' in category '{category}'")

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == to_unit:
            return value
        if from_unit in ("Celsius", "°C"):
            if to_unit in ("Fahrenheit", "°F"):
                return value * 9 / 5 + 32
            if to_unit in ("Kelvin", "K"):
                return value + 273.15
        elif from_unit in ("Fahrenheit", "°F"):
            if to_unit in ("Celsius", "°C"):
                return (value - 32) * 5 / 9
            if to_unit in ("Kelvin", "K"):
                return (value - 32) * 5 / 9 + 273.15
        elif from_unit in ("Kelvin", "K"):
            if to_unit in ("Celsius", "°C"):
                return value - 273.15
            if to_unit in ("Fahrenheit", "°F"):
                return (value - 273.15) * 9 / 5 + 32
        raise ValueError(f"Cannot convert {from_unit} to {to_unit}")
