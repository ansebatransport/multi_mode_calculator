"""Named variable storage for scientific calculations."""

__all__ = ["VariableManager"]

import re


class VariableManager:
    def __init__(self) -> None:
        self._variables: dict[str, float] = {}

    def set(self, name: str, value: float) -> None:
        if not self.validate_name(name):
            raise ValueError(
                f"Invalid variable name '{name}': must start with a letter and "
                "contain only alphanumeric characters and underscores"
            )
        self._variables[name] = float(value)

    def get(self, name: str) -> float:
        if name not in self._variables:
            raise KeyError(f"Variable '{name}' is not defined")
        return self._variables[name]

    def delete(self, name: str) -> None:
        if name not in self._variables:
            raise KeyError(f"Variable '{name}' is not defined")
        del self._variables[name]

    def list_all(self) -> dict[str, float]:
        return dict(self._variables)

    def clear(self) -> None:
        self._variables.clear()

    def to_dict(self) -> dict:
        return {"variables": dict(self._variables)}

    def from_dict(self, data: dict) -> None:
        vars_dict = data.get("variables", {})
        for name, value in vars_dict.items():
            if not self.validate_name(name):
                raise ValueError(f"Invalid variable name in data: '{name}'")
            vars_dict[name] = float(value)
        self._variables = vars_dict

    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z]\w*", name))
