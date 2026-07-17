# Multi-Mode Calculator

A professional, full-featured multi-mode calculator application built with Python. Supports 6 calculator modes, 14+ specialized dialogs, persistent history, shared clipboard, and cross-platform deployment (Android, iOS, Web, Desktop).

## Features

### 6 Calculator Modes
| Mode | Description |
|------|-------------|
| **Standard** | Basic arithmetic with memory, history, and undo/redo |
| **Scientific** | Trig, logarithms, powers, constants, hyperbolic functions, angle modes (DEG/RAD/GRAD) |
| **Programmer** | HEX/DEC/OCT/BIN conversion, bitwise operators, QWORD/DWORD/WORD/BYTE word sizes |
| **Graph** | Function plotting, zoom/pan, trace mode, multiple functions, parametric & polar |
| **Unit Converter** | 7 categories (Length, Weight, Temperature, Volume, Area, Speed, Data), bidirectional |
| **Financial** | TVM solver, amortization, NPV/IRR/MIRR, depreciation, bond pricing, break-even |

### 14+ Dialogs
Statistics, Equation Solver, Date Calculator, Percentage, Matrix Calculator, Complex Numbers, Distribution Calculator, Physical Constants, Currency Converter, Worksheet Templates, Variable Manager, Export/Import, Random Number Generator, Help & Shortcuts

### Core Capabilities
- **Expression Engine**: Shunting-yard parser + RPN evaluator with operator precedence
- **Memory Registers**: M0-M9 with store/recall/add/subtract
- **History**: Persistent calculation history (100 entries)
- **Shared Clipboard**: 20-entry clipboard for sharing values between modes
- **Undo/Redo**: Full undo/redo stack
- **Auto-Save**: Persists state across sessions
- **Themes**: Dark and light theme support
- **Natural Display**: Mathematical notation rendering (fractions, roots, etc.)

## Tech Stack
- **Primary UI**: [Flet](https://flet.dev) 0.86.0 (cross-platform Flutter-based)
- **Fallback UI**: Tkinter (stdlib, desktop only)
- **Math Core**: Pure Python stdlib (math, cmath, ast, re, json)
- **Tests**: unittest + pytest (860 tests, <1s runtime)
- **Build**: Hatchling + `flet build` for platform packages

## Project Structure
```
multi_mode_calculator/
├── main.py                    # Entry point
├── pyproject.toml             # Project config
├── core/                      # 40 pure Python modules (no UI deps)
│   ├── engine.py              # Expression evaluator
│   ├── expression_parser.py   # Shunting-yard parser
│   ├── graph_engine.py        # Graph math core
│   ├── financial.py           # TVM, NPV/IRR, depreciation
│   ├── statistics.py          # Descriptive statistics
│   ├── base_converter.py      # Radix conversion
│   ├── matrices.py            # Matrix operations
│   ├── complex_numbers.py     # Complex arithmetic
│   ├── distributions.py       # Probability distributions
│   ├── equation_solver.py     # Linear/quadratic/cubic solver
│   ├── unit_converter.py      # Unit conversion engine
│   ├── currency_converter.py  # Currency conversion
│   └── ...                    # 27 more modules
├── ui/
│   ├── flet_app/              # 46 Flet UI files
│   │   ├── app.py             # Main Flet app shell
│   │   ├── navigation.py      # Hamburger menu
│   │   ├── pages/             # 6 mode pages
│   │   ├── components/        # Display, buttons, sidebars, status bar
│   │   ├── components/dialogs/ # 15 dialog files
│   │   └── widgets/           # 11 specialized widgets
│   └── tkinter_app/           # 16 Tkinter fallback files
├── utils/                     # UI constants and helpers
├── platforms/                 # Build configs (Android, iOS, Web, Desktop)
└── tests/                     # 46 test files (860 tests)
    ├── core/                  # Core module tests
    └── integration/           # Integration tests
```

## Quick Start

### Install Dependencies
```bash
pip install flet pytest
```

### Run (Flet - Primary)
```bash
python main.py
```

### Run (Tkinter Fallback)
```bash
python -m ui.tkinter_app.app
```

### Run Tests
```bash
pytest tests/ -v
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+C` | Copy result to clipboard |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+S` | Save/auto-save |
| `Ctrl+H` | Toggle history sidebar |
| `Escape` | Close dialogs/overlays |
| `Enter` | Evaluate expression |
| `Backspace` | Delete last character |

## Building for Mobile

```bash
# Install Flet CLI
pip install flet-cli

# Build Android APK
flet build apk

# Build iOS IPA (requires macOS + Xcode)
flet build ipa

# Build Web
flet build web

# Build Desktop
flet build windows  # or macos, linux
```

## License

MIT
