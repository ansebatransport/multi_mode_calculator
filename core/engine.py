"""Expression evaluator - evaluates RPN token lists. The mathematical core of the calculator."""
import math
import cmath
from typing import Any, Callable, Optional

class ExpressionEvaluator:
    """Evaluates postfix (RPN) expressions produced by ShuntingYardParser."""
    
    CONSTANTS = {
        'π': math.pi,
        'pi': math.pi,
        'e': math.e,
        'phi': (1 + math.sqrt(5)) / 2,
        'c': 299792458,
        'g': 9.80665,
        'h_planck': 6.62607015e-34,
        'k_b': 1.380649e-23,
        'N_A': 6.02214076e23,
    }
    
    UNARY_FUNCTIONS = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'asinh': math.asinh, 'acosh': math.acosh, 'atanh': math.atanh,
        'ln': math.log, 'log': math.log10, 'log2': math.log2, 'log10': math.log10,
        'sqrt': math.sqrt, 'cbrt': lambda x: math.copysign(abs(x) ** (1/3), x),
        'abs': abs, 'exp': math.exp,
        'ceil': math.ceil, 'floor': math.floor, 'round': round,
        'factorial': math.factorial,
        'sec': lambda x: 1/math.cos(x), 'csc': lambda x: 1/math.sin(x),
        'cot': lambda x: 1/math.tan(x),
        'asec': lambda x: math.acos(1/x), 'acsc': lambda x: math.asin(1/x),
        'acot': lambda x: math.atan(1/x),
    }
    
    BINARY_OPERATORS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else (_ for _ in ()).throw(ZeroDivisionError("Division by zero")),
        '%': lambda a, b: a % b if b != 0 else (_ for _ in ()).throw(ZeroDivisionError("Modulo by zero")),
    }
    
    def __init__(self, angle_mode: str = "degrees"):
        self._angle_mode = angle_mode
        self._variables: dict[str, float] = {}
        self._user_functions: dict[str, tuple[list[str], str]] = {}
    
    @property
    def angle_mode(self) -> str:
        return self._angle_mode
    
    @angle_mode.setter
    def angle_mode(self, mode: str):
        if mode not in ("degrees", "radians", "gradians"):
            raise ValueError(f"Invalid angle mode: {mode}")
        self._angle_mode = mode
    
    def set_variable(self, name: str, value: float) -> None:
        self._variables[name] = value
    
    def set_user_function(self, name: str, params: list[str], expression: str) -> None:
        self._user_functions[name] = (params, expression)
    
    def _to_radians(self, angle: float) -> float:
        if self._angle_mode == "degrees":
            return math.radians(angle)
        elif self._angle_mode == "gradians":
            return angle * math.pi / 200
        return angle
    
    def _from_radians(self, angle: float) -> float:
        if self._angle_mode == "degrees":
            return math.degrees(angle)
        elif self._angle_mode == "gradians":
            return angle * 200 / math.pi
        return angle
    
    def _apply_unary_function(self, func_name: str, arg: float) -> float:
        """Apply a unary function, handling angle conversions for trig functions."""
        trig_funcs = {'sin', 'cos', 'tan', 'sec', 'csc', 'cot'}
        inverse_trig = {'asin', 'acos', 'atan', 'asec', 'acsc', 'acot'}
        
        if func_name in trig_funcs:
            converted = self._to_radians(arg)
            result = self.UNARY_FUNCTIONS[func_name](converted)
            if abs(result) < 1e-15:
                result = 0.0
            return result
        elif func_name in inverse_trig:
            raw = self.UNARY_FUNCTIONS[func_name](arg)
            return self._from_radians(raw)
        elif func_name in self.UNARY_FUNCTIONS:
            return self.UNARY_FUNCTIONS[func_name](arg)
        else:
            raise ValueError(f"Unknown function: {func_name}")
    
    def evaluate(self, tokens: list) -> float:
        """Evaluate a postfix (RPN) token list."""
        stack: list[float] = []
        
        for token in tokens:
            token_type = token.type if hasattr(token, 'type') else None
            token_value = token.value if hasattr(token, 'value') else str(token)
            
            if isinstance(token, tuple):
                token_type, token_value = token[0], token[1]
            
            if token_type and str(token_type).endswith('NUMBER'):
                stack.append(float(token_value))
            elif token_type and str(token_type).endswith('CONSTANT'):
                if token_value in self.CONSTANTS:
                    stack.append(self.CONSTANTS[token_value])
                else:
                    raise ValueError(f"Unknown constant: {token_value}")
            elif token_type and str(token_type).endswith('VARIABLE'):
                if token_value in self._variables:
                    stack.append(self._variables[token_value])
                else:
                    raise ValueError(f"Undefined variable: {token_value}")
            elif token_value == 'u-':
                if not stack: raise ValueError("Missing operand for unary minus")
                stack.append(-stack.pop())
            elif token_value == 'u+':
                if not stack: raise ValueError("Missing operand for unary plus")
            elif token_value == '!':
                if not stack: raise ValueError("Missing operand for factorial")
                val = stack.pop()
                if val < 0 or val != int(val):
                    raise ValueError(f"Factorial requires non-negative integer, got {val}")
                stack.append(float(math.factorial(int(val))))
            elif token_value == '~':
                if not stack: raise ValueError("Missing operand for bitwise NOT")
                stack.append(float(~int(stack.pop())))
            elif token_value in self.BINARY_OPERATORS:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for '{token_value}'")
                b = stack.pop()
                a = stack.pop()
                stack.append(self.BINARY_OPERATORS[token_value](a, b))
            elif token_value == '**':
                if len(stack) < 2:
                    raise ValueError("Insufficient operands for power")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = a ** b
                    if isinstance(result, complex):
                        result = result.real if result.imag == 0 else result
                    stack.append(result)
                except (OverflowError, ValueError):
                    stack.append(float('inf'))
            elif token_value in self.UNARY_FUNCTIONS:
                if not stack: raise ValueError(f"Missing operand for {token_value}")
                arg = stack.pop()
                stack.append(self._apply_unary_function(token_value, arg))
            else:
                try:
                    stack.append(float(token_value))
                except (ValueError, TypeError):
                    raise ValueError(f"Unknown token: {token_value}")
        
        if not stack:
            raise ValueError("Empty expression")
        if len(stack) > 1:
            raise ValueError("Malformed expression (too many operands)")
        
        return stack[0]
    
    def quick_evaluate(self, expression: str) -> float:
        """Tokenize, parse, and evaluate in one step (for simple expressions)."""
        from core.expression_parser import ShuntingYardParser
        parser = ShuntingYardParser()
        tokens = parser.parse(expression)
        return self.evaluate(tokens)
