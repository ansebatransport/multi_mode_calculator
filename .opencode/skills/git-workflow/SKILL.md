---
name: git-workflow
description: Use when committing, branching, creating PRs, reviewing code, or managing git history. Trigger on phrases like "commit this", "create PR", "review changes", "merge", "rebase", "changelog", "release", "git", or when git operations are needed.
---

# Git/PR Workflow Skill

Consistent git practices for the multi_mode_calculator project.

## Repository Info

- **Remote**: `git@github.com:ansebatransport/multi_mode_calculator.git`
- **Main branch**: `main` (stable release)
- **Dev branch**: `feature/new-features` (active development)
- **Auth**: SSH key at `/home/mulugeta/.ssh/id_ed25519`

## Branch Strategy

```
main                    ← stable releases only
  └── feature/new-features  ← active development
       ├── feature/<name>   ← specific features (branch off this)
       └── fix/<name>       ← bug fixes
```

- Always work on `feature/new-features` or a sub-branch
- Merge to `main` only for stable releases
- Delete merged branches to keep repo clean

## Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]
```

Types:
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation only
- `test` — adding/fixing tests
- `refactor` — code restructuring (no behavior change)
- `style` — formatting, whitespace (no logic change)
- `chore` — build, CI, tooling
- `perf` — performance improvement

Examples:
```
feat(financial): add depreciation calculator with 3 methods
fix(expression): handle pi constant in parser
test(financial): add bond pricing test cases
docs: update ARCHITECTURE.md with new API endpoints
```

## Common Operations

```bash
# Switch to dev branch
git checkout feature/new-features

# Create feature sub-branch
git checkout -b feature/my-feature

# Stage and commit
git add -A && git commit -m "feat(mode): add new feature"

# Push current branch
git push -u origin feature/new-features

# Push and set upstream
git push --set-upstream origin feature/my-feature

# View recent commits
git log --oneline -10

# View changes before committing
git diff --staged

# Amend last commit (before push)
git commit --amend -m "better message"

# Stash work in progress
git stash
git stash pop
```

## PR Workflow

1. Push feature branch
2. Create PR from `feature/new-features` → `main` (or sub-branch)
3. Write PR description with:
   - What changed
   - Why it changed
   - How to test it
4. Review diff carefully before merging
5. Squash merge for clean history

## Rules

- NEVER force-push to `main`
- NEVER commit secrets, API keys, or tokens
- Always pull before pushing to shared branches
- Write meaningful commit messages — no "fix stuff" or "updates"
- Keep commits atomic — one logical change per commit
