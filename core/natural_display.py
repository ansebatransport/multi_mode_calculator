"""Textbook notation rendering logic (fractions, roots, exponents)."""
from typing import Union

SUPERSCRIPT = str.maketrans("0123456789.", "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u2024")
SUBSCRIPT = str.maketrans("0123456789", "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089")


class NaturalDisplay:
    @staticmethod
    def format_fraction(num: int, den: int) -> dict:
        return {
            "type": "fraction",
            "numerator": str(num),
            "denominator": str(den),
            "display": f"{num}/{den}",
        }

    @staticmethod
    def format_root(radicand: str, index: int = 2) -> dict:
        prefix = "\u221b" if index == 3 else "\u221a"
        display = f"{prefix}({radicand})"
        if index != 2 and index != 3:
            display = f"{index}{prefix}({radicand})"
        return {
            "type": "root",
            "radicand": radicand,
            "index": index,
            "display": display,
        }

    @staticmethod
    def format_power(base: str, exponent: str) -> dict:
        return {
            "type": "power",
            "base": base,
            "exponent": exponent,
            "display": f"{base}^{exponent}",
        }

    @staticmethod
    def format_subscript(base: str, subscript: str) -> dict:
        return {
            "type": "subscript",
            "base": base,
            "subscript": subscript,
            "display": f"{base}_{subscript}",
        }

    @staticmethod
    def format_log(base: str, argument: str) -> dict:
        display = f"log\u2081\u2080({argument})" if base == "10" else f"ln({argument})" if base == "e" else f"log_{base}({argument})"
        return {
            "type": "log",
            "base": base,
            "argument": argument,
            "display": display,
        }

    @staticmethod
    def to_unicode(expr: str) -> str:
        result = []
        i = 0
        while i < len(expr):
            if expr[i] == "^" and i + 1 < len(expr):
                i += 1
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == "." or expr[i] == "-"):
                    num += expr[i]
                    i += 1
                result.append(num.translate(SUPERSCRIPT))
                continue
            elif expr[i] == "_" and i + 1 < len(expr):
                i += 1
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                    num += expr[i]
                    i += 1
                result.append(num.translate(SUBSCRIPT))
                continue
            result.append(expr[i])
            i += 1
        return "".join(result)
