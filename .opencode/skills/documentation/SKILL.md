---
name: documentation
description: Use when updating README, ARCHITECTURE.md, TEST_GUIDE.md, API docs, inline docstrings, or when code changes affect documentation. Trigger on phrases like "update docs", "document this", "add docstring", "update README", "API documentation", "changelog", or after significant code changes.
---

# Documentation Skill

Keep documentation accurate and in sync with code changes.

## Documentation Files

| File | Purpose | When to update |
|------|---------|---------------|
| `README.md` | Project overview, setup, usage | New features, setup changes |
| `ARCHITECTURE.md` | Design, modules, data flow | New modules, API changes |
| `TEST_GUIDE.md` | Test values, user guide | New modes, changed calculations |
| `AGENTS.md` | Dev workflow for opencode | Workflow changes |
| `CHANGELOG.md` | Release history | Each release |

## Docstring Standard

Use Google-style docstrings for all public functions:

```python
def mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly mortgage payment.

    Uses the standard amortization formula:
    M = P * [r(1+r)^n] / [(1+r)^n - 1]

    Args:
        principal: Loan amount in dollars.
        annual_rate: Annual interest rate as decimal (e.g., 0.05 for 5%).
        years: Loan term in years.

    Returns:
        Monthly payment amount in dollars.

    Raises:
        ValueError: If principal is negative or rate is negative.

    Examples:
        >>> mortgage_payment(100000, 0.05, 30)
        536.82
    """
```

## API Documentation

For each Flask endpoint in `apps/web/app.py`, document:

```python
@app.route('/api/financial/mortgage', methods=['POST'])
def calculate_mortgage():
    """Calculate mortgage details.

    Request body:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (decimal)
        years (int): Loan term in years

    Response:
        {
            "monthly_payment": float,
            "total_payment": float,
            "total_interest": float
        }

    Error responses:
        400: Missing required fields
        500: Calculation error
    """
```

## README Updates

Keep README current with:
- Project description and features
- Setup instructions (install deps, run server)
- API endpoint list with examples
- Screenshot or GIF of the UI
- Contributing guidelines

## Rules

- NEVER let documentation lag behind code — update docs in the same PR
- Use concrete examples, not abstract descriptions
- Keep ARCHITECTURE.md high-level (no code snippets longer than 5 lines)
- TEST_GUIDE.md must have verifiable expected values for each test case
- When adding a new module, add its docstring AND update ARCHITECTURE.md
