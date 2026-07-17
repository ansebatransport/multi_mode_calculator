---
name: hook-system
description: Use when setting up automated actions triggered by events, lifecycle hooks, or pre/post processing. Trigger on phrases like "hook", "trigger", "automate", "pre-commit", "post-save", "on change", "lifecycle", "event handler", or when configuring automatic responses to events.
---

# Hook System Skill

Automate actions triggered by events and lifecycle moments.

## Hook Types

| Hook | When | Use For |
|------|------|---------|
| Pre-commit | Before git commit | Lint, format, test |
| Post-commit | After git commit | Push, notify |
| Pre-push | Before git push | Run full test suite |
| Pre-edit | Before file edit | Create checkpoint |
| Post-edit | After file edit | Run linter |
| Pre-test | Before tests | Clean cache |
| Post-test | After tests | Report results |
| Session-start | When session begins | Load learnings, check status |
| Session-end | When session ends | Save state, cleanup |

## Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running pre-commit checks..."

# Check for secrets
if git diff --cached --name-only | xargs grep -l "password\|secret\|token" 2>/dev/null; then
    echo "ERROR: Potential secrets detected!"
    exit 1
fi

# Run linter
python3 -m flake8 core/ --max-line-length=100 --ignore=E501,W503
if [ $? -ne 0 ]; then
    echo "Linting failed. Fix errors before committing."
    exit 1
fi

# Run tests
python3 -m pytest tests/ -x -q --tb=short
if [ $? -ne 0 ]; then
    echo "Tests failed. Fix before committing."
    exit 1
fi

echo "Pre-commit checks passed!"
```

```bash
# .git/hooks/pre-push
#!/bin/bash
echo "Running full test suite before push..."
python3 -m pytest tests/ -x -q
if [ $? -ne 0 ]; then
    echo "Tests failed. Fix before pushing."
    exit 1
fi
```

## Session Hooks

### Session Start
```bash
# opencode-session-start.sh
# Runs at beginning of each session

echo "=== Session Starting ==="

# Check server status
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✓ Server running on port 5000"
else
    echo "✗ Server not running"
fi

# Check git status
git status --short

# Load learnings
if [ -f .opencode/learnings.md ]; then
    echo "✓ Learnings loaded"
fi

echo "=== Session Ready ==="
```

### Session End
```bash
# opencode-session-end.sh
# Runs at end of each session

echo "=== Session Ending ==="

# Save current state
echo "Last session: $(date -Iseconds)" >> .opencode/session-log.md

# Cleanup old checkpoints (keep 20)
ls -dt .opencode/checkpoints/*/ 2>/dev/null | tail -n +21 | xargs rm -rf 2>/dev/null

# Cleanup temp files
rm -f /tmp/web_calc_*.tmp

echo "=== Session Saved ==="
```

## Automated Workflow Hooks

### Auto-Lint After Edit
```bash
# .opencode/hooks/post-edit-lint.sh
#!/bin/bash
FILE=$1

# Run linter on edited file
if [[ "$FILE" == *.py ]]; then
    python3 -m flake8 "$FILE" --max-line-length=100 --ignore=E501,W503
fi

if [[ "$FILE" == *.js ]]; then
    # eslint "$FILE" 2>/dev/null
    echo "JS linting not configured"
fi
```

### Auto-Test After Core Change
```bash
# .opencode/hooks/post-edit-test.sh
#!/bin/bash
FILE=$1

# If core module changed, run its tests
if [[ "$FILE" == core/*.py ]]; then
    MODULE=$(basename "$FILE" .py)
    TEST_FILE="tests/core/test_${MODULE}.py"

    if [ -f "$TEST_FILE" ]; then
        echo "Running tests for $MODULE..."
        python3 -m pytest "$TEST_FILE" -x -q
    fi
fi
```

### Auto-Checkpoint Before Refactor
```bash
# .opencode/hooks/pre-refactor-checkpoint.sh
#!/bin/bash
# Triggered before large refactors

echo "Creating checkpoint before refactor..."
CHECKPOINT_DIR=".opencode/checkpoints/pre_refactor_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$CHECKPOINT_DIR"

# Save affected files
git diff --name-only > "$CHECKPOINT_DIR/files.txt"
while read file; do
    if [ -f "$file" ]; then
        mkdir -p "$CHECKPOINT_DIR/$(dirname $file)"
        cp "$file" "$CHECKPOINT_DIR/$file"
    fi
done < "$CHECKPOINT_DIR/files.txt"

echo "Checkpoint: $CHECKPOINT_DIR"
```

## Webhook Integration

```bash
# Send notification on successful deploy
notify_deploy() {
    curl -X POST "https://hooks.slack.com/services/..." \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"Deploy successful: $(date)\"}"
}

# Trigger on git push to main
if [ "$BRANCH" = "main" ]; then
    notify_deploy
fi
```

## Hook Registration

```bash
# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
chmod +x .opencode/hooks/*.sh

# Install pre-commit framework (optional)
pip install pre-commit --break-system-packages
pre-commit install
```

## Rules

- Hooks should be fast (< 5 seconds for pre-commit)
- Always provide escape hatch (SKIP钩子 variable)
- Log hook actions for debugging
- Never block on non-critical failures (use warnings)
- Test hooks before relying on them
- Keep hooks simple and focused
