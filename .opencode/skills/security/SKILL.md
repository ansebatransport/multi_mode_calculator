---
name: security
description: Use when reviewing code for vulnerabilities, handling user input, implementing authentication, or when security concerns arise. Trigger on phrases like "security review", "check for vulnerabilities", "XSS", "injection", "sanitization", "CSRF", "authenticate", "authorize", or when modifying input handling in apps/web/.
---

# Security Skill

Protect the calculator web app from common vulnerabilities.

## Threat Model

This is a calculator web app. Primary risks:
1. **XSS (Cross-Site Scripting)** — user input rendered as HTML/JS
2. **Injection** — malicious expressions sent to the math engine
3. **DoS (Denial of Service)** — extremely complex expressions exhausting resources
4. **Information Leakage** — error messages exposing internal paths/stack traces

## Input Validation Checklist

### Expression Input (Calculator)
- [ ] Validate expression characters before processing
- [ ] Reject expressions with HTML tags: `<script>`, `<img onerror=...>`
- [ ] Limit expression length (e.g., 1000 characters max)
- [ ] Sanitize before logging
- [ ] Never `eval()` user input directly — use the parser

### API Input (Flask Routes)
- [ ] Validate Content-Type headers
- [ ] Check required fields exist in request body
- [ ] Validate numeric ranges (prevent overflow)
- [ ] Return proper HTTP status codes (400 for bad input, not 500)
- [ ] Never expose stack traces in production

## Common Vulnerabilities

### XSS Prevention
```python
# BAD — renders user input as HTML
return f"<div>{user_input}</div>"

# GOOD — Flask auto-escapes in templates
# Use |e filter or ensure autoescaping is on
return render_template('index.html', data=user_input)
```

```javascript
// BAD — innerHTML with user data
element.innerHTML = userInput;

// GOOD — textContent
element.textContent = userInput;
```

### Expression Injection
```python
# BAD — direct eval
result = eval(user_expression)

# GOOD — use the project's parser
from core.engine import MathEngine
engine = MathEngine()
result = engine.calculate(user_expression)
```

### DoS Prevention
```python
# Limit expression complexity
MAX_EXPRESSION_LENGTH = 1000
MAX_NESTING_DEPTH = 50

if len(expression) > MAX_EXPRESSION_LENGTH:
    return jsonify({"error": "Expression too long"}), 400
```

## Flask Security Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Error Handling

```python
# Never expose internals in production
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Log detailed errors server-side, return generic to client
app.logger.error(f"Calculation error: {error}", exc_info=True)
```

## Rules

- NEVER store or log user expressions with PII
- ALWAYS validate input on both client and server
- NEVER trust client-side validation alone
- Use HTTPS in production (never HTTP)
- Keep dependencies updated for security patches
