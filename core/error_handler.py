"""Centralized error handling and user-friendly messages."""
from enum import Enum
from typing import Optional

class ErrorType(Enum):
    DIVISION_BY_ZERO = "division_by_zero"
    INVALID_EXPRESSION = "invalid_expression"
    DOMAIN_ERROR = "domain_error"
    OVERFLOW = "overflow"
    UNDERFLOW = "underflow"
    MATRIX_DIMENSION = "matrix_dimension_mismatch"
    MATRIX_SINGULAR = "matrix_singular"
    INVALID_UNIT = "invalid_unit_conversion"
    INVALID_BASE = "invalid_base"
    INVALID_HEX_DIGIT = "invalid_hex_digit"
    OUT_OF_RANGE = "out_of_range"
    NO_SOLUTION = "no_solution"
    INVALID_INPUT = "invalid_input"
    NETWORK_ERROR = "network_error"
    FILE_ERROR = "file_error"
    UNKNOWN = "unknown"

ERROR_MESSAGES = {
    ErrorType.DIVISION_BY_ZERO: "Cannot divide by zero",
    ErrorType.INVALID_EXPRESSION: "Invalid expression",
    ErrorType.DOMAIN_ERROR: "Value out of domain",
    ErrorType.OVERFLOW: "Number too large to display",
    ErrorType.UNDERFLOW: "Number too small to display",
    ErrorType.MATRIX_DIMENSION: "Matrix dimensions mismatch",
    ErrorType.MATRIX_SINGULAR: "Matrix is singular (no inverse)",
    ErrorType.INVALID_UNIT: "Cannot convert between incompatible units",
    ErrorType.INVALID_BASE: "Invalid digit for selected base",
    ErrorType.INVALID_HEX_DIGIT: "Invalid hexadecimal digit",
    ErrorType.OUT_OF_RANGE: "Value out of allowed range",
    ErrorType.NO_SOLUTION: "No solution found",
    ErrorType.INVALID_INPUT: "Invalid input",
    ErrorType.NETWORK_ERROR: "Network unavailable (using cached rates)",
    ErrorType.FILE_ERROR: "Could not save/load file",
    ErrorType.UNKNOWN: "An unexpected error occurred",
}

class CalculatorError(Exception):
    def __init__(self, error_type: ErrorType, detail: Optional[str] = None):
        self.error_type = error_type
        self.detail = detail
        self.message = ERROR_MESSAGES.get(error_type, "Unknown error")
        if detail:
            self.message = f"{self.message}: {detail}"
        super().__init__(self.message)

class ErrorHandler:
    @staticmethod
    def handle_division_by_zero() -> CalculatorError:
        return CalculatorError(ErrorType.DIVISION_BY_ZERO)
    
    @staticmethod
    def handle_invalid_expression(expr: str = "") -> CalculatorError:
        return CalculatorError(ErrorType.INVALID_EXPRESSION, expr)
    
    @staticmethod
    def handle_domain_error(detail: str = "") -> CalculatorError:
        return CalculatorError(ErrorType.DOMAIN_ERROR, detail)
    
    @staticmethod
    def handle_overflow() -> CalculatorError:
        return CalculatorError(ErrorType.OVERFLOW)
    
    @staticmethod
    def handle_matrix_error(detail: str = "") -> CalculatorError:
        return CalculatorError(ErrorType.MATRIX_DIMENSION, detail)
    
    @staticmethod
    def handle_invalid_base(base: int) -> CalculatorError:
        return CalculatorError(ErrorType.INVALID_BASE, f"base {base}")
    
    @staticmethod
    def handle_out_of_range(detail: str = "") -> CalculatorError:
        return CalculatorError(ErrorType.OUT_OF_RANGE, detail)
    
    @staticmethod
    def handle_no_solution(detail: str = "") -> CalculatorError:
        return CalculatorError(ErrorType.NO_SOLUTION, detail)
    
    @staticmethod
    def format_error(error: CalculatorError) -> str:
        return f"⚠ {error.message}"
    
    @staticmethod
    def format_error_for_display(error: Exception) -> str:
        if isinstance(error, CalculatorError):
            return ErrorHandler.format_error(error)
        elif isinstance(error, ZeroDivisionError):
            return "⚠ Cannot divide by zero"
        elif isinstance(error, ValueError):
            return f"⚠ {str(error)}"
        elif isinstance(error, OverflowError):
            return "⚠ Number too large"
        elif isinstance(error, TypeError):
            return "⚠ Invalid operation"
        else:
            return f"⚠ Error: {str(error)[:50]}"
