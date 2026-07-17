"""Base/radix conversion utilities."""


class BaseConverter:
    DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def to_decimal(value: str, base: int) -> int:
        if base < 2 or base > 36:
            raise ValueError("Base must be between 2 and 36")
        value = value.strip().upper()
        if not value:
            raise ValueError("Empty value")
        neg = False
        if value[0] == "-":
            neg = True
            value = value[1:]
        try:
            result = int(value, base)
        except ValueError as e:
            raise ValueError(f"Invalid value '{value}' for base {base}") from e
        return -result if neg else result

    @staticmethod
    def from_decimal(value: int, base: int) -> str:
        if base < 2 or base > 36:
            raise ValueError("Base must be between 2 and 36")
        if value == 0:
            return "0"
        neg = "-" if value < 0 else ""
        value = abs(value)
        digits = []
        while value > 0:
            digits.append(BaseConverter.DIGITS[value % base])
            value //= base
        return neg + "".join(reversed(digits))

    @staticmethod
    def hex_to_bin(hex_str: str) -> str:
        dec = BaseConverter.to_decimal(hex_str, 16)
        return BaseConverter.from_decimal(dec, 2)

    @staticmethod
    def bin_to_hex(bin_str: str) -> str:
        dec = BaseConverter.to_decimal(bin_str, 2)
        return BaseConverter.from_decimal(dec, 16)

    @staticmethod
    def oct_to_bin(oct_str: str) -> str:
        dec = BaseConverter.to_decimal(oct_str, 8)
        return BaseConverter.from_decimal(dec, 2)

    @staticmethod
    def bin_to_oct(bin_str: str) -> str:
        dec = BaseConverter.to_decimal(bin_str, 2)
        return BaseConverter.from_decimal(dec, 8)

    @staticmethod
    def hex_to_oct(hex_str: str) -> str:
        dec = BaseConverter.to_decimal(hex_str, 16)
        return BaseConverter.from_decimal(dec, 8)

    @staticmethod
    def oct_to_hex(oct_str: str) -> str:
        dec = BaseConverter.to_decimal(oct_str, 8)
        return BaseConverter.from_decimal(dec, 16)

    @staticmethod
    def twos_complement(value: int, bits: int) -> str:
        if bits < 1:
            raise ValueError("Bits must be positive")
        if value < -(2 ** (bits - 1)) or value >= 2 ** (bits - 1):
            raise ValueError(f"Value {value} out of range for {bits}-bit two's complement")
        if value >= 0:
            return BaseConverter.from_decimal(value, 2).zfill(bits)
        return BaseConverter.from_decimal(2 ** bits + value, 2).zfill(bits)

    @staticmethod
    def sign_extend(value: int, bits: int) -> int:
        if bits < 1:
            raise ValueError("Bits must be positive")
        if value >> (bits - 1) & 1:
            mask = (1 << bits) - 1
            return -((~value & mask) + 1)
        return value

    @staticmethod
    def to_all_bases(decimal_value: int) -> dict[str, str]:
        return {
            "hex": BaseConverter.from_decimal(decimal_value, 16),
            "dec": str(decimal_value),
            "oct": BaseConverter.from_decimal(decimal_value, 8),
            "bin": BaseConverter.from_decimal(decimal_value, 2),
        }

    @staticmethod
    def get_bit_length(value: int) -> int:
        if value == 0:
            return 1
        return value.bit_length()
