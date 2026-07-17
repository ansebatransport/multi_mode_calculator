"""Input validation for calculator modes."""
import re
from typing import Optional

VALID_DECIMAL_DIGITS = set("0123456789.")
VALID_HEX_DIGITS = set("0123456789ABCDEFabcdef")
VALID_OCT_DIGITS = set("01234567")
VALID_BIN_DIGITS = set("01")
VALID_OPERATORS = set("+-×÷*/%")
VALID_FUNCTIONS = {
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
    "ln", "log", "log2", "sqrt", "cbrt", "abs",
    "factorial", "exp", "ceil", "floor",
}

class InputValidator:
    @staticmethod
    def validate_number_input(value: str, allow_negative: bool = True) -> bool:
        if not value: return True
        pattern = r'^-?\d*\.?\d*$' if allow_negative else r'^\d*\.?\d*$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def validate_expression(expr: str) -> tuple[bool, str]:
        if not expr: return True, ""
        depth = 0
        for ch in expr:
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
            if depth < 0:
                return False, "Unmatched closing parenthesis"
        if depth > 0:
            return False, "Unmatched opening parenthesis"
        if re.search(r'[+\-×÷*/%]{2,}(?!-)', expr):
            return False, "Consecutive operators"
        return True, ""
    
    @staticmethod
    def validate_hex_input(value: str) -> bool:
        return all(c in VALID_HEX_DIGITS or c in '+-' for c in value)
    
    @staticmethod
    def validate_oct_input(value: str) -> bool:
        return all(c in VALID_OCT_DIGITS or c in '+-' for c in value)
    
    @staticmethod
    def validate_bin_input(value: str) -> bool:
        return all(c in VALID_BIN_DIGITS or c in '><&|^~+-' for c in value)
    
    @staticmethod
    def validate_base_input(value: str, base: int) -> bool:
        valid = {c for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]}
        return all(c in valid or c in '+-' for c in value.upper())
    
    @staticmethod
    def validate_graph_expression(expr: str) -> tuple[bool, str]:
        if not expr:
            return False, "Expression cannot be empty"
        if 'x' not in expr.lower():
            return False, "Expression must contain 'x' as variable"
        valid = InputValidator.validate_expression(expr)
        if not valid[0]:
            return valid
        if '**' in expr and expr.count('**') > 5:
            return False, "Expression too complex"
        return True, ""
    
    @staticmethod
    def validate_range(value: float, min_val: float = -1e18, max_val: float = 1e18) -> bool:
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_angle(value: float, mode: str) -> bool:
        if mode == "degrees":
            return True
        elif mode == "radians":
            return True
        elif mode == "gradians":
            return True
        return False
    
    @staticmethod
    def sanitize_expression(expr: str) -> str:
        result = expr.replace('×', '*').replace('÷', '/')
        result = result.replace('−', '-')
        return result
    
    @staticmethod
    def validate_variable_name(name: str) -> tuple[bool, str]:
        if not name:
            return False, "Variable name cannot be empty"
        if not name[0].isalpha() and name[0] != '_':
            return False, "Variable name must start with a letter or underscore"
        if not re.match(r'^[a-zA-Z_]\w*$', name):
            return False, "Variable name can only contain letters, digits, and underscores"
        reserved = {'sin', 'cos', 'tan', 'log', 'ln', 'pi', 'e', 'i', 'inf', 'nan'}
        if name.lower() in reserved:
            return False, f"'{name}' is a reserved name"
        return True, ""
    
    @staticmethod
    def validate_financial_input(value: Optional[float], name: str) -> tuple[bool, str]:
        if value is None:
            return False, f"{name} is required"
        return True, ""
