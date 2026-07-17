"""Physical and mathematical constants library."""

__all__ = ["Constant", "CONSTANTS_LIBRARY", "ConstantsLibrary"]

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Constant:
    name: str
    symbol: str
    value: float
    unit: str
    category: str


CONSTANTS_LIBRARY: list[Constant] = [
    # Mathematical
    Constant("Pi", "\u03c0", 3.141592653589793, "", "Mathematical"),
    Constant("Euler's Number", "e", 2.718281828459045, "", "Mathematical"),
    Constant("Golden Ratio", "\u03c6", 1.618033988749895, "", "Mathematical"),
    Constant("Euler-Mascheroni Constant", "\u03b3", 0.5772156649015329, "", "Mathematical"),
    Constant("Tau", "\u03c4", 6.283185307179586, "", "Mathematical"),
    Constant("Square Root of 2", "\u221a2", 1.4142135623730951, "", "Mathematical"),
    Constant("Square Root of 3", "\u221a3", 1.7320508075688772, "", "Mathematical"),
    Constant("Natural Log of 2", "ln 2", 0.6931471805599453, "", "Mathematical"),
    Constant("Natural Log of 10", "ln 10", 2.302585092994046, "", "Mathematical"),
    # Physical
    Constant("Speed of Light", "c", 299792458, "m/s", "Physical"),
    Constant("Planck's Constant", "h", 6.62607015e-34, "J\u00b7s", "Physical"),
    Constant("Reduced Planck Constant", "\u0127", 1.054571817e-34, "J\u00b7s", "Physical"),
    Constant("Boltzmann Constant", "k_B", 1.380649e-23, "J/K", "Physical"),
    Constant("Avogadro's Number", "N_A", 6.02214076e23, "mol\u207b\u00b9", "Physical"),
    Constant("Gravitational Constant", "G", 6.6743e-11, "m\u00b3/(kg\u00b7s\u00b2)", "Physical"),
    Constant("Elementary Charge", "e", 1.602176634e-19, "C", "Physical"),
    Constant("Permittivity of Free Space", "\u03b5\u2080", 8.854187817e-12, "F/m", "Physical"),
    Constant("Permeability of Free Space", "\u03bc\u2080", 1.25663706212e-6, "N/A\u00b2", "Physical"),
    Constant("Fine-Structure Constant", "\u03b1", 7.2973525693e-3, "", "Physical"),
    Constant("Rydberg Constant", "R_\u221e", 10973731.568157, "m\u207b\u00b9", "Physical"),
    # Chemical
    Constant("Universal Gas Constant", "R", 8.314462618, "J/(mol\u00b7K)", "Chemical"),
    Constant("Faraday Constant", "F", 96485.33212, "C/mol", "Chemical"),
    Constant("Standard Atmospheric Pressure", "atm", 101325, "Pa", "Chemical"),
    Constant("Molar Volume (STP)", "V_m", 0.02241396954, "m\u00b3/mol", "Chemical"),
    Constant("Stefan-Boltzmann Constant", "\u03c3", 5.670374419e-8, "W/(m\u00b2\u00b7K\u2074)", "Chemical"),
    # Astronomical
    Constant("Astronomical Unit", "AU", 1.495978707e11, "m", "Astronomical"),
    Constant("Light-Year", "ly", 9.4607304725808e15, "m", "Astronomical"),
    Constant("Parsec", "pc", 3.08567758149e16, "m", "Astronomical"),
    Constant("Solar Mass", "M_\u2609", 1.98847e30, "kg", "Astronomical"),
    Constant("Solar Radius", "R_\u2609", 6.957e8, "m", "Astronomical"),
    Constant("Earth Mass", "M_\u2295", 5.9722e24, "kg", "Astronomical"),
    Constant("Earth Radius", "R_\u2295", 6.371e6, "m", "Astronomical"),
    # Engineering
    Constant("Standard Gravity", "g\u2080", 9.80665, "m/s\u00b2", "Engineering"),
    Constant("Atmospheric Pressure (atm)", "atm", 101325, "Pa", "Engineering"),
    Constant("Speed of Sound (STP)", "v_sound", 343, "m/s", "Engineering"),
    Constant("Vacuum Permittivity", "\u03b5\u2080", 8.854187817e-12, "F/m", "Engineering"),
    Constant("Vacuum Permeability", "\u03bc\u2080", 1.25663706212e-6, "H/m", "Engineering"),
    Constant("Characteristic Impedance", "Z\u2080", 376.730313668, "\u03a9", "Engineering"),
]


class ConstantsLibrary:
    def __init__(self) -> None:
        self._constants: dict[str, Constant] = {c.symbol: c for c in CONSTANTS_LIBRARY}

    def get_by_symbol(self, symbol: str) -> Constant:
        if symbol not in self._constants:
            raise KeyError(f"Constant with symbol '{symbol}' not found")
        return self._constants[symbol]

    def get_by_name(self, name: str) -> Constant:
        for c in CONSTANTS_LIBRARY:
            if c.name.lower() == name.lower():
                return c
        raise KeyError(f"Constant with name '{name}' not found")

    def get_by_category(self, category: str) -> list[Constant]:
        result = [c for c in CONSTANTS_LIBRARY if c.category.lower() == category.lower()]
        if not result:
            raise KeyError(f"No constants found in category '{category}'")
        return result

    def search(self, query: str) -> list[Constant]:
        q = query.lower()
        return [
            c for c in CONSTANTS_LIBRARY
            if q in c.name.lower() or q in c.symbol.lower() or q in c.category.lower()
        ]

    def get_categories(self) -> list[str]:
        seen: set[str] = set()
        cats: list[str] = []
        for c in CONSTANTS_LIBRARY:
            if c.category not in seen:
                seen.add(c.category)
                cats.append(c.category)
        return cats

    def get_all(self) -> list[Constant]:
        return list(CONSTANTS_LIBRARY)
