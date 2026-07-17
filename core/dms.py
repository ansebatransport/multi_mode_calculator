"""Degrees/minutes/seconds (DMS) conversion."""
import math
import re


class DMSConverter:
    @staticmethod
    def decimal_to_dms(decimal_degrees: float) -> tuple[int, int, float]:
        sign = -1 if decimal_degrees < 0 else 1
        decimal_degrees = abs(decimal_degrees)
        d = int(decimal_degrees)
        m_full = (decimal_degrees - d) * 60
        m = int(m_full)
        s = (m_full - m) * 60
        return (sign * d, m, round(s, 4))

    @staticmethod
    def dms_to_decimal(degrees: int, minutes: int, seconds: float) -> float:
        if minutes < 0 or minutes >= 60:
            raise ValueError("Minutes must be between 0 and 59")
        if seconds < 0 or seconds >= 60:
            raise ValueError("Seconds must be between 0 and 60")
        sign = -1 if degrees < 0 else 1
        return sign * (abs(degrees) + minutes / 60 + seconds / 3600)

    @staticmethod
    def format_dms(degrees: int, minutes: int, seconds: float) -> str:
        if minutes < 0 or minutes >= 60:
            raise ValueError("Minutes must be between 0 and 59")
        if seconds < 0 or seconds >= 60:
            raise ValueError("Seconds must be between 0 and 60")
        return f"{degrees}\u00b0 {minutes}' {seconds}\""

    @staticmethod
    def parse_dms(dms_string: str) -> tuple[int, int, float]:
        pattern = r"(-?\d+)\s*[°d]\s*(\d+)\s*['m]\s*(\d+(?:\.\d+)?)\s*(?:\"|s)?"
        match = re.match(pattern, dms_string.strip())
        if not match:
            raise ValueError(f"Invalid DMS format: {dms_string}")
        degrees, minutes, seconds = int(match.group(1)), int(match.group(2)), float(match.group(3))
        if minutes < 0 or minutes >= 60:
            raise ValueError("Minutes must be between 0 and 59")
        if seconds < 0 or seconds >= 60:
            raise ValueError("Seconds must be between 0 and 60")
        return (degrees, minutes, seconds)
