---
name: dependency-management
description: Use when updating packages, checking for vulnerabilities, resolving version conflicts, or managing requirements. Trigger on phrases like "update dependencies", "pip install", "vulnerability", "outdated", "requirements", "version conflict", "security patch", "upgrade", or when modifying pyproject.toml or requirements files.
---

# Dependency Management Skill

Keep dependencies updated, secure, and compatible.

## Current Dependencies

```
# pyproject.toml (runtime)
flask>=3.0.0
flet>=0.25.0

# Dev/test
pytest>=8.0.0
pylsp (installed separately)
```

## Commands

```bash
# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Show specific package info
pip show flask

# Check dependency tree
pip install pipdeptree --break-system-packages
pipdeptree

# Install from requirements
pip install -r requirements.txt

# Freeze current environment
pip freeze > requirements.txt
```

## Security Scanning

```bash
# Install safety
pip install safety --break-system-packages

# Check for known vulnerabilities
safety check

# Check specific package
safety check flask
```

## Updating Dependencies

### Safe Updates (patch versions)
```bash
# Update within current major version
pip install --upgrade flask
pip install --upgrade pytest
```

### Major Version Updates
```bash
# Check changelog before upgrading
# Test thoroughly after upgrading
pip install flask>=4.0.0
python -m pytest tests/ -x -q
```

## Version Pinning Strategy

```toml
# pyproject.toml

[project]
dependencies = [
    "flask>=3.0.0,<4.0.0",  # Pinned to major version
    "flet>=0.25.0,<1.0.0",  # Pinned to major version
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0,<9.0.0",
    "flake8>=7.0.0,<8.0.0",
]
```

## Virtual Environment Management

```bash
# Create venv (if allowed)
python -m venv .venv

# Activate
source .venv/bin/activate

# Deactivate
deactivate

# Export requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## Dependency Audit Checklist

When reviewing dependency changes:
- [ ] Check for known CVEs (security vulnerabilities)
- [ ] Review changelog for breaking changes
- [ ] Check license compatibility
- [ ] Verify package is actively maintained
- [ ] Test all affected functionality after update
- [ ] Check transitive dependencies

## Adding New Dependencies

```bash
# Research first
pip search <package>  # or search PyPI web

# Check alternatives
pip show <package>  # See dependencies

# Install and test
pip install <package> --break-system-packages
python -m pytest tests/ -x -q

# Add to pyproject.toml
# Update requirements.txt
```

## Common Issues

### Version Conflict
```bash
# Error: flask 3.0 requires Werkzeug>=3.0, but you have 2.0

# Fix: Update both
pip install --upgrade flask werkzeug
```

### Import Error After Update
```bash
# Error: cannot import name 'X' from 'Y'

# Check what changed
pip show <package>
# Review changelog for removed APIs
# Update code to use new API
```

### Dependency Hell
```bash
# Package A requires X>=2.0
# Package B requires X<2.0

# Solutions:
# 1. Find compatible versions
# 2. Fork and fix
# 3. Use dependency groups
# 4. Contact maintainers
```

## Rules

- NEVER commit `requirements.txt` with exact pinned versions for apps (use ranges)
- ALWAYS test after updating dependencies
- Check security advisories before updating
- Keep minimal dependencies — each one is a maintenance burden
- Document why each dependency is needed
- Review transitive dependencies periodically
