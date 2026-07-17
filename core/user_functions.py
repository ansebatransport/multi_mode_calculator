"""User-defined function storage and evaluation."""
import re
import math
from typing import Callable


class UserFunctionManager:
    def __init__(self):
        self._functions: dict[str, dict] = {}

    def define(self, name: str, params: list[str], expression: str) -> None:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            raise ValueError(f"Invalid function name: {name}")
        if not params:
            raise ValueError("Function must have at least one parameter")
        for p in params:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', p):
                raise ValueError(f"Invalid parameter name: {p}")
        if not self._validate_expression(expression):
            raise ValueError(f"Invalid expression: {expression}")
        func = self._compile(expression, params)
        self._functions[name] = {
            "params": list(params),
            "expression": expression,
            "func": func,
        }

    def evaluate(self, name: str, args: list[float]) -> float:
        if name not in self._functions:
            raise ValueError(f"Function '{name}' not defined")
        func_info = self._functions[name]
        if len(args) != len(func_info["params"]):
            raise ValueError(f"Expected {len(func_info['params'])} arguments, got {len(args)}")
        return func_info["func"](*args)

    def delete(self, name: str) -> None:
        if name not in self._functions:
            raise ValueError(f"Function '{name}' not defined")
        del self._functions[name]

    def list_all(self) -> dict[str, dict]:
        result = {}
        for name, info in self._functions.items():
            result[name] = {"params": list(info["params"]), "expression": info["expression"]}
        return result

    def get_params(self, name: str) -> list[str]:
        if name not in self._functions:
            raise ValueError(f"Function '{name}' not defined")
        return list(self._functions[name]["params"])

    def get_expression(self, name: str) -> str:
        if name not in self._functions:
            raise ValueError(f"Function '{name}' not defined")
        return self._functions[name]["expression"]

    def _compile(self, expression: str, params: list[str]) -> Callable:
        safe_globals = {
            "math": math,
            "abs": abs,
            "max": max,
            "min": min,
            "pow": pow,
            "round": round,
            "sum": sum,
        }
        safe_globals.update({
            k: getattr(math, k) for k in dir(math) if not k.startswith("_")
        })
        local_vars = {p: 0.0 for p in params}
        try:
            code = compile(expression, "<user_function>", "eval")
            for name in code.co_names:
                if name not in safe_globals and name not in params:
                    raise ValueError(f"Unsafe or unknown name in expression: {name}")
            def user_func(*args):
                env = {p: a for p, a in zip(params, args)}
                env.update(safe_globals)
                return eval(code, {"__builtins__": {}}, env)
            return user_func
        except SyntaxError as e:
            raise ValueError(f"Syntax error in expression: {e}") from e

    def _validate_expression(self, expression: str) -> bool:
        if not expression or not expression.strip():
            return False
        allowed = re.compile(r'^[a-zA-Z0-9_\s+\-*/().,%^e**]+$')
        return bool(allowed.match(expression))
