---
name: testing
description: Use when writing, running, debugging, or fixing tests. Trigger on phrases like "run tests", "fix failing tests", "write tests for", "add test coverage", "test failed", "pytest", or when modifying files in tests/. Covers unit tests, integration tests, test generation, and failure analysis.
---

# Testing Skill

Manage the project's 860+ test suite efficiently.

## Project Test Structure

```
tests/
  core/                    # 33 unit test files
    test_engine.py         # Calculator engine tests
    test_financial.py      # Financial module tests
    test_expression_parser.py
    ... (one per core module)
  integration/             # 4 integration test files
    test_calculation_pipeline.py
    test_export_import_integration.py
    test_history_clipboard_integration.py
    test_mode_switching.py
  ui/                      # Placeholder (currently empty)
```

## Commands

```bash
# Run all tests (fast, ~1s)
cd /home/mulugeta/projects/multi_mode_calculator && python -m pytest tests/ -x -q

# Run specific module tests
python -m pytest tests/core/test_financial.py -x -v

# Run with short traceback
python -m pytest tests/ --tb=short -q

# Run and stop on first failure
python -m pytest tests/ -x

# Verbose output for debugging
python -m pytest tests/core/test_engine.py -v

# Show last N failing tests
python -m pytest tests/ --lf

# Run tests matching a keyword
python -m pytest tests/ -k "financial" -v
```

## Workflow

### After code changes:
1. Run `python -m pytest tests/ -x -q` to verify no regressions
2. If a test fails, read the failure output carefully
3. Identify whether the bug is in the code or the test
4. Fix the root cause, not the test (unless the test expectation is wrong)

### Writing new tests:
1. Look at existing tests in the same module for patterns
2. Use `pytest.approx()` for floating-point comparisons: `assert result == pytest.approx(1.570799, rel=1e-5)`
3. Test both happy paths and edge cases (zero, negative, overflow, invalid input)
4. Name tests descriptively: `test_mortgage_monthly_payment_with_zero_interest`

### Debugging failures:
1. Run the specific failing test with `-v` for details
2. Add temporary `print()` statements or use `pytest.set_trace()` for breakpoints
3. Check if the failure is in core logic or an import/API issue
4. Compare expected vs actual values — small differences may be floating-point precision

## Test Patterns

```python
# Standard assertion
assert result == expected

# Float comparison
assert result == pytest.approx(expected, rel=1e-9)

# Exception testing
with pytest.raises(ValueError, match="Invalid"):
    dangerous_function()

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (-1, -1),
])
def test_abs(input, expected):
    assert abs(input) == expected
```

## Important Rules

- NEVER skip tests to make things pass — fix the root cause
- If a test is flaky (passes sometimes), investigate timing or randomness
- Keep tests independent — no test should depend on another test's state
- When adding a new core module, always add a corresponding test file
