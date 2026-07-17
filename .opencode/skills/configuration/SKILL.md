---
name: configuration
description: Use when managing settings, environment variables, feature flags, or configuration files. Trigger on phrases like "config", "settings", "environment", "env vars", "feature flag", ".env", "configuration", "setup", or when managing application settings across environments.
---

# Configuration Skill

Manage application settings cleanly across environments.

## Configuration Hierarchy

```
1. Hardcoded defaults (in code)
2. Config files (opencode.json, config.py)
3. Environment variables (.env)
4. Command-line arguments
5. Runtime overrides
```

Later sources override earlier ones.

## Project Config Files

| File | Purpose | Version controlled? |
|------|---------|-------------------|
| `opencode.json` | opencode agent config | Yes |
| `pyproject.toml` | Python project metadata | Yes |
| `.env.example` | Template for env vars | Yes |
| `.env` | Actual secrets | NO (gitignored) |
| `apps/web/run.py` | Server startup config | Yes |

## Environment Variables Pattern

```python
import os

# config.py
class Config:
    """Application configuration from environment."""

    # Server
    HOST = os.getenv("CALC_HOST", "0.0.0.0")
    PORT = int(os.getenv("CALC_PORT", "5000"))
    DEBUG = os.getenv("CALC_DEBUG", "false").lower() == "true"

    # Security
    SECRET_KEY = os.getenv("CALC_SECRET_KEY", "dev-secret-key-change-in-prod")
    ALLOWED_ORIGINS = os.getenv("CALC_ALLOWED_ORIGINS", "http://localhost:5000").split(",")

    # Features
    ENABLE_GRAPHING = os.getenv("CALC_ENABLE_GRAPHING", "true").lower() == "true"
    ENABLE_FINANCIAL = os.getenv("CALC_ENABLE_FINANCIAL", "true").lower() == "true"

    # Limits
    MAX_EXPRESSION_LENGTH = int(os.getenv("CALC_MAX_EXPR_LEN", "1000"))
    MAX_HISTORY_SIZE = int(os.getenv("CALC_MAX_HISTORY", "100"))
```

## .env File Template

```bash
# .env.example (version controlled)
CALC_HOST=0.0.0.0
CALC_PORT=5000
CALC_DEBUG=false
CALC_SECRET_KEY=change-me-in-production
CALC_ALLOWED_ORIGINS=http://localhost:5000
CALC_ENABLE_GRAPHING=true
CALC_ENABLE_FINANCIAL=true
CALC_MAX_EXPR_LEN=1000
CALC_MAX_HISTORY=100
```

## Feature Flags

```python
class FeatureFlags:
    """Runtime feature toggles."""

    _flags = {
        "dark_mode": True,
        "graph_mode": True,
        "financial_mode": True,
        "unit_converter": True,
        "export_import": True,
        "auto_save": False,  # Future feature
        "user_accounts": False,  # Future feature
    }

    @classmethod
    def is_enabled(cls, flag: str) -> bool:
        return cls._flags.get(flag, False)

    @classmethod
    def enable(cls, flag: str):
        cls._flags[flag] = True

    @classmethod
    def disable(cls, flag: str):
        cls._flags[flag] = False
```

## Flask Config

```python
# apps/web/app.py
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Or from file
app.config.from_pyfile('config.py')

# Or from env var
app.config.from_envvar('CALC_CONFIG_FILE')
```

## Settings Validation

```python
from dataclasses import dataclass

@dataclass
class ServerConfig:
    host: str
    port: int
    debug: bool

    def __post_init__(self):
        if not 1 <= self.port <= 65535:
            raise ValueError(f"Invalid port: {self.port}")
        if self.host not in ("0.0.0.0", "127.0.0.1", "localhost"):
            raise ValueError(f"Invalid host: {self.host}")

def load_config() -> ServerConfig:
    return ServerConfig(
        host=os.getenv("CALC_HOST", "0.0.0.0"),
        port=int(os.getenv("CALC_PORT", "5000")),
        debug=os.getenv("CALC_DEBUG", "false").lower() == "true",
    )
```

## Rules

- NEVER commit `.env` files with secrets
- ALWAYS provide `.env.example` with defaults
- Use type conversion for non-string values
- Validate config on startup, not at runtime
- Document all config options in `.env.example`
- Use environment-specific overrides (dev/staging/prod)
