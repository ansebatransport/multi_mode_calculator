---
name: repository-map
description: Use when exploring a codebase, understanding project structure, finding related code, or navigating large projects. Trigger on phrases like "codebase map", "project structure", "find related code", "dependency graph", "callers", "callees", "who uses this", "what calls this", or when navigating unfamiliar code.
---

# Repository Map Skill

Navigate and understand codebase structure efficiently.

## Project Map

```
multi_mode_calculator/
├── core/                          # Pure Python math engine
│   ├── __init__.py
│   ├── engine.py                  # Central calculator (ENTRANCE POINT)
│   ├── expression_parser.py       # Tokenizer + shunting-yard
│   ├── financial.py               # TVM, depreciation, bonds, NPV/IRR
│   ├── unit_converter.py          # 11 categories, ~100 units
│   ├── statistics.py              # Mean, median, std dev
│   ├── graph_engine.py            # Canvas plotting
│   ├── base_converter.py          # HEX/DEC/OCT/BIN
│   ├── matrices.py                # Matrix operations
│   ├── complex_numbers.py         # Complex math
│   ├── equation_solver.py         # Algebra equations
│   ├── regression.py              # Curve fitting
│   ├── distributions.py           # Normal, Poisson, etc.
│   ├── polar_coords.py            # Polar <-> Cartesian
│   ├── parametric.py              # Parametric curves
│   ├── sequences.py               # Arithmetic, geometric
│   ├── fractions.py               # Fraction arithmetic
│   ├── recurring_decimal.py       # Recurring -> fraction
│   ├── dms.py                     # Degrees/minutes/seconds
│   ├── constants_lib.py           # Math constants
│   ├── themes.py                  # Dark/light themes
│   ├── worksheets.py              # Mortgage, car loan, interest
│   ├── validators.py              # Input validation
│   ├── error_handler.py           # Error handling
│   ├── history.py                 # Calculation history
│   ├── clipboard.py               # Copy/paste
│   ├── memory.py                  # Memory functions (M+, M-, MR)
│   ├── undo_redo.py               # Undo/redo stack
│   ├── state_manager.py           # App state management
│   ├── settings.py                # User settings
│   ├── autosave.py                # Auto-save state
│   ├── export_import.py           # Export/import data
│   ├── natural_display.py         # Pretty-print expressions
│   ├── rpn_engine.py              # Reverse Polish Notation
│   ├── commands.py                # Command patterns
│   ├── variables.py               # User variables
│   ├── user_functions.py          # Custom functions
│   ├── random_generator.py        # Random numbers
│   └── currency_converter.py      # Currency exchange
│
├── apps/
│   ├── web/
│   │   ├── app.py                 # Flask routes (18 endpoints)
│   │   ├── run.py                 # Server entry point
│   │   ├── templates/
│   │   │   └── index.html         # Single-page UI
│   │   └── static/
│   │       ├── style.css          # Dark theme styles
│   │       └── script.js          # Button logic, API calls
│   │
│   ├── desktop/
│   │   ├── app.py                 # Flet desktop (skeleton)
│   │   └── run.py                 # Desktop entry point
│   │
│   └── mobile/
│       ├── app.py                 # Flet mobile (skeleton)
│       └── run.py                 # Mobile entry point
│
├── tests/
│   ├── core/                      # 33 unit test files
│   ├── integration/               # 4 integration tests
│   └── ui/                        # Placeholder
│
├── utils/
│   └── constants.py               # Theme constants
│
├── .opencode/
│   ├── skills/                    # 24+ skills
│   ├── checkpoints/               # File snapshots
│   ├── playbooks/                 # Reusable workflows
│   └── learnings.md               # Persisted knowledge
│
├── opencode.json                  # Agent configuration
├── AGENTS.md                      # Workflow documentation
├── ARCHITECTURE.md                # Design document
├── TEST_GUIDE.md                  # Test values guide
└── pyproject.toml                 # Project metadata
```

## Dependency Graph

```
engine.py
├── expression_parser.py (parse)
├── constants_lib.py (constants)
├── complex_numbers.py (complex ops)
├── matrices.py (matrix ops)
├── statistics.py (stat functions)
├── fractions.py (fraction math)
├── recurring_decimal.py (recurring)
├── dms.py (DMS conversion)
├── polar_coords.py (polar)
├── parametric.py (parametric)
├── sequences.py (sequences)
├── equation_solver.py (equations)
├── regression.py (regression)
├── distributions.py (probability)
├── graph_engine.py (plotting)
├── base_converter.py (number bases)
├── unit_converter.py (units)
├── financial.py (financial)
└── currency_converter.py (currency)

apps/web/app.py
├── core/engine.py (calculate)
├── core/base_converter.py (programmer)
├── core/unit_converter.py (units)
├── core/financial.py (financial)
├── core/graph_engine.py (graph)
└── core/worksheets.py (worksheets)
```

## Module Responsibilities

| Module | Responsibility | Public API |
|--------|---------------|------------|
| engine.py | Central evaluator | `MathEngine.calculate()` |
| expression_parser.py | Parse expressions | `parse()` → AST |
| financial.py | Financial calculations | `mortgage_payment()`, `depreciation()`, etc. |
| unit_converter.py | Unit conversion | `convert()`, `get_categories()` |
| graph_engine.py | Plot functions | `plot_function()` |
| base_converter.py | Number bases | `to_decimal()`, `from_decimal()` |
| statistics.py | Statistics | `mean()`, `median()`, `std_dev()` |

## Navigation Patterns

### Find all callers of a function
```bash
grep -rn "function_name" core/ apps/
```

### Find all uses of a module
```bash
grep -rn "from core.module import\|import core.module" core/ apps/
```

### Find test coverage
```bash
ls tests/core/test_*.py | sed 's/.*test_//' | sed 's/.py//' | sort
```

### Find untested modules
```bash
diff <(ls core/*.py | sed 's/.*\///' | sed 's/.py//' | sort) \
     <(ls tests/core/test_*.py | sed 's/.*test_//' | sed 's/.py//' | sort)
```

## Quick Reference

### To add a new feature:
1. Add core logic in `core/`
2. Add tests in `tests/core/`
3. Add API route in `apps/web/app.py`
4. Add UI in `apps/web/templates/index.html`
5. Add button logic in `apps/web/static/script.js`

### To fix a bug:
1. Find the bug location using the map above
2. Check existing tests: `tests/core/test_<module>.py`
3. Add regression test
4. Fix the bug
5. Run all tests

### To understand a module:
1. Read `core/<module>.py` docstring
2. Check `tests/core/test_<module>.py` for usage examples
3. Check `apps/web/app.py` for API usage
4. Check `ARCHITECTURE.md` for design context

## Rules

- Update this map when adding new modules
- Keep dependency graph current
- Reference module responsibilities when working in unfamiliar code
- Use grep to find actual usage patterns
