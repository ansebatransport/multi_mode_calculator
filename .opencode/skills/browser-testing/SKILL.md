---
name: browser-testing
description: Use when testing web UI visually, taking screenshots, verifying layouts, or doing end-to-end testing. Trigger on phrases like "test in browser", "screenshot", "visual test", "check UI", "verify layout", "browser test", "end to end", "e2e", or when validating the web app appearance.
---

# Browser Testing Skill

Visual verification and end-to-end testing of the web app.

## Tools Available

### curl (Basic)
```bash
# Test all API endpoints
curl -s http://localhost:5000/api/health
curl -s -X POST http://localhost:5000/api/calculate -H "Content-Type: application/json" -d '{"expression":"2+3"}'
```

### wget (Page Download)
```bash
# Download page for inspection
wget -q -O - http://localhost:5000/ | head -50

# Save full page
wget -q http://localhost:5000/ -O /tmp/page.html
```

### headless Chromium (Full Testing)
```bash
# Install if available
# chromium-browser --headless --screenshot=/tmp/screenshot.png http://localhost:5000

# Or with puppeteer
# npx puppeteer screenshot http://localhost:5000 /tmp/screenshot.png
```

## Visual Testing Checklist

### Layout Verification
- [ ] Calculator card centered on page
- [ ] Dark gradient background visible (#1a1a2e → #16213e)
- [ ] Red operator buttons (#e94560)
- [ ] Green equals button (#2ed573)
- [ ] White text on dark background
- [ ] 20px border-radius on card
- [ ] 12px border-radius on buttons

### Mode Switching
- [ ] Standard mode shows basic buttons
- [ ] Scientific mode shows sin/cos/tan/log/etc.
- [ ] Programmer mode shows HEX/DEC/OCT/BIN
- [ ] Graph mode shows canvas
- [ ] Unit converter shows dropdowns
- [ ] Financial mode shows tabs

### Interactive Elements
- [ ] Buttons respond to clicks
- [ ] Display updates correctly
- [ ] Keyboard input works
- [ ] History panel shows entries
- [ ] Mode menu opens/closes

## API Endpoints to Test

```bash
#!/bin/bash
# test_web_app.sh

BASE="http://localhost:5000"

echo "=== Health Check ==="
curl -s $BASE/api/health | python3 -m json.tool

echo "=== Standard Calculator ==="
curl -s -X POST $BASE/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 3 * 4"}' | python3 -m json.tool

echo "=== Scientific Calculator ==="
curl -s -X POST $BASE/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "sin(pi/4)", "angle_mode": "radians"}' | python3 -m json.tool

echo "=== Programmer Calculator ==="
curl -s -X POST $BASE/api/programmer/convert \
  -H "Content-Type: application/json" \
  -d '{"number": 255, "from_base": 10}' | python3 -m json.tool

echo "=== Unit Conversion ==="
curl -s -X POST $BASE/api/unit/convert \
  -H "Content-Type: application/json" \
  -d '{"value": 1, "from_unit": "kg", "to_unit": "lb"}' | python3 -m json.tool

echo "=== Financial Mortgage ==="
curl -s -X POST $BASE/api/financial/mortgage \
  -H "Content-Type: application/json" \
  -d '{"principal": 100000, "annual_rate": 0.05, "years": 30}' | python3 -m json.tool

echo "=== Error Handling ==="
curl -s -X POST $BASE/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "1/0"}' | python3 -m json.tool
```

## Screenshot Verification (When Available)

```bash
# Capture screenshot
chromium-browser --headless --screenshot=/tmp/calc.png \
  --window-size=1280,720 http://localhost:5000

# Verify screenshot exists
ls -la /tmp/calc.png

# Compare screenshots (if imagemagick installed)
# compare /tmp/baseline.png /tmp/calc.png /tmp/diff.png
```

## Responsive Testing

```bash
# Test different viewport sizes
for size in "320,568" "768,1024" "1280,720" "1920,1080"; do
    width=$(echo $size | cut -d, -f1)
    height=$(echo $size | cut -d, -f2)
    echo "Testing ${width}x${height}..."
    # chromium-browser --headless --screenshot="/tmp/calc_${width}.png" \
    #   --window-size=$size http://localhost:5000
done
```

## Rules

- ALWAYS test API endpoints before UI changes
- Check both success and error responses
- Verify responsive layout at multiple sizes
- Screenshot before and after UI changes
- Test keyboard navigation and accessibility
- Verify color contrast meets WCAG standards
