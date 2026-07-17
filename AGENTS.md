# Development Workflow

## GitHub

- **Repo**: https://github.com/ansebatransport/multi_mode_calculator
- **Remote URL**: `git@github.com:ansebatransport/multi_mode_calculator.git`
- **Auth**: SSH key at `/home/mulugeta/.ssh/id_ed25519`
- **Username**: ansebatransport

## Branches

- `main` — stable release branch
- `feature/new-features` — active development branch

## Common Commands

```bash
# Switch to dev branch
git checkout feature/new-features

# Run tests
cd /home/mulugeta/projects/multi_mode_calculator && python -m pytest tests/ -x -q

# Run tests with coverage
python -m pytest tests/ --tb=short -q --co -q 2>/dev/null | tail -1

# Start web server
cd /home/mulugeta/projects/multi_mode_calculator && python3 apps/web/run.py &

# Server URL
# http://localhost:5000

# Commit and push
git add -A && git commit -m "description" && git push
```

## Project Structure

- `core/` — pure Python math modules (no UI, no Flask)
- `apps/web/` — Flask web app (HTML/CSS/JS)
- `apps/desktop/` — Flet desktop (skeleton, needs libgtk)
- `apps/mobile/` — Flet mobile (skeleton)
- `tests/` — 860 tests (37 unit + 4 integration)

## Available Skills (39)

All skills are in `~/.config/opencode/skills/` (global) and `.opencode/skills/` (project).
Skills are inherited by ALL agents in ALL projects automatically.

### Core Development
| Skill | Purpose |
|-------|---------|
| vision | Analyze screenshots, UI designs |
| testing | Run tests, fix failures, write tests |
| git-workflow | Commits, PRs, branches |
| security | XSS, injection, sanitization |
| type-safety | Type hints, mypy/pylsp |
| docs | README, ARCHITECTURE, docstrings |
| performance | Profiling, caching, benchmarks |
| sdks | Python/JS/CLI client libraries |

### Autonomous Agent
| Skill | Purpose |
|-------|---------|
| error-recovery | Retry, fallback, circuit breaker |
| refactoring | Code smells, DRY, SOLID |
| debugging | Root cause analysis, breakpoints |
| code-review | PR review, style checks |
| cicd | GitHub Actions, pipelines |
| configuration | Env vars, feature flags |
| accessibility | WCAG, ARIA, keyboard nav |
| dependency-management | Updates, security patches |

### Compiled Languages
| Skill | Purpose |
|-------|---------|
| c-lang | gcc, Makefile, memory, valgrind |
| cpp | CMake, RAII, templates, STL |
| rust | Cargo, ownership, traits, clippy |
| csharp | .NET, LINQ, async, DI, xUnit |

### Automation
| Skill | Purpose |
|-------|---------|
| http-client | curl, API testing, batch scripts |
| database | SQLite, schemas, migrations, SQL |
| file-manager | Bulk rename, organize, cleanup |
| process-monitor | Background processes, auto-restart |

## Available Tools

| Tool | Purpose |
|------|---------|
| bash | Shell commands, git, docker, curl |
| edit | Edit files with string replacements |
| write | Create/overwrite files |
| read | Read files and directories |
| glob | Find files by pattern |
| grep | Search file contents |
| webfetch | Fetch web content |
| websearch | Search the web |
| task | Launch subagents |
| todowrite | Task tracking |
| question | Ask user questions |
| skill | Load specialized skills |

## How to Use Skills

Skills auto-trigger on keyword matches. To manually load:
```
/skill testing
/skill http-client
/skill database
```

## Environment Notes

- Running in WSL2, no sudo access
- Desktop Flet mode requires libgtk-3.so.0 (not available in WSL2)
- Web mode on port 5000 is the primary working mode
- User prefers to focus on web app first
- All skills and tools are inherited by all agents in this project
