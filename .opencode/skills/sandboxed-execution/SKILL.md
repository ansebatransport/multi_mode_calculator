---
name: sandboxed-execution
description: Use when running untrusted code, testing in isolation, or creating safe execution environments. Trigger on phrases like "sandbox", "isolation", "Docker", "container", "safe execution", "untrusted code", "virtual environment", or when testing potentially dangerous operations.
---

# Sandboxed Execution Skill

Run code safely in isolated environments.

## Docker Sandboxing

### Basic Sandbox
```bash
# Run Python in Docker container
docker run --rm -i python:3.13-slim python3 << 'EOF'
# Untrusted code runs here
result = eval("2 + 3")
print(f"Result: {result}")
EOF

# Mount project directory (read-only)
docker run --rm -v /home/mulugeta/projects/multi_mode_calculator:/app:ro \
    python:3.13-slim python3 -c "
import sys
sys.path.insert(0, '/app')
from core.engine import MathEngine
e = MathEngine()
print(e.calculate('2 + 3'))
"
```

### Interactive Sandbox
```bash
# Start sandbox container
docker run --rm -it \
    -v /home/mulugeta/projects/multi_mode_calculator:/app \
    --name calc-sandbox \
    python:3.13-slim bash

# Inside container
cd /app
python -m pytest tests/ -x -q
```

### Restricted Sandbox
```bash
# Run with limited resources
docker run --rm \
    --memory=256m \
    --cpus=0.5 \
    --network=none \
    -v /home/mulugeta/projects/multi_mode_calculator:/app:ro \
    python:3.13-slim python3 -m pytest tests/ -x -q
```

## Python Virtual Environment

```bash
# Create isolated Python environment
python3 -m venv .venv/sandbox

# Activate
source .venv/sandbox/bin/activate

# Install only what's needed
pip install flask pytest

# Run code in isolation
python3 -c "from core.engine import MathEngine; print(MathEngine().calculate('2+3'))"

# Deactivate when done
deactivate
```

## Process Isolation

```bash
# Run with limited permissions
sudo -u nobody python3 untrusted_script.py

# Run with resource limits
ulimit -v 100000  # Limit virtual memory
ulimit -t 30      # Limit CPU time to 30 seconds
python3 untrusted_script.py

# Run in separate namespace
unshare --pid --fork python3 untrusted_script.py
```

## Filesystem Isolation

```bash
# Use tmpfs for temporary work
mount -t tmpfs -o size=100M tmpfs /tmp/sandbox

# Copy files to sandbox
cp untrusted_code.py /tmp/sandbox/

# Run in sandbox
cd /tmp/sandbox
python3 untrusted_code.py

# Cleanup
umount /tmp/sandbox
```

## Safe Evaluation Patterns

```python
# NEVER use eval() on untrusted input
result = eval(user_input)  # DANGEROUS!

# SAFE: Use ast.literal_eval for simple data
import ast
result = ast.literal_eval(user_input)  # Only literals

# SAFE: Use the project's expression parser
from core.engine import MathEngine
e = MathEngine()
result = e.calculate(user_input)  # Parsed, not executed

# SAFE: Restrict available functions
import builtins
safe_builtins = {
    'abs': abs, 'min': min, 'max': max,
    'sum': sum, 'len': len, 'range': range,
}
# Block dangerous builtins like __import__, eval, exec
```

## Docker Compose for Full Sandbox

```yaml
# docker-compose.sandbox.yml
version: '3.8'

services:
  calculator-sandbox:
    image: python:3.13-slim
    volumes:
      - .:/app:ro
    working_dir: /app
    command: python3 -m pytest tests/ -x -q
    mem_limit: 256m
    cpus: 0.5
    network_mode: none
    read_only: true
    tmpfs:
      - /tmp:size=100M
```

```bash
# Run sandboxed tests
docker-compose -f docker-compose.sandbox.yml up
```

## Security Checklist

- [ ] Never use `eval()` on untrusted input
- [ ] Use Docker for untrusted code execution
- [ ] Limit container resources (memory, CPU)
- [ ] Disable network for isolated execution
- [ ] Use read-only filesystem mounts
- [ ] Run as non-root user
- [ ] Clean up temporary files
- [ ] Log all sandbox activity

## Rules

- ALWAYS sandbox untrusted code
- NEVER grant network access to sandboxed code
- Limit resource usage (memory, CPU, time)
- Use read-only mounts when possible
- Clean up sandbox after use
- Log sandbox activity for debugging
