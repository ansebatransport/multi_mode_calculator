---
name: debugging
description: Use when investigating bugs, analyzing errors, tracing execution, or diagnosing issues. Trigger on phrases like "debug", "bug", "why isn't this working", "trace", "breakpoint", "investigate", "not working", "wrong output", "unexpected behavior", or when something produces incorrect results.
---

# Debugging Skill

Systematic approach to finding and fixing bugs.

## Debug Workflow

```
1. Reproduce     → Make the bug happen consistently
2. Isolate       → Narrow down where it happens
3. Hypothesize   → Form a theory about why
4. Test          → Verify the theory
5. Fix           → Apply the minimal fix
6. Verify        → Confirm the fix works
7. Prevent       → Add test to prevent regression
```

## Reproduce First

```python
# Create a minimal reproduction script
# Save as debug_repro.py and run it

from core.engine import MathEngine

engine = MathEngine()

# Minimal reproduction
result = engine.calculate("sin(pi/2)")
print(f"Expected: 1.0, Got: {result}")

# With context
print(f"Angle mode: {engine.angle_mode}")
print(f"State: {engine.state}")
```

## Isolation Techniques

### Binary Search
```python
# Comment out half the code to narrow the problem
def problematic_function(data):
    # Step 1: Is it the input?
    print(f"Input: {data}")

    # Step 2: Is it step 1?
    result1 = step1(data)
    print(f"After step1: {result1}")

    # Step 3: Is it step 2?
    result2 = step2(result1)
    print(f"After step2: {result2}")

    # The bug is in whichever step produces wrong output
    return result2
```

### Print Debugging
```python
# Structured debug prints
def debug(var_name, value):
    print(f"[DEBUG] {var_name} = {value!r} (type: {type(value).__name__})")

# Usage
debug("expression", expression)
debug("result", result)
debug("angle_mode", engine.angle_mode)
```

### Logging Instead of Print
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Expression: {expression}")
logger.info(f"Angle mode: {engine.angle_mode}")
logger.warning(f"Precision loss detected: {diff}")
logger.error(f"Calculation failed: {e}", exc_info=True)
```

## Common Bug Patterns

### Floating Point
```python
# BUG: Direct equality comparison
assert result == 1.5707963267948966

# FIX: Use approximate comparison
assert result == pytest.approx(1.5707963267948966, rel=1e-9)
```

### Mutable Default
```python
# BUG: Shared mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# FIX: Use None sentinel
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Off-by-One
```python
# BUG: Wrong range
for i in range(1, len(data)):  # Skips first element
    process(data[i])

# FIX: Correct range
for i in range(len(data)):
    process(data[i])

# BETTER: Iterate directly
for item in data:
    process(item)
```

### Variable Scope
```python
# BUG: Loop variable leaks
for x in range(10):
    pass
print(x)  # 9, not an error

# FIX: Use function scope or explicit initial value
result = None
for x in range(10):
    result = x
print(result)
```

## Using Python Debugger

```python
# Add breakpoint anywhere
result = calculate(expression)
breakpoint()  # Drops into pdb here
print(result)

# In terminal:
# n = next line
# s = step into
# c = continue
# p <expr> = print expression
# l = list source
# q = quit
```

## Verification Checklist

After fixing a bug:
- [ ] Minimal fix — didn't change unrelated code
- [ ] Tests pass — `python -m pytest tests/ -x -q`
- [ ] Added regression test
- [ ] Checked similar code for same bug
- [ ] Updated documentation if behavior changed

## Rules

- ALWAYS reproduce before fixing
- NEVER fix without understanding the root cause
- MINIMAL changes — don't refactor while fixing
- ALWAYS add a regression test
- Check if the same bug exists elsewhere
