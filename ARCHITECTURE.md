# Multi-Mode Calculator — Architecture & Design Reference

> **Purpose:** This document explains how the calculator is built, how the pieces fit together, and why it was designed this way. It is written for anyone on the team — including non-programmers — who needs to understand the system or plan future changes.

---

## 1. What This Application Is

A professional calculator that does six different jobs from a single application:

1. **Standard** — everyday arithmetic (add, subtract, multiply, divide)
2. **Scientific** — trigonometry, logarithms, powers, constants
3. **Programmer** — work with binary, hexadecimal, and bitwise logic
4. **Graph** — plot mathematical functions visually
5. **Unit Converter** — convert between 11 categories (length, weight, temperature, etc.)
6. **Financial** — loans, investments, depreciation, bonds, break-even analysis

It currently runs as a **web application** in any browser. Designs for desktop and mobile versions exist and can be activated later.

---

## 2. The Big-Picture Design (Three Layers)

The application follows a simple three-layer pattern. Think of it like a restaurant:

```
┌─────────────────────────────────────────────────┐
│              PRESENTATION LAYER                 │
│   (What the user sees and clicks)               │
│                                                 │
│   Web app:  HTML + CSS + JavaScript in browser  │
│   Desktop:  Flet (Python UI toolkit)            │
│   Mobile:   Flet (Python UI toolkit)            │
├─────────────────────────────────────────────────┤
│              TRANSPORT LAYER                    │
│   (How the front and back talk to each other)   │
│                                                 │
│   Web: 18 REST API calls over HTTP              │
│   Desktop/Mobile: Direct Python function calls   │
├─────────────────────────────────────────────────┤
│              LOGIC LAYER (core/)                │
│   (All the math, financial formulas, etc.)      │
│                                                 │
│   40 pure-Python modules with zero UI code      │
│   860 automated tests verify correctness        │
└─────────────────────────────────────────────────┘
```

### Why Three Layers?

- **The math never changes** whether it runs on a phone, a desktop, or in a browser. So we write it once in the Logic Layer.
- **The look and feel is different** on each platform (big touch buttons on mobile, hover effects on desktop, browser-based for web). So each platform has its own Presentation Layer.
- **The Transport Layer** is the bridge. On the web, the browser sends data over the network to the server. On desktop/mobile, Python calls the math functions directly — no network needed.

---

## 3. The Logic Layer — The "Brain" (core/)

This is the heart of the application. It lives in 40 Python files totaling about 3,700 lines of code. **None of these files know anything about buttons, screens, or browsers.** They only do math and data management.

### 3.1 The Expression Pipeline

When you type `2 + 3 * 4` and press `=`, this is what happens:

```
You type:    "2 + 3 * 4"
                │
                ▼
┌─────────────────────────────┐
│  STEP 1: TOKENIZER          │
│  Breaks the text into       │
│  meaningful pieces:         │
│  [2] [+] [3] [×] [4]       │
└─────────────────────────────┘
                │
                ▼
┌─────────────────────────────┐
│  STEP 2: SHUNTING-YARD      │
│  Rearranges using math      │
│  rules (multiplication      │
│  before addition):          │
│  [2] [3] [4] [×] [+]       │
└─────────────────────────────┘
                │
                ▼
┌─────────────────────────────┐
│  STEP 3: EVALUATOR          │
│  Walks through and          │
│  calculates:                │
│  3 × 4 = 12                │
│  2 + 12 = 14               │
│                             │
│  Result: 14                 │
└─────────────────────────────┘
```

The three steps are handled by three dedicated modules:
- **expression_parser.py** — Tokenizes and rearranges (Steps 1 & 2)
- **engine.py** — Evaluates the rearranged expression (Step 3)
- **rpn_engine.py** — An alternative stack-based evaluator

### 3.2 Core Module Map

Here is every module grouped by what job it does:

#### Math & Computation
| Module | What It Does |
|--------|-------------|
| engine.py | Evaluates math expressions — the central calculator brain |
| expression_parser.py | Parses text like "sin(pi/2)" into instructions the engine can follow |
| rpn_engine.py | Alternative expression evaluator (Reverse Polish Notation) |
| graph_engine.py | Computes plot points for graphing functions |
| equation_solver.py | Solves linear, quadratic, and cubic equations |
| matrices.py | Matrix operations (add, multiply, inverse, determinant) |
| complex_numbers.py | Complex number arithmetic |
| fractions.py | Converts decimals to fractions |
| statistics.py | Mean, median, mode, variance, standard deviation |
| distributions.py | Probability distributions (normal, binomial, etc.) |
| regression.py | Line and curve fitting to data points |
| sequences.py | Arithmetic and geometric sequences, Fibonacci |
| parametric.py | Parametric curve evaluation for graphing |
| polar_coords.py | Converts between (x,y) and (r, angle) coordinates |
| dms.py | Degrees-minutes-seconds conversions |
| recurring_decimal.py | Detects repeating decimal patterns |
| random_generator.py | Random numbers in various distributions |

#### Financial
| Module | What It Does |
|--------|-------------|
| financial.py | TVM solver, depreciation schedules, bond pricing, NPV/IRR/MIRR, break-even, ROI, profit margin (348 lines — the largest module) |
| worksheets.py | Mortgage, car loan, simple & compound interest, fuel economy |

#### Data & Conversion
| Module | What It Does |
|--------|-------------|
| unit_converter.py | Converts between 11 categories of measurement units |
| currency_converter.py | Converts between currencies (with offline cache) |
| base_converter.py | Converts numbers between binary, octal, decimal, hexadecimal |
| date_calculator.py | Date arithmetic (days between, add/subtract days) |
| constants_lib.py | Physical and mathematical constants (speed of light, Planck, etc.) |

#### App Infrastructure
| Module | What It Does |
|--------|-------------|
| history.py | Stores calculation history with persistence |
| clipboard.py | Shared clipboard for copying results across modes |
| memory.py | Calculator memory registers (M0 through M9) |
| undo_redo.py | Undo/redo system for calculator actions |
| commands.py | Command pattern base classes for undo/redo |
| variables.py | Named variable storage for scientific work |
| user_functions.py | User-defined custom functions |
| settings.py | User preferences with file persistence |
| themes.py | Dark/light theme management |
| autosave.py | Saves and restores your work between sessions |
| state_manager.py | Remembers state when you switch between modes |
| validators.py | Checks that user input is valid before processing |
| error_handler.py | Friendly error messages for math problems |
| export_import.py | Save/load history as JSON or CSV files |
| natural_display.py | Renders math in textbook-style notation |
| textbook_notation.py | Supporting logic for natural display |

### 3.3 Key Design Rule: No UI Code in core/

Every module in `core/` follows one strict rule: **it never imports any UI library** (no Flask, no Flet, no tkinter). This means:

- The same math code runs everywhere — web, phone, desktop
- We can test every formula without launching a screen
- Changing the look of the app never touches the math

---

## 4. The Presentation Layer — What the User Sees

### 4.1 Web Application (apps/web/)

This is the version that runs today. It has four files:

```
apps/web/
├── run.py                  → Starts the server (9 lines)
├── app.py                  → Flask backend + 18 API routes (235 lines)
├── templates/
│   └── index.html          → The single-page HTML structure (413 lines)
└── static/
    ├── style.css            → All visual styling, dark theme (787 lines)
    └── script.js            → All button logic, API calls, mode switching (794 lines)
```

**How the web app works:**

1. Your browser requests `http://localhost:5000/`
2. Flask sends back `index.html` — a single page with all six modes hidden inside
3. `style.css` paints the dark theme with colored buttons (red operators, green equals, dark background)
4. `script.js` handles every button click, keystroke, and mode switch — all in the browser
5. When you press `=`, JavaScript sends the expression to Flask over HTTP, Flask runs the core math, and sends the answer back

```
┌──────────────┐    HTTP POST     ┌──────────────┐    Calls     ┌──────────────┐
│   Browser    │ ──────────────→  │  Flask API   │ ──────────→  │  core/ math  │
│  (JS/HTML)   │ ←────────────── │  (app.py)    │ ←────────── │  modules     │
│              │    JSON answer   │              │   answer     │              │
└──────────────┘                  └──────────────┘              └──────────────┘
```

### 4.2 Desktop Application (apps/desktop/) — Ready, Not Active

Built with Flet (a Python UI toolkit). Would run as a native window on Windows, macOS, or Linux. Features designed:
- Custom title bar with window controls
- Hamburger menu for mode switching
- Compact centered calculator that expands when maximized
- Keyboard shortcuts

### 4.3 Mobile Application (apps/mobile/) — Ready, Not Active

Also built with Flet, designed for touch:
- Large 56-pixel-tall buttons for easy tapping
- Bottom navigation bar instead of hamburger menu
- Full-width layout optimized for phone screens

---

## 5. The Web App — Detailed Component Map

### 5.1 The Six Mode Pages

Each mode is a `<div class="page">` inside `index.html`. Only one is visible at a time. Switching modes shows/hides these divs:

```
Standard ──────→ Basic number pad + operations
                  Display: expression + result
                  24 buttons

Scientific ────→ Extended pad with trig, log, powers
                  Display: angle mode indicator + expression + result
                  48 buttons (6 columns)

Programmer ────→ Base conversion + bitwise operations
                  Display: result + HEX/DEC/OCT/BIN readout
                  30 buttons (5 columns) + hex A-F keys

Graph ─────────→ Function input + canvas + range controls
                  Canvas: real-time plotted function
                  8 preset buttons (sin, cos, x², etc.)

Unit Converter → Category dropdown + unit selectors + value fields
                  11 categories, ~100 units total

Financial ─────→ 6 sub-tabs with specialized forms
                  TVM, Loans, NPV/IRR, Depreciation, Bond, Business
```

### 5.2 The Financial Sub-System (Most Complex Page)

The financial mode has the most features, organized into tabs:

```
Financial Mode
├── TVM ──────────── Solve for any one of N, I/Y, PV, PMT, FV
├── Loans ────────── Three sub-tabs:
│   ├── Mortgage ─── Monthly payment from principal, rate, years
│   ├── Car Loan ─── Monthly payment from price, rate, months
│   └── Interest ─── Simple or compound interest
├── NPV/IRR ──────── Investment analysis
│   └── Also: MIRR (Modified Internal Rate of Return)
├── Depreciation ──── Three methods:
│   ├── Straight Line
│   ├── Double Declining Balance
│   └── Sum of Years Digits
│   (Results shown as a scrollable table)
├── Bond ──────────── Bond price, yield, coupon analysis
└── Business ──────── Three sub-tabs:
    ├── Break-Even ── Units and revenue to break even
    ├── ROI ────────── Return on investment over time
    └── Margin ──────── Gross profit, margin %, markup %
```

### 5.3 API Endpoints — The Bridge Between Browser and Math

When the browser needs to calculate something, it sends an HTTP request to one of 18 endpoints:

| Endpoint | What It Calculates |
|----------|-------------------|
| `POST /api/calculate` | Any math expression (2+3, sin(pi/2), etc.) |
| `POST /api/programmer/convert` | Convert number between bases (DEC→HEX, etc.) |
| `POST /api/programmer/bitwise` | AND, OR, XOR, NOT, shift operations |
| `GET /api/unit/categories` | List all unit categories and their units |
| `POST /api/unit/convert` | Convert between any two units |
| `POST /api/financial/tvm` | Time Value of Money (solve for any variable) |
| `POST /api/financial/npv` | Net Present Value of cash flows |
| `POST /api/financial/irr` | Internal Rate of Return |
| `POST /api/financial/mirr` | Modified IRR with finance/reinvest rates |
| `POST /api/financial/mortgage` | Monthly mortgage payment |
| `POST /api/financial/amortization` | Full payment schedule (month-by-month) |
| `POST /api/financial/car_loan` | Monthly car loan payment |
| `POST /api/financial/interest` | Simple or compound interest |
| `POST /api/financial/depreciation` | Depreciation schedule (3 methods) |
| `POST /api/financial/bond` | Bond price and yield |
| `POST /api/financial/break_even` | Break-even units and revenue |
| `POST /api/financial/roi` | Return on investment |
| `POST /api/financial/profit_margin` | Gross margin and markup |

---

## 6. Data Flow — A Calculation from Start to Finish

Here is exactly what happens when a user types `sin(pi/2)` in Scientific mode and presses `=`:

```
1. USER TYPES     "sin(pi/2)" in the text input
        │
2. JAVASCRIPT     Captures the expression string
        │
3. HTTP REQUEST   POST to /api/calculate
                  Body: {"expression": "sin(pi/2)", "angle_mode": "radians"}
        │
4. FLASK RECEIVES request, passes to core modules
        │
5. TOKENIZER      ["sin", "(", "pi", "/", "2", ")"]
        │          Recognizes "sin" as function, "pi" as constant
        │
6. SHUNTING-YARD  Rearranges to: [pi] [2] [/] [sin]
        │          (Division first, then apply sin)
        │
7. EVALUATOR
   ├─ Push 3.14159 (pi)
   ├─ Push 2
   ├─ Divide: 3.14159 / 2 = 1.5708
   └─ Apply sin: sin(1.5708) = 1.0
        │
8. HTTP RESPONSE  {"result": 1.0}
        │
9. JAVASCRIPT     Updates display: "1"
        │
10. USER SEES     Result on screen
```

---

## 7. Testing Strategy

### 7.1 What We Test

Every core module has its own test file. There are **37 unit test files** with **860 individual tests**. These verify:

- Correct mathematical answers for known inputs
- Edge cases (division by zero, negative numbers, very large numbers)
- Error handling (invalid inputs, overflow)
- Persistence (save and reload settings, history)

### 7.2 Integration Tests

Four integration tests verify that modules work together:

| Test | What It Verifies |
|------|-----------------|
| test_calculation_pipeline | Full expression → parse → evaluate → result flow |
| test_export_import_integration | Export history → import → verify data intact |
| test_history_clipboard_integration | Copy result → paste into new calculation |
| test_mode_switching | Switch modes without losing state |

### 7.3 How to Run Tests

```bash
cd multi_mode_calculator
python3 -m pytest tests/ -q
# Output: 860 passed in ~1 second
```

---

## 8. How the Project Is Organized on Disk

```
multi_mode_calculator/
│
├── core/                    ← The brain (40 modules, no UI)
│   ├── engine.py            ← Central math evaluator
│   ├── expression_parser.py ← Parses math text
│   ├── financial.py         ← All financial formulas
│   ├── unit_converter.py    ← Unit conversions
│   └── ... (36 more)
│
├── apps/                    ← User-facing applications
│   ├── web/                 ← Flask web app (ACTIVE)
│   │   ├── app.py           ← Server + API routes
│   │   ├── run.py           ← Start command
│   │   ├── templates/       ← HTML page
│   │   └── static/          ← CSS + JavaScript
│   ├── desktop/             ← Flet desktop app (READY)
│   └── mobile/              ← Flet mobile app (READY)
│
├── tests/                   ← All 860 tests
│   ├── core/                ← Unit tests for each module
│   └── integration/         ← Tests that combine modules
│
├── utils/
│   └── constants.py         ← Theme color definitions
│
├── pyproject.toml           ← Project metadata and dependencies
├── TEST_GUIDE.md            ← Values to verify each feature
└── ARCHITECTURE.md          ← This document
```

---

## 9. Design Principles

These are the rules the project follows. They guide every decision:

### Principle 1: Separate Logic from Presentation
The math never knows about buttons. Buttons never know about formulas. This means we can swap the entire UI without retesting the math.

### Principle 2: Each Platform Gets Its Own Entry Point
The web app has `apps/web/run.py`. The desktop has `apps/desktop/run.py`. The mobile has `apps/mobile/run.py`. They all share `core/` but are otherwise independent.

### Principle 3: Test Everything, Automatically
Every core module has tests. Every change is verified in under 1 second. If a test breaks, we know immediately.

### Principle 4: Minimal Dependencies
The core uses only Python's built-in math library. No external packages for calculations. This means the math works on any Python 3.10+ installation without installing anything extra.

### Principle 5: Persist User State Silently
History, settings, clipboard, and theme preferences are saved automatically. The user never has to think about saving.

---

## 10. How to Extend the Application

### Adding a New Calculator Mode
1. Create the UI page in the Presentation Layer (HTML for web, Flet for desktop/mobile)
2. If it needs new math, add a module in `core/`
3. Add API endpoints in `apps/web/app.py` (if the math lives server-side)
4. Add tests in `tests/core/`
5. Register the mode in the hamburger menu in all apps

### Adding a New Financial Feature
1. Add the formula in `core/financial.py` (or `core/worksheets.py`)
2. Add a test with known inputs and expected outputs in `tests/core/test_financial.py`
3. Add an API endpoint in `apps/web/app.py`
4. Add a tab or sub-tab in the financial page HTML
5. Add the JavaScript handler in `script.js`

### Adding a New Unit Category
1. Add units to the `UNITS` dictionary in `core/unit_converter.py`
2. Add a test in `tests/core/test_unit_converter.py`
3. The web UI will automatically show the new category (no frontend changes needed)

---

## 11. Current Statistics

| Metric | Value |
|--------|-------|
| Total Python code | ~10,300 lines |
| Total frontend code (HTML+CSS+JS) | ~2,000 lines |
| Core modules | 40 |
| API endpoints | 18 |
| Calculator modes | 6 |
| Unit categories | 11 (~100 units) |
| Automated tests | 860 |
| Test execution time | ~1 second |
| External dependencies | Flask (web), Flet (desktop/mobile) |
| Python version required | 3.10 or higher |

---

## 12. Future Roadmap

| Priority | Item | Notes |
|----------|------|-------|
| Done | Web application | Running on port 5000 |
| Done | Financial sub-system | TVM, loans, depreciation, bonds, business |
| Ready | Desktop application | Code complete, needs testing |
| Ready | Mobile application | Code complete, needs testing |
| Planned | User-defined functions | Core module exists, UI needed |
| Planned | Matrix mode UI | Core module exists, UI needed |
| Planned | Statistics mode UI | Core module exists, UI needed |
| Planned | Currency rates (live) | Offline mode exists, API integration needed |
| Planned | Accessibility | Screen reader support, high contrast |
| Planned | PWA support | Installable as a web app on phones |

---

*Last updated: July 17, 2026*
