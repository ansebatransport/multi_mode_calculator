"""Detect and format repeating decimal patterns."""
import re
from decimal import Decimal


class RecurringDecimal:
    @staticmethod
    def detect(value: float, precision: int = 15) -> dict:
        d = Decimal(str(value))
        sign, digits, exponent = d.as_tuple()
        digit_str = "".join(str(digit) for digit in digits)
        if exponent >= 0:
            return {"is_recurring": False, "non_repeating": str(d), "repeating": "", "notation": str(d)}
        int_part = digit_str[:len(digit_str) + exponent] if len(digit_str) + exponent > 0 else "0"
        frac_part = digit_str[len(digit_str) + exponent:] if len(digit_str) + exponent >= 0 else "0" * (-(len(digit_str) + exponent)) + digit_str
        frac_part = frac_part.ljust(-exponent, "0")
        if len(frac_part) < 4:
            return {"is_recurring": False, "non_repeating": str(d), "repeating": "", "notation": str(d)}
        for cycle_len in range(1, len(frac_part) // 2 + 1):
            if len(frac_part) % cycle_len == 0:
                pattern = frac_part[:cycle_len]
                if pattern * (len(frac_part) // cycle_len) == frac_part:
                    notation = RecurringDecimal.format_recurring(f"{int_part}.", pattern)
                    return {"is_recurring": True, "non_repeating": f"{int_part}.", "repeating": pattern, "notation": notation}
        for cycle_len in range(1, len(frac_part) // 3 + 1):
            for start in range(0, len(frac_part) - cycle_len * 2 + 1):
                pattern = frac_part[start:start + cycle_len]
                remaining = frac_part[start + cycle_len:]
                if remaining.startswith(pattern) and len(remaining) >= cycle_len * 2:
                    match_len = 0
                    temp = remaining
                    while temp.startswith(pattern):
                        temp = temp[cycle_len:]
                        match_len += cycle_len
                    if match_len >= cycle_len * 2:
                        non_rep_part = frac_part[:start]
                        non_rep = f"{int_part}.{non_rep_part}" if non_rep_part else f"{int_part}."
                        notation = RecurringDecimal.format_recurring(non_rep, pattern)
                        return {"is_recurring": True, "non_repeating": non_rep, "repeating": pattern, "notation": notation}
        return {"is_recurring": False, "non_repeating": str(d), "repeating": "", "notation": str(d)}

    @staticmethod
    def fraction_to_recurring(numerator: int, denominator: int) -> str:
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        if numerator == 0:
            return "0"
        neg = "-" if (numerator < 0) != (denominator < 0) else ""
        num, den = abs(numerator), abs(denominator)
        int_part = num // den
        remainder = num % den
        if remainder == 0:
            return f"{neg}{int_part}"
        result = f"{neg}{int_part}."
        rems = {}
        frac = ""
        while remainder != 0 and remainder not in rems:
            rems[remainder] = len(frac)
            remainder *= 10
            frac += str(remainder // den)
            remainder %= den
        if remainder == 0:
            return result + frac
        idx = rems[remainder]
        non_rep = frac[:idx]
        rep = frac[idx:]
        if non_rep:
            return result + non_rep + f"({rep})"
        else:
            return result + f"({rep})"

    @staticmethod
    def format_recurring(non_rep: str, rep: str) -> str:
        return f"{non_rep}({rep})"
