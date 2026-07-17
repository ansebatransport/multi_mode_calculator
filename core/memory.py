"""Memory registers for calculator. Supports M0-M9."""

__all__ = ["MemoryManager"]

_REGISTER_COUNT = 10


class MemoryManager:
    def __init__(self) -> None:
        self._registers: list[float] = [0.0] * _REGISTER_COUNT

    def store(self, register: int, value: float) -> None:
        if not 0 <= register < _REGISTER_COUNT:
            raise IndexError(f"Register must be 0-{_REGISTER_COUNT - 1}, got {register}")
        self._registers[register] = value

    def recall(self, register: int) -> float:
        if not 0 <= register < _REGISTER_COUNT:
            raise IndexError(f"Register must be 0-{_REGISTER_COUNT - 1}, got {register}")
        return self._registers[register]

    def add(self, register: int, value: float) -> None:
        if not 0 <= register < _REGISTER_COUNT:
            raise IndexError(f"Register must be 0-{_REGISTER_COUNT - 1}, got {register}")
        self._registers[register] += value

    def subtract(self, register: int, value: float) -> None:
        if not 0 <= register < _REGISTER_COUNT:
            raise IndexError(f"Register must be 0-{_REGISTER_COUNT - 1}, got {register}")
        self._registers[register] -= value

    def clear(self, register: int) -> None:
        if not 0 <= register < _REGISTER_COUNT:
            raise IndexError(f"Register must be 0-{_REGISTER_COUNT - 1}, got {register}")
        self._registers[register] = 0.0

    def clear_all(self) -> None:
        self._registers = [0.0] * _REGISTER_COUNT

    def to_dict(self) -> dict:
        return {"registers": self._registers[:]}

    def from_dict(self, data: dict) -> None:
        regs = data.get("registers")
        if not isinstance(regs, list) or len(regs) != _REGISTER_COUNT:
            raise ValueError(f"Invalid memory data: expected list of length {_REGISTER_COUNT}")
        self._registers = [float(v) for v in regs]
