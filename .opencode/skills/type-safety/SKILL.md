---
name: type-safety
description: Use when adding type hints, running mypy/pyright, fixing type errors, or improving static analysis coverage. Trigger on phrases like "add types", "type hints", "mypy", "pyright", "type error", "static analysis", "type checking", or when editing core/ modules.
---

# Type Safety Skill

Add and maintain type hints across the codebase for catching bugs at edit-time.

## Current State

- 40 core modules with minimal type hints
- LSP configured with pylsp in opencode.json
- No mypy config yet

## Setup

```bash
# Install mypy (if not present)
pip install mypy --break-system-packages

# Run mypy on the project
cd /home/mulugeta/projects/multi_mode_calculator
python -m mypy core/ --ignore-missing-imports

# Run on a single file
python -m mypy core/engine.py --ignore-missing-imports

# Strict mode (for new code)
python -m mypy core/ --strict --ignore-missing-imports
```

## Type Hint Patterns for This Project

### Function signatures
```python
from typing import Optional, Union

# Basic
def add(a: float, b: float) -> float:
    return a + b

# Optional parameters
def calculate(expression: str, angle_mode: str = "radians") -> float:
    ...

# Union types
def parse_value(val: Union[str, int, float]) -> float:
    ...

# Multiple return types
def safe_divide(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b
```

### Dictionary/config patterns
```python
from typing import Dict, List, Any

# Financial parameters
params: Dict[str, float] = {
    "principal": 100000,
    "rate": 0.05,
    "years": 30,
}

# API response
response: Dict[str, Any] = {
    "result": 1234.56,
    "success": True,
}
```

### Return type annotations
```python
# Always annotate return types — helps IDE and catches bugs
def mortgage_payment(principal: float, rate: float, months: int) -> float:
    ...

# Tuple returns
def min_max(values: List[float]) -> tuple[float, float]:
    return min(values), max(values)
```

## Adding Types to Existing Code

### Priority order:
1. `core/engine.py` — central module, most used
2. `core/expression_parser.py` — complex parsing logic
3. `core/financial.py` — financial calculations
4. `core/statistics.py` — statistical functions
5. All other `core/` modules
6. `apps/web/app.py` — Flask routes
7. `utils/` — utility modules

### Approach:
1. Add type hints to function signatures first
2. Run mypy to find inconsistencies
3. Fix type errors one file at a time
4. Add `# type: ignore` only as last resort with a comment explaining why

## Rules

- NEVER use `Any` unless absolutely necessary — prefer specific types
- ALWAYS annotate return types — even `-> None`
- Use `Optional[X]` for values that can be None, not `X | None` (Python 3.9 compat)
- Keep types readable — use aliases for complex types
- Don't over-type internal helpers — focus on public APIs
