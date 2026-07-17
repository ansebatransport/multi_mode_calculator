"""Reverse Polish Notation (RPN) calculator engine."""
import math
from typing import Union


class RPNEngine:
    def __init__(self):
        self._stack: list[float] = []
        self._ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else (_ for _ in ()).throw(ZeroDivisionError),
            '**': lambda a, b: a ** b,
            '%': lambda a, b: a % b,
            '&': lambda a, b: int(a) & int(b),
            '|': lambda a, b: int(a) | int(b),
            '^': lambda a, b: int(a) ^ int(b),
            '~': lambda a: ~int(a),
            '<<': lambda a, b: int(a) << int(b),
            '>>': lambda a, b: int(a) >> int(b),
            'sin': lambda a: math.sin(a),
            'cos': lambda a: math.cos(a),
            'tan': lambda a: math.tan(a),
            'ln': lambda a: math.log(a),
            'log': lambda a: math.log10(a),
            'sqrt': lambda a: math.sqrt(a),
            'abs': lambda a: abs(a),
            '!': lambda a: math.factorial(int(a)),
        }

    def push(self, value: float) -> None:
        self._stack.append(value)

    def execute(self, token: str) -> None:
        parsed = self._parse_token(token)
        if isinstance(parsed, float):
            self._stack.append(parsed)
            return
        op = str(parsed)
        if op not in self._ops:
            raise ValueError(f"Unknown operator: {op}")
        op_func = self._ops[op]
        import inspect
        sig = inspect.signature(op_func)
        n_args = len(sig.parameters)
        if len(self._stack) < n_args:
            raise ValueError(f"Not enough stack values for {op} (need {n_args})")
        if n_args == 2:
            b = self._stack.pop()
            a = self._stack.pop()
            self._stack.append(op_func(a, b))
        elif n_args == 1:
            a = self._stack.pop()
            self._stack.append(op_func(a))

    def dup(self) -> None:
        if not self._stack:
            raise ValueError("Stack is empty")
        self._stack.append(self._stack[-1])

    def swap(self) -> None:
        if len(self._stack) < 2:
            raise ValueError("Need at least 2 values to swap")
        self._stack[-1], self._stack[-2] = self._stack[-2], self._stack[-1]

    def drop(self) -> None:
        if not self._stack:
            raise ValueError("Stack is empty")
        self._stack.pop()

    def rot(self) -> None:
        if len(self._stack) < 3:
            raise ValueError("Need at least 3 values to rotate")
        self._stack[-3], self._stack[-2], self._stack[-1] = self._stack[-2], self._stack[-1], self._stack[-3]

    def clear(self) -> None:
        self._stack.clear()

    def get_stack(self) -> list[float]:
        return list(self._stack)

    def peek(self) -> float:
        if not self._stack:
            raise ValueError("Stack is empty")
        return self._stack[-1]

    def evaluate_rpn(self, expression: str) -> float:
        self._stack.clear()
        tokens = expression.strip().split()
        for token in tokens:
            if token.lower() in ("dup", "swap", "drop", "rot", "clear"):
                getattr(self, token.lower())()
            else:
                self.execute(token)
        if not self._stack:
            raise ValueError("No result on stack")
        return self._stack[-1]

    def _parse_token(self, token: str) -> Union[float, str]:
        token = token.strip().lower()
        try:
            return float(token)
        except ValueError:
            return token
