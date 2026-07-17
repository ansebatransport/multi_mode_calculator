---
name: accessibility
description: Use when improving web UI accessibility, adding ARIA labels, keyboard navigation, screen reader support, or WCAG compliance. Trigger on phrases like "accessibility", "a11y", "WCAG", "screen reader", "keyboard", "ARIA", "contrast", "alt text", "focus", or when modifying HTML/CSS in apps/web/.
---

# Accessibility Skill

Make the calculator web app usable by everyone.

## WCAG 2.1 Quick Reference

### Level A (Must Have)
- [ ] All images have `alt` text
- [ ] All form inputs have labels
- [ ] Keyboard can reach all interactive elements
- [ ] Focus order is logical
- [ ] No keyboard traps
- [ ] Page has a title

### Level AA (Should Have)
- [ ] Color contrast ratio ≥ 4.5:1 (text), ≥ 3:1 (large text)
- [ ] Text can be resized to 200% without loss
- [ ] Focus indicators are visible
- [ ] Error messages are descriptive
- [ ] Skip navigation link exists

## Calculator-Specific a11y

### Button Accessibility
```html
<!-- BAD -->
<button onclick="pressButton('7')">7</button>
<button onclick="pressOperator('+')">+</button>

<!-- GOOD -->
<button onclick="pressButton('7')" aria-label="Number 7">7</button>
<button onclick="pressOperator('+')" aria-label="Add" aria-keyshortcuts="+=ShiftEqual">+</button>
<button onclick="calculate()" aria-label="Calculate result" aria-keyshortcuts="Enter">=</button>
<button onclick="clearAll()" aria-label="Clear all" aria-keyshortcuts="Escape">AC</button>
```

### Live Region for Results
```html
<!-- Announce result to screen readers -->
<div aria-live="polite" aria-atomic="true" id="result-region">
  <span id="result">0</span>
</div>

<script>
// Update live region when result changes
function updateResult(value) {
    const region = document.getElementById('result-region');
    region.textContent = `Result: ${value}`;
}
</script>
```

### Keyboard Navigation
```javascript
// Arrow keys to navigate button grid
document.addEventListener('keydown', (e) => {
    const focused = document.activeElement;
    const buttons = Array.from(document.querySelectorAll('.calc-btn'));
    const index = buttons.indexOf(focused);

    switch(e.key) {
        case 'ArrowRight':
            buttons[index + 1]?.focus();
            e.preventDefault();
            break;
        case 'ArrowLeft':
            buttons[index - 1]?.focus();
            e.preventDefault();
            break;
        case 'ArrowDown':
            buttons[index + 4]?.focus(); // 4 columns
            e.preventDefault();
            break;
        case 'ArrowUp':
            buttons[index - 4]?.focus();
            e.preventDefault();
            break;
    }
});
```

### Focus Management
```css
/* Visible focus indicator */
.calc-btn:focus {
    outline: 3px solid #2ed573;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(46, 213, 115, 0.3);
}

/* Skip navigation link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #e94560;
    color: white;
    padding: 8px;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
```

### Screen Reader Only Text
```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

```html
<span class="sr-only">Calculator result:</span>
<span id="result" aria-live="polite">0</span>
```

### Color Contrast Check
```javascript
// Test contrast ratio
function getContrastRatio(hex1, hex2) {
    const lum1 = getLuminance(hex1);
    const lum2 = getLuminance(hex2);
    const lighter = Math.max(lum1, lum2);
    const darker = Math.min(lum1, lum2);
    return (lighter + 0.05) / (darker + 0.05);
}

// Our theme contrast ratios:
// White (#fff) on #0f3460: ~8.5:1 ✓
// White (#fff) on #16213e: ~7.2:1 ✓
// #e94560 on #0f3460: ~3.1:1 (large text only)
// #2ed573 on #0f3460: ~5.8:1 ✓
```

### Modal Accessibility
```html
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
    <h2 id="dialog-title">Settings</h2>
    <!-- Trap focus inside modal -->
    <button aria-label="Close settings" onclick="closeModal()">×</button>
</div>
```

## Testing Accessibility

```bash
# Install axe-core for automated testing
npm install -g axe-cli

# Test page
axe http://localhost:5000

# Or use Lighthouse
npx lighthouse http://localhost:5000 --only-categories=accessibility
```

## Rules

- ALL interactive elements must be keyboard accessible
- ALL images must have meaningful alt text
- Focus must be visible on all focused elements
- Error messages must be associated with their inputs
- Color is never the only way to convey information
- Test with screen reader (NVDA, VoiceOver) when possible
