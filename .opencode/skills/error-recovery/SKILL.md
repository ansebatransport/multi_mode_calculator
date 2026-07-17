---
name: error-recovery
description: Use when handling errors, implementing retry logic, building fallback mechanisms, or recovering from failures. Trigger on phrases like "error handling", "retry", "fallback", "graceful degradation", "crash recovery", "resilient", "fault tolerant", or when code needs to handle unexpected states.
---

# Error Recovery Skill

Build resilient code that handles failures gracefully and self-heals.

## Error Categories

| Category | Example | Strategy |
|----------|---------|----------|
| Transient | Network timeout, API rate limit | Retry with backoff |
| Permanent | Invalid input, missing field | Return clear error |
| Critical | Out of memory, disk full | Log + alert + safe exit |
| Data | Corrupt file, bad JSON | Validate + fallback to default |

## Retry Pattern

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=0.1):
    """Execute with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return func()
        except ConnectionError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
            time.sleep(delay)
    raise RuntimeError("Max retries exceeded")
```

## Fallback Pattern

```python
def calculate_with_fallback(expression: str) -> dict:
    """Calculate with graceful fallback on errors."""
    try:
        result = engine.calculate(expression)
        return {"result": result, "success": True, "method": "primary"}
    except ZeroDivisionError:
        return {"result": None, "success": False, "error": "Division by zero"}
    except OverflowError:
        # Try with reduced precision
        try:
            result = engine.calculate(expression, precision=6)
            return {"result": result, "success": True, "method": "reduced_precision"}
        except Exception:
            return {"result": None, "success": False, "error": "Result too large"}
    except Exception as e:
        logger.error(f"Calculation failed: {e}", exc_info=True)
        return {"result": None, "success": False, "error": "Internal error"}
```

## Circuit Breaker

```python
class CircuitBreaker:
    """Prevent repeated calls to a failing service."""

    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        self.state = "closed"  # closed = normal, open = blocking

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
            else:
                raise RuntimeError("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

## Graceful Shutdown

```python
import signal
import sys

shutdown_requested = False

def handle_signal(signum, frame):
    global shutdown_requested
    shutdown_requested = True
    print("Shutdown requested, finishing current operation...")

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def process_batch(items):
    results = []
    for item in items:
        if shutdown_requested:
            print(f"Saving progress ({len(results)} items processed)")
            return results
        results.append(process(item))
    return results
```

## Flask Error Handling

```python
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {e}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({"error": "Rate limited", "retry_after": 60}), 429
```

## Rules

- NEVER silently swallow exceptions — always log them
- ALWAYS provide meaningful error messages to users
- NEVER expose internal details (stack traces, file paths) in production
- Use specific exception types, not bare `except:`
- Clean up resources in `finally` blocks
