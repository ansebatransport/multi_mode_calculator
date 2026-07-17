---
name: cicd
description: Use when setting up CI/CD pipelines, GitHub Actions, automated testing, deployment, or build automation. Trigger on phrases like "CI", "CD", "pipeline", "GitHub Actions", "deploy", "build", "automation", "workflow", "release", or when creating .github/workflows/ files.
---

# CI/CD Skill

Automate testing, building, and deployment with GitHub Actions.

## Project CI/CD Setup

### Basic Test Pipeline

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, feature/new-features]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          pip install -e .

      - name: Run tests
        run: python -m pytest tests/ -x -q --tb=short

      - name: Run linter
        run: |
          pip install flake8
          flake8 core/ apps/ --max-line-length=100 --ignore=E501,W503
```

### Deploy Pipeline (Flask)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: pip install flask

      - name: Run tests before deploy
        run: python -m pytest tests/ -x -q

      - name: Deploy
        run: echo "Add deployment step here"
```

## Workflow Patterns

### Conditional Steps
```yaml
- name: Run linter
  if: github.event_name == 'pull_request'
  run: flake8 core/

- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

### Caching
```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Artifact Upload
```yaml
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results/
```

### Matrix Testing
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - os: windows-latest
        python-version: "3.11"
```

## Branch Protection Rules

Configure in GitHub repo settings:
- Require PR reviews before merging
- Require status checks to pass
- Require branches to be up to date
- Require signed commits (optional)

## Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

## Local CI (Pre-commit)

```bash
# Install pre-commit
pip install pre-commit --break-system-packages

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
EOF

# Install hooks
pre-commit install
```

## Rules

- Tests MUST pass before merge
- Never force-push to `main`
- Use meaningful workflow names
- Cache dependencies for faster builds
- Run security scanning on dependencies
- Keep workflow files in `.github/workflows/`
