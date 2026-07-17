---
name: learning
description: Use after completing tasks, fixing bugs, or discovering patterns to persist learnings across sessions. Trigger on phrases like "remember this", "save learning", "note to self", "what did we learn", "pattern", "always do this", "never do this", or when a significant discovery is made during work.
---

# Learning / Memory Skill

Persist knowledge across sessions. Every session builds on the last.

## Learning File

All learnings are stored in `.opencode/learnings.md`:

```markdown
# Project Learnings

Auto-updated by the learning skill. DO NOT manually edit sections marked [AUTO].

## Patterns That Work
- [AUTO] 2024-01-15: Flask routes return JSON with jsonify(), not dict
- [AUTO] 2024-01-15: pytest.approx with rel=1e-9 for float comparisons

## Patterns to Avoid
- [AUTO] 2024-01-15: Never use eval() on user input - use expression_parser

## User Preferences
- User prefers dark theme with red operators (#e94560)
- User likes compact UI, minimal whitespace
- User wants tests run before commits

## Project-Specific Knowledge
- WSL2 has no sudo - use --break-system-packages for pip
- libatomic.so.1 missing - use pylsp instead of pyright
- Port 5000 is the primary dev server

## Bug Fixes Applied
- [AUTO] 2024-01-15: pi constant was missing from expression_parser.py line 43
```

## Learning Workflow

### After fixing a bug:
```markdown
## Pattern: [bug type]
- **Problem**: [what was wrong]
- **Root cause**: [why it happened]
- **Fix**: [what was changed]
- **Prevention**: [how to avoid in future]
```

### After discovering user preference:
```markdown
## User Preference: [category]
- **Preference**: [what user wants]
- **Context**: [when it applies]
- **Example**: [specific instance]
```

### After finding a pattern:
```markdown
## Pattern: [name]
- **Context**: [when to use]
- **Approach**: [what to do]
- **Anti-pattern**: [what NOT to do]
```

## Auto-Learning Triggers

After each activity, automatically save:
1. **Bug fix** → Add to "Bug Fixes Applied" with root cause
2. **User feedback** → Add to "User Preferences"
3. **Working pattern** → Add to "Patterns That Work"
4. **Failed approach** → Add to "Patterns to Avoid"
5. **Project constraint** → Add to "Project-Specific Knowledge"

## Session Start

At the beginning of each session:
1. Read `.opencode/learnings.md`
2. Reference relevant learnings in current task
3. Apply user preferences automatically
4. Avoid known anti-patterns

## Knowledge Management

### Deduplication
```python
def add_learning(category: str, entry: str):
    """Add learning, avoiding duplicates."""
    existing = read_learnings(category)
    if not any(levenshtein_ratio(entry, e) > 0.85 for e in existing):
        append_to_file(category, entry)
```

### Organization
- Group by category (patterns, preferences, constraints)
- Date-stamp all entries
- Mark auto-generated entries with [AUTO]
- Keep entries concise (1-2 lines)

## Rules

- ALWAYS save learnings before ending a session
- NEVER save sensitive data (passwords, tokens, keys)
- Keep entries actionable and specific
- Reference learnings in context when applying them
- Review and prune outdated learnings periodically
