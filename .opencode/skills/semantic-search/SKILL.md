---
name: semantic-search
description: Use when searching for code by meaning, finding related code, or understanding codebase relationships. Trigger on phrases like "find similar", "related code", "code like this", "semantic search", "codebase understanding", "find patterns", "what's related", or when grep/glob aren't enough.
---

# Semantic Search Skill

Understand code by meaning, not just text patterns.

## Search Strategies

### 1. Text Search (Current — grep/glob)
```bash
# Exact pattern match
grep -rn "def calculate" core/
find . -name "*.py" | xargs grep "class"

# Limitations:
# - Only finds exact text matches
# - No understanding of code meaning
# - No relationship discovery
```

### 2. Structural Search (AST-based)
```bash
# Find all function definitions
python3 -c "
import ast, sys
for root, dirs, files in os.walk('core'):
    for f in files:
        if f.endswith('.py'):
            tree = ast.parse(open(os.path.join(root, f)).read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    print(f'{root}/{f}:{node.lineno}: def {node.name}')
"

# Find all class definitions
python3 -c "
import ast, os
for root, dirs, files in os.walk('core'):
    for f in files:
        if f.endswith('.py'):
            tree = ast.parse(open(os.path.join(root, f)).read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    print(f'{root}/{f}:{node.lineno}: class {node.name}')
"
```

### 3. Dependency Search (Import Graph)
```bash
# Find what a module imports
grep -n "^from\|^import" core/engine.py

# Find what imports a module
grep -rn "from core.engine import\|import core.engine" core/ apps/

# Build dependency graph
python3 -c "
import ast, os
for root, dirs, files in os.walk('core'):
    for f in files:
        if f.endswith('.py'):
            tree = ast.parse(open(os.path.join(root, f)).read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith('core'):
                        print(f'{f} imports {node.module}')
"
```

### 4. Call Graph Search
```bash
# Find all callers of a function
grep -rn "engine\.calculate" core/ apps/
grep -rn "mortgage_payment" core/ apps/

# Find what a function calls
python3 -c "
import ast
tree = ast.parse(open('core/engine.py').read())
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            print(f'Line {node.lineno}: calls {node.func.id}')
"
```

### 5. Pattern Search (Similar Code)
```bash
# Find similar function signatures
grep -rn "def.*float.*float.*float" core/

# Find similar patterns
grep -rn "try:" core/ | head -20
grep -rn "except.*Error" core/

# Find similar class structures
grep -rn "class.*:" core/ | head -20
```

## Codebase Understanding Maps

### Module Responsibility Map
```python
# Auto-generate from docstrings
python3 -c "
import ast, os
for root, dirs, files in os.walk('core'):
    for f in files:
        if f.endswith('.py') and f != '__init__.py':
            tree = ast.parse(open(os.path.join(root, f)).read())
            docstring = ast.get_docstring(tree)
            if docstring:
                print(f'{f}: {docstring[:100]}')
"
```

### Function Signature Index
```python
# Index all function signatures
python3 -c "
import ast, os, json
index = {}
for root, dirs, files in os.walk('core'):
    for f in files:
        if f.endswith('.py'):
            tree = ast.parse(open(os.path.join(root, f)).read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [a.arg for a in node.args.args]
                    index[f'{f}:{node.name}'] = args
print(json.dumps(index, indent=2))
"
```

### Test Coverage Map
```python
# Map tests to modules
python3 -c "
import os
modules = [f.replace('.py','') for f in os.listdir('core') if f.endswith('.py')]
tests = [f.replace('test_','').replace('.py','') for f in os.listdir('tests/core') if f.endswith('.py')]
for m in sorted(modules):
    status = '✅' if m in tests else '❌'
    print(f'{status} {m}')
"
```

## Search Commands

```bash
# Find code that does something similar
grep -rn "result = " core/ | grep -i "sum\|total\|add"

# Find error handling patterns
grep -rn "try:" core/ -A 2

# Find configuration patterns
grep -rn "os.getenv\|os.environ" core/

# Find test patterns
grep -rn "def test_" tests/ | head -20

# Find all decorators
grep -rn "@\|lru_cache\|property" core/
```

## Limitations & Workarounds

| Need | Current Limitation | Workaround |
|------|-------------------|------------|
| Meaning-based search | grep only matches text | Use AST analysis |
| Code similarity | No vector embeddings | Use pattern matching |
| Whole-project context | Manual exploration | Use repository-map skill |
| Relationship discovery | Manual grep chains | Build dependency graph |

## Rules

- Start with grep for quick searches
- Use AST analysis for structural queries
- Build maps for frequently accessed information
- Keep maps updated when code changes
- Use multiple search strategies for complex queries
