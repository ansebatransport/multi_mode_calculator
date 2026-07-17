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

## Notes

- Running in WSL2, no sudo access
- Desktop Flet mode requires libgtk-3.so.0 (not available in WSL2)
- Web mode on port 5000 is the primary working mode
- User prefers to focus on web app first
