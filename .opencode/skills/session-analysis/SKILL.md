---
name: session-analysis
description: Use after completing tasks or sessions to analyze what worked, what failed, and extract patterns for improvement. Trigger on phrases like "analyze session", "what worked", "what failed", "retrospective", "review session", "lessons learned", "improve", or when reflecting on completed work.
---

# Session Analysis Skill

Diagnose session outcomes and extract improvement patterns.

## Analysis Framework

### Session Log Format

```markdown
# Session Log: [date]

## Objective
[What we set out to do]

## Activities
1. [Activity 1] — [result]
2. [Activity 2] — [result]
3. [Activity 3] — [result]

## Outcomes
- **Completed**: [list]
- **Partial**: [list]
- **Failed**: [list]

## Time Analysis
- Total time: [X hours]
- Most time spent: [area]
- Bottlenecks: [what slowed us down]

## Patterns Discovered
- [pattern 1]
- [pattern 2]

## Improvements for Next Time
- [improvement 1]
- [improvement 2]
```

## Success Metrics

| Metric | How to Measure |
|--------|---------------|
| Task Completion | % of objectives completed |
| First-try Success | % of changes that worked first time |
| Regression Rate | % of changes that broke something |
| Time to Fix | How long bug fixes took |
| Learning Rate | New patterns discovered |

## Analysis Checklist

### After Each Task
- [ ] Did it work on first try?
- [ ] What errors occurred?
- [ ] What was the root cause?
- [ ] How long did it take?
- [ ] What pattern was discovered?

### After Each Session
- [ ] All planned objectives completed?
- [ ] Any unexpected issues?
- [ ] What took longer than expected?
- [ ] What could be automated?
- [ ] What should be saved as a learning?

## Pattern Categories

### Code Patterns
- Common mistakes → Add to anti-pattern list
- Working solutions → Add to playbook
- Recurring issues → Add to validation

### Process Patterns
- Task ordering → What sequence works best
- Parallel opportunities → What can be split
- Blockers → What stops progress

### User Patterns
- Preferences → What user likes
- Communication → How to present results
- Feedback → What user corrects

## Improvement Loop

```
Do → Measure → Analyze → Improve → Do
  ↑                                    ↓
  └────────────────────────────────────┘
```

### Step 1: Do
- Execute the task
- Track what happens

### Step 2: Measure
- Time taken
- Errors encountered
- Changes needed

### Step 3: Analyze
- Root causes
- Patterns
- Opportunities

### Step 4: Improve
- Update playbooks
- Add to learnings
- Modify workflows

## Automated Analysis

```bash
# Git commit analysis
echo "=== Session Summary ==="
echo "Commits this session:"
git log --oneline --since="2 hours ago"

echo ""
echo "Files changed:"
git diff --stat HEAD~5..HEAD

echo ""
echo "Lines added/removed:"
git diff --shortstat HEAD~5..HEAD

echo ""
echo "Test results:"
python -m pytest tests/ -x -q 2>&1 | tail -3
```

## Learning Extraction

### From Bugs
```markdown
## Bug Pattern: [name]
- **Symptom**: [what happened]
- **Root cause**: [why]
- **Fix**: [what worked]
- **Prevention**: [how to avoid]
```

### From Success
```markdown
## Success Pattern: [name]
- **Context**: [when to use]
- **Approach**: [what worked]
- **Why it worked**: [reasoning]
- **Reuse**: [where else to apply]
```

### From Failures
```markdown
## Failure Pattern: [name]
- **What was tried**: [approach]
- **Why it failed**: [reason]
- **Alternative**: [what to do instead]
```

## Session Report Template

```markdown
# Session Report

**Date**: [date]
**Duration**: [time]
**Branch**: [branch]

## Objectives
1. [ ] [objective 1]
2. [ ] [objective 2]
3. [ ] [objective 3]

## Results
| Objective | Status | Notes |
|-----------|--------|-------|
| [obj 1] | ✅ Done | [details] |
| [obj 2] | ⚠️ Partial | [details] |
| [obj 3] | ❌ Blocked | [reason] |

## Discoveries
- [discovery 1]
- [discovery 2]

## Changes Made
- [file]: [change]
- [file]: [change]

## Lessons Learned
1. [lesson]
2. [lesson]

## Action Items for Next Session
- [ ] [action 1]
- [ ] [action 2]
```

## Rules

- Analyze after EVERY session, not just successful ones
- Be honest about failures — they teach the most
- Extract actionable patterns, not vague observations
- Save analysis to `.opencode/session-logs/`
- Review past analyses at session start
- Track metrics over time to measure improvement
