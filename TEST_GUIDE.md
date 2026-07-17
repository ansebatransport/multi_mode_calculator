# Calculator Test Guide & User Manual

## 1. STANDARD MODE

### Button Functions
| Button | Function | How to Use |
|--------|----------|------------|
| 0-9 | Digits | Tap to enter numbers |
| . | Decimal point | Tap after digits for decimals |
| + - × ÷ | Basic operations | Tap number, operator, number, = |
| = | Equals | Evaluates the expression |
| C | Clear all | Resets calculator |
| CE | Clear entry | Clears current number only |
| ⌫ | Backspace | Deletes last digit |
| ± | Negate | Toggles positive/negative |
| % | Percent | Divides by 100 (or applies to running expression) |
| x² | Square | Squares current number |
| √ | Square root | Square roots current number |
| 1/x | Reciprocal | 1 divided by current number |

### Test Values (Expected Results)
```
2 + 3          = 5
10 - 4         = 6
7 × 8          = 56
20 ÷ 4         = 5
3.14 + 2.86    = 6
(-5) + 3       = -2       (use ± then enter 5)
100 ÷ 3        = 33.333333333
999 × 999      = 998001
1000000 ÷ 7    = 142857.142857
```

### Keyboard Shortcuts
- `0-9`, `.`, `+`, `-`, `*`, `/` — type numbers and operators
- `Enter` or `=` — evaluate
- `Backspace` — delete last digit
- `Escape` — clear all
- `Delete` — clear entry

---

## 2. SCIENTIFIC MODE

### Additional Functions
| Button | Function | Input Format |
|--------|----------|-------------|
| sin, cos, tan | Trigonometry | Enter number, tap function |
| sin⁻¹, cos⁻¹, tan⁻¹ | Inverse trig | Same |
| sinh, cosh, tanh | Hyperbolic | Same |
| ln | Natural log (base e) | Same |
| log | Log base 10 | Same |
| x² | Square | Same |
| xʸ | Power | Enter base, tap xʸ, enter exponent, = |
| √ | Square root | Same |
| ³√ | Cube root | Same |
| 10ˣ | 10 to power | Enter exponent |
| eˣ | e to power | Enter exponent |
| n! | Factorial | Enter integer |
| π | Pi constant | Inserts 3.14159... |
| e | Euler's number | Inserts 2.71828... |
| mod | Modulo | Remainder division |
| DEG/RAD/GRAD | Angle mode toggle | Tap to cycle |
| ( ) | Parentheses | For grouping |

### Test Values (Angles in DEG mode, convert to RAD for API)
```
sin(90°)       = 1        → API: sin(pi/2) = 1
cos(0°)        = 1        → API: cos(0) = 1
tan(45°)       = 1        → API: tan(pi/4) = 1
sin(30°)       = 0.5      → API: sin(pi/6) = 0.5
asin(1)        = 90°      → API: asin(1) = pi/2 ≈ 1.5708
acos(0)        = 90°      → API: acos(0) = pi/2 ≈ 1.5708
ln(e)          = 1        → API: ln(e) = 1
log(100)       = 2        → API: log(100) = 2
log(1000)      = 3
sinh(1)        = 1.1752
cosh(1)        = 1.5431
sqrt(144)      = 12
³√(27)         = 3
5²             = 25
2^10           = 1024     → 2**10
5!             = 120      → factorial(5)
π              = 3.14159265359
e              = 2.71828182846
```

---

## 3. PROGRAMMER MODE

### Button Functions
| Button | Function | How to Use |
|--------|----------|------------|
| HEX/DEC/OCT/BIN | Base selector | Tap to switch active base |
| A-F | Hex digits | Only active in HEX mode |
| C | Clear | Resets to 0 |
| ⌫ | Backspace | Deletes last digit |
| AND OR XOR NOT | Bitwise ops | a OP b = result |
| « » | Bit shift left/right | a « b or a » b |
| ± | Negate | Toggle sign |
| = | Equals | Completes pending operation |

### Test Values
```
DEC 255 → HEX = FF
DEC 1024 → BIN = 10000000000
HEX FF → DEC = 255
BIN 1010 → DEC = 10
OCT 77 → DEC = 63

255 AND 15   = 15      (0xFF & 0x0F)
255 OR 16    = 271     (0xFF | 0x10)
12 XOR 10    = 6       (0b1100 ^ 0b1010)
NOT 0        = -1      (bitwise NOT)
255 AND 128  = 128
```

---

## 4. GRAPH MODE

### How to Use
1. Type a function in the f(x) field
2. Set X and Y ranges
3. Click **Plot** to draw

### Function Syntax
| You Write | Meaning |
|-----------|---------|
| sin(x) | Sine function |
| cos(x) | Cosine |
| x**2 or x^2 | Parabola |
| sqrt(x) | Square root |
| log(x) | Log base 10 |
| ln(x) | Natural log |
| abs(x) | Absolute value |
| 1/x | Reciprocal |
| exp(x) | e^x |
| tan(x) | Tangent |
| x**3 | Cubic |
| sin(x)/x | Sinc function |
| sqrt(abs(x)) | Semicircle shape |

### Test Functions (verify visually)
```
f(x) = x^2       — Parabola opening up, vertex at (0,0)
f(x) = sin(x)    — Wave, period ~6.28, amplitude 1
f(x) = cos(x)    — Wave shifted left from sin
f(x) = 1/x       — Hyperbola, asymptotes at x=0 and y=0
f(x) = abs(x)    — V-shape, vertex at origin
f(x) = sqrt(x)   — Only positive x, half-parabola
f(x) = log(x)    — Only positive x, passes through (1,0)
f(x) = x^3       — S-curve through origin
```

### Range Suggestions
- sin/cos: X: -10 to 10, Y: -2 to 2
- x^2: X: -5 to 5, Y: 0 to 25
- 1/x: X: -10 to 10, Y: -10 to 10
- sqrt(x): X: 0 to 20, Y: 0 to 5

---

## 5. UNIT CONVERTER

### How to Use
1. Select a **Category** (Length, Weight, Temperature, etc.)
2. Pick **From** and **To** units
3. Enter a value — result updates live
4. Use **⇄** button to swap units

### Categories & Test Values
| Category | From | To | Input | Expected |
|----------|------|----|-------|----------|
| Length | Kilometer | Mile | 1 | 0.621371 |
| Length | Meter | Foot | 1 | 3.28084 |
| Length | Inch | Centimeter | 1 | 2.54 |
| Length | Mile | Kilometer | 1 | 1.60934 |
| Weight | Kilogram | Pound | 1 | 2.20462 |
| Weight | Ounce | Gram | 1 | 28.3495 |
| Temperature | Celsius | Fahrenheit | 100 | 212 |
| Temperature | Fahrenheit | Celsius | 32 | 0 |
| Temperature | Celsius | Kelvin | 0 | 273.15 |
| Area | Acre | Square Meter | 1 | 4046.86 |
| Volume | Gallon (US) | Liter | 1 | 3.78541 |
| Speed | km/h | mph | 100 | 62.1371 |
| Data Storage | Gigabyte | Megabyte | 1 | 1024 |
| Time | Hour | Minute | 1 | 60 |
| Energy | Kilocalorie | Joule | 1 | 4184 |
| Pressure | Atmosphere | PSI | 1 | 14.6959 |
| Angle | Degree | Radian | 180 | 3.14159 (π) |

### All Categories Available
Length, Weight, Temperature, Area, Volume, Speed, Data Storage, Time, Pressure, Energy, Angle

---

## 6. FINANCIAL MODE

### 6.1 TVM (Time Value of Money)
Leave **one** field empty to solve for it. Fill the other four.

| Test Case | N | I/Y | PV | PMT | FV | Solve For | Expected |
|-----------|---|-----|-----|------|-----|-----------|----------|
| Savings growth | 10 | 5 | -1000 | 0 | ? | FV | ≈ 1628.89 |
| Loan payment | 360 | 6 | 200000 | ? | 0 | PMT | ≈ 1199.10 |
| How long to save | 60 | ? | 0 | -500 | -50000 | I/Y | ≈ 0.7556% |
| Present value | 20 | 4 | ? | -1000 | 0 | PV | ≈ -13590.33 |

### 6.2 Mortgage
| Test Case | Amount | Rate | Years | Expected Monthly |
|-----------|--------|------|-------|-----------------|
| Standard | $250,000 | 6.5% | 30 | $1,580.17 |
| Low rate | $400,000 | 3.5% | 30 | ≈ $1,796.18 |
| Short term | $150,000 | 5% | 15 | ≈ $1,186.19 |

### 6.3 Car Loan
| Test Case | Price | Rate | Months | Expected Monthly |
|-----------|-------|------|--------|-----------------|
| New car | $35,000 | 5.9% | 60 | ≈ $675.73 |
| Used car | $20,000 | 7.5% | 48 | ≈ $484.97 |

### 6.4 Interest Calculator
| Test Case | Principal | Rate | Time | Type | Expected |
|-----------|-----------|------|------|------|----------|
| Simple | $10,000 | 5% | 3 yr | Simple | Interest=$1,500, Total=$11,500 |
| Compound | $10,000 | 5% | 3 yr | Compound (monthly) | Amount≈$11,614.72, Interest≈$1,614.72 |
| Compound | $5,000 | 8% | 10 yr | Compound (annual) | Amount≈$10,794.62 |

### 6.5 NPV / IRR / MIRR
| Test Case | Rate | Cash Flows | Expected |
|-----------|------|------------|----------|
| NPV | 10% | -1000,300,400,500,600 | ≈ $278.15 |
| IRR | — | -1000,300,400,500,600 | ≈ 17.80% |
| NPV | 8% | -50000,15000,20000,25000,30000 | ≈ $19,606.93 |
| IRR | — | -50000,15000,20000,25000,30000 | ≈ 22.56% |
| MIRR | 5% / 8% | -1000,300,400,500,600 | ≈ 14.99% |

### 6.6 Depreciation
| Test Case | Cost | Salvage | Life | Method | Year 1 Dep | Expected |
|-----------|------|---------|------|--------|-----------|----------|
| SL | $50,000 | $5,000 | 10 | Straight Line | — | $4,500/yr |
| DDB | $50,000 | $5,000 | 10 | Double Declining | — | $10,000 (Y1) |
| SYD | $50,000 | $5,000 | 5 | Sum of Years | — | $15,000 (Y1) |
| SL | $100,000 | $10,000 | 5 | Straight Line | — | $18,000/yr |

### 6.7 Bond Calculator
| Test Case | Face | Coupon | YTM | Years | Expected Price |
|-----------|------|--------|-----|-------|---------------|
| Premium bond | $1,000 | 8% | 6% | 10 | ≈ $1,147.20 |
| Discount bond | $1,000 | 4% | 6% | 10 | ≈ $851.23 |
| Par bond | $1,000 | 6% | 6% | 10 | = $1,000.00 |

### 6.8 Break-Even Analysis
| Test Case | Fixed Costs | Price/Unit | Var Cost/Unit | Expected Units | Expected Revenue |
|-----------|-------------|------------|---------------|----------------|-----------------|
| Basic | $50,000 | $25 | $10 | 3,334 | $83,350 |
| High margin | $100,000 | $50 | $15 | 2,858 | $142,900 |

### 6.9 ROI
| Test Case | Investment | Return | Years | Expected ROI | Expected Annualized |
|-----------|-----------|--------|-------|-------------|-------------------|
| Simple | $10,000 | $15,000 | 1 | 50% | 50% |
| Multi-year | $10,000 | $20,000 | 3 | 100% | ≈ 25.99% |
| Short | $5,000 | $6,000 | 2 | 20% | ≈ 9.54% |

### 6.10 Profit Margin
| Test Case | Revenue | Cost | Expected Margin | Expected Markup |
|-----------|---------|------|----------------|-----------------|
| Basic | $100,000 | $60,000 | 40% | 66.67% |
| High margin | $500 | $150 | 70% | 233.33% |
| Low margin | $1,000 | $900 | 10% | 11.11% |

---

## Quick Reference: Keyboard Shortcuts (Standard/Scientific)
| Key | Action |
|-----|--------|
| 0-9 | Digit |
| + - * / | Operators |
| Enter / = | Evaluate |
| Backspace | Delete last |
| Escape | Clear all |
| Delete | Clear entry |
| . | Decimal point |
