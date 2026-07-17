---
name: sdks
description: Use when building SDK/client libraries, defining API contracts, creating language bindings, or packaging the calculator as a reusable library. Trigger on phrases like "SDK", "client library", "API wrapper", "package for", "npm package", "pip package", "export API", "language binding", or when creating new entry points for the core engine.
---

# SDK Skill

Package the calculator's core logic as reusable libraries for other platforms.

## Current Architecture Advantage

The `core/` directory is already UI-independent pure Python. This makes SDK creation straightforward — just add thin wrappers.

## SDK Targets

| Platform | Package Name | Entry Point | Priority |
|----------|-------------|-------------|----------|
| Python (pip) | `multi-calc` | `from multi_calc import Calculator` | High |
| JavaScript (npm) | `multi-calc` | `const calc = require('multi-calc')` | High |
| REST API | — | `https://api.example.com/v1/calculate` | Already exists |
| CLI | `multi-calc-cli` | `multi-calc "sin(pi/4)"` | Medium |

## Python SDK

### Structure
```
sdks/python/
  multi_calc/
    __init__.py
    calculator.py
    exceptions.py
  setup.py
  README.md
  tests/
```

### API Design
```python
from multi_calc import Calculator

calc = Calculator()
result = calc.evaluate("sin(pi/4) + cos(pi/4)")

# With options
result = calc.evaluate(
    "sqrt(x^2 + y^2)",
    angle_mode="degrees",
    precision=10
)

# Financial
mortgage = calc.mortgage(principal=100000, rate=0.05, years=30)

# Unit conversion
weight = calc.convert(1, "kg", "lb")
```

## JavaScript SDK

### Structure
```
sdks/javascript/
  src/
    index.js
    calculator.js
  package.json
  README.md
  tests/
```

### API Design
```javascript
const { Calculator } = require('multi-calc');

const calc = new Calculator();
const result = calc.evaluate('sin(pi/4) + cos(pi/4)');

// Financial
const mortgage = calc.mortgage({
  principal: 100000,
  rate: 0.05,
  years: 30
});
```

## CLI SDK

```bash
# Basic calculation
multi-calc "2 + 3 * 4"
# Output: 14

# With options
multi-calc "sin(45)" --angle degrees
# Output: 0.7071067811865475

# Financial mode
multi-calc --mortgage --principal 100000 --rate 0.05 --years 30
# Output: Monthly payment: $536.82

# Pipe support
echo "sqrt(144)" | multi-calc
# Output: 12.0
```

## Packaging

### Python (PyPI)
```bash
cd sdks/python
python -m build
twine upload dist/*
```

### JavaScript (npm)
```bash
cd sdks/javascript
npm publish
```

## API Contract (OpenAPI)

Define the REST API contract for external consumers:

```yaml
openapi: 3.0.0
paths:
  /api/calculate:
    post:
      summary: Evaluate a math expression
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                expression:
                  type: string
                angle_mode:
                  type: string
                  enum: [radians, degrees]
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: number
```

## Rules

- SDK must be a thin wrapper — all logic stays in `core/`
- Each SDK must have its own test suite
- Version numbers must sync across all SDKs
- Breaking changes require major version bump
- Include type stubs (`.pyi`) for Python SDK
- Include JSDoc for JavaScript SDK
