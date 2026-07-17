---
name: performance
description: Use when optimizing code, profiling execution time, reducing memory usage, or when performance issues are reported. Trigger on phrases like "slow", "optimize", "performance", "profiling", "memory", "bottleneck", "latency", "fast", or when processing large datasets or complex calculations.
---

# Performance Skill

Identify and resolve performance bottlenecks in the calculator.

## Profiling Commands

```bash
# Quick timing
cd /home/mulugeta/projects/multi_mode_calculator
python -c "
import time
from core.engine import MathEngine
e = MathEngine()
start = time.time()
for _ in range(10000):
    e.calculate('sin(pi/4) + cos(pi/4)')
print(f'{time.time()-start:.3f}s for 10k calculations')
"

# Python profiler
python -m cProfile -s cumulative your_script.py

# Line-by-line profiling
pip install line_profiler --break-system-packages
kernprof -l -v your_script.py

# Memory profiling
pip install memory_profiler --break-system-packages
python -m memory_profiler your_script.py
```

## Known Hotspots

| Module | Risk | Mitigation |
|--------|------|-----------|
| `graph_engine.py` | Plotting 1000+ points | Batch rendering, downsample |
| `matrices.py` | Large matrix operations | NumPy if available, limit size |
| `statistics.py` | Large datasets | Streaming algorithms |
| `expression_parser.py` | Deep nesting | Limit depth, optimize tokenizer |
| `distributions.py` | PDF/CDF calculations | Cache common values |

## Optimization Patterns

### Cache expensive computations
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> float:
    ...
```

### Batch API responses
```python
# BAD — N+1 queries
for point in points:
    result = calculate(point)

# GOOD — batch
results = [calculate(p) for p in points]
```

### Lazy evaluation
```python
# BAD — computes everything upfront
def get_all_results(data):
    return [expensive(x) for x in data]

# GOOD — generator for large datasets
def get_all_results(data):
    return (expensive(x) for x in data)
```

### Limit recursion
```python
MAX_DEPTH = 100

def recursive_calc(value, depth=0):
    if depth > MAX_DEPTH:
        raise RecursionError("Maximum depth exceeded")
    ...
```

## Flask API Performance

- Add caching headers for static responses
- Use `json.dumps(separators=(',', ':'))` for compact JSON
- Limit response size for graph data (downsample if > 10k points)
- Profile endpoints with `flask-debugtoolbar` in development

## Benchmarking

```python
import timeit

# Compare two approaches
old_time = timeit.timeit('old_function()', globals=globals(), number=1000)
new_time = timeit.timeit('new_function()', globals=globals(), number=1000)
print(f"Speedup: {old_time/new_time:.1f}x")
```

## Rules

- ALWAYS measure before optimizing — don't guess
- NEVER sacrifice correctness for speed
- Profile real workloads, not synthetic benchmarks
- Document performance characteristics in docstrings
- Set reasonable limits (max matrix size, max expression length, max graph points)
