---
name: architect-mode
description: Use when planning complex implementations, designing architecture, or when a task needs separation of reasoning from implementation. Trigger on phrases like "architect mode", "plan first", "design before code", "think through", "approach", "strategy", "how should I implement", or when facing a complex multi-file change.
---

# Architect Mode Skill

Separate planning from implementation. Think first, code second.

## Two-Phase Workflow

```
Phase 1: ARCHITECT (reasoning)
  → Understand requirements
  → Analyze codebase
  → Design approach
  → Create plan
  → Review plan

Phase 2: IMPLEMENT (execution)
  → Follow the plan step by step
  → Verify each step
  → Run tests after each change
  → Final verification
```

## Phase 1: Architecture

### Step 1: Understand Requirements
```markdown
## Requirements Analysis
- **Goal**: [what needs to be done]
- **Input**: [what we start with]
- **Output**: [what we need to produce]
- **Constraints**: [limitations, patterns to follow]
- **Edge cases**: [what could go wrong]
```

### Step 2: Codebase Analysis
```bash
# Find relevant files
grep -rn "pattern" core/ apps/
find . -name "*.py" | xargs grep "class.*:"

# Check dependencies
grep -rn "from core.module import" core/
grep -rn "import core.module" core/

# Check tests
ls tests/core/test_*.py
```

### Step 3: Design Options
```markdown
## Option A: [name]
**Approach**: [description]
**Pros**: [benefits]
**Cons**: [drawbacks]
**Files affected**: [list]
**Estimated complexity**: Low/Medium/High

## Option B: [name]
**Approach**: [description]
**Pros**: [benefits]
**Cons**: [drawbacks]
**Files affected**: [list]
**Estimated complexity**: Low/Medium/High

## Recommendation
Option [X] because [reasoning].
```

### Step 4: Implementation Plan
```markdown
## Implementation Plan

### Step 1: [task]
**File**: [specific file]
**Changes**: [exact changes]
**Risk**: Low/Medium/High
**Time**: [estimate]
**Verify**: [how to verify]

### Step 2: [task]
...

### Step N: Final Verification
**Command**: `python -m pytest tests/ -x -q`
**Expected**: All tests pass
```

## Phase 2: Implementation

### Execution Rules
1. Follow the plan exactly
2. Complete each step before moving to next
3. Verify after each step
4. If a step fails, STOP and reassess
5. Don't skip verification steps

### Step Execution Template
```markdown
## Executing Step [N]: [task]

### Changes Made
- [file1]: [what changed]
- [file2]: [what changed]

### Verification
- [ ] [check 1]
- [ ] [check 2]
- [x] Step complete

### Issues Encountered
- [any issues or "None"]

### Next Step
Proceed to Step [N+1]
```

## Decision Records

```markdown
# ADR-001: [Title]

## Status
Accepted

## Context
[What is the issue?]

## Decision
[What was decided?]

## Consequences
### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [drawback 1]
- [drawback 2]

### Risks
- [risk 1]
```

## When to Use Architect Mode

| Situation | Use Architect? |
|-----------|---------------|
| Simple bug fix | No — fix directly |
| Adding a button | No — follow existing pattern |
| New calculator mode | Yes — plan structure |
| Major refactor | Yes — plan carefully |
| API redesign | Yes — design first |
| New core module | Yes — plan architecture |
| Test additions | Maybe — if complex |
| Documentation | No — write directly |

## Rules

- ALWAYS complete Phase 1 before Phase 2
- NEVER skip the design step for complex tasks
- Write the plan as markdown before coding
- Review the plan before implementing
- If implementation deviates from plan, STOP and update plan
- Keep decision records for significant architectural choices
