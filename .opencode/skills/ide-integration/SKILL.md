---
name: ide-integration
description: Use when integrating with IDEs, setting up watch mode, or configuring editor features. Trigger on phrases like "IDE", "VS Code", "watch mode", "editor integration", "auto-reload", "live reload", "file watcher", "next edit", or when configuring development environment.
---

# IDE Integration Skill

Seamless integration with code editors and IDEs.

## VS Code Integration

### Project Settings
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "/usr/bin/python3",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true
  },
  "search.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true
  }
}
```

### Launch Configuration
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Calculator",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/apps/web/run.py",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Run Tests",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-x", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Tasks
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "python -m pytest tests/ -x -q",
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "Start Server",
      "type": "shell",
      "command": "python3 apps/web/run.py",
      "isBackground": true,
      "problemMatcher": []
    }
  ]
}
```

## Watch Mode (Auto-Reload)

### Flask Auto-Reload
```python
# apps/web/run.py
# Flask has built-in auto-reload in debug mode
app.run(debug=True, host='0.0.0.0', port=5000)
```

### File Watcher Script
```bash
#!/bin/bash
# watch.sh — Auto-restart server on file changes

WATCH_DIR="/home/mulugeta/projects/multi_mode_calculator"
WATCH_EXT="py"

last_modified=$(find "$WATCH_DIR" -name "*.$WATCH_EXT" -printf '%T@\n' | sort -n | tail -1)

while true; do
    current_modified=$(find "$WATCH_DIR" -name "*.$WATCH_EXT" -printf '%T@\n' | sort -n | tail -1)

    if [ "$current_modified" != "$last_modified" ]; then
        echo "[$(date)] File changed, restarting server..."
        pkill -f "run.py" 2>/dev/null
        sleep 1
        cd "$WATCH_DIR" && python3 apps/web/run.py &
        last_modified=$current_modified
    fi

    sleep 2
done
```

### Using watchexec
```bash
# Install watchexec
# cargo install watchexec-cli

# Auto-run tests on file change
watchexec -e py -- python -m pytest tests/ -x -q

# Auto-restart server on file change
watchexec -r -e py -- python3 apps/web/run.py
```

## Editor Features

### Code Snippets
```json
// .vscode/snippets/python.json
{
  "Calculate": {
    "prefix": "calc",
    "body": [
      "from core.engine import MathEngine",
      "",
      "engine = MathEngine()",
      "result = engine.calculate(\"${1:expression}\")",
      "print(result)"
    ],
    "description": "Calculate expression"
  },
  "Test Function": {
    "prefix": "testf",
    "body": [
      "def test_${1:function_name}():",
      "    \"\"\"Test ${1:function_name}\"\"\"",
      "    ${2:pass}"
    ],
    "description": "Create test function"
  }
}
```

### Keybindings
```json
// .vscode/keybindings.json
[
  {
    "key": "ctrl+shift+t",
    "command": "workbench.action.terminal.sendSequence",
    "args": { "text": "python -m pytest tests/ -x -q\n" }
  },
  {
    "key": "ctrl+shift+r",
    "command": "workbench.action.terminal.sendSequence",
    "args": { "text": "python3 apps/web/run.py\n" }
  }
]
```

## Next Edit Suggestions (Cursor-like)

### Pattern Recognition
```python
# When user types:
def calculate_sqrt(x):

# Suggest completion:
def calculate_sqrt(x):
    """Calculate square root of x."""
    return engine.calculate(f"sqrt({x})")
```

### Context-Aware Suggestions
```python
# Based on nearby code, suggest:
# 1. Similar function patterns
# 2. Import statements
# 3. Error handling
# 4. Type hints
```

## Live Reload for Web

```html
<!-- Add to index.html for live reload -->
<script>
  if ('WebSocket' in window) {
    const ws = new WebSocket('ws://localhost:5000/ws');
    ws.onmessage = (event) => {
      if (event.data === 'reload') {
        location.reload();
      }
    };
    ws.onclose = () => {
      setTimeout(() => location.reload(), 1000);
    };
  }
</script>
```

## Rules

- Use debug mode for development (auto-reload)
- Configure editor to exclude cache directories
- Set up launch configurations for debugging
- Use file watchers for auto-testing
- Keep IDE settings in version control
- Use consistent formatting (black, isort)
