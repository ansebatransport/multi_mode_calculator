---
name: code-review
description: Use when reviewing code changes, checking PRs, enforcing standards, or evaluating code quality. Trigger on phrases like "review", "code review", "check this PR", "review changes", "standards check", "best practices", "lint", or when examining code before committing or merging.
---

# Code Review Skill

Systematic code review for quality, security, and maintainability.

## Review Checklist

### Correctness
- [ ] Does the code do what it claims?
- [ ] Are edge cases handled (zero, null, empty, overflow)?
- [ ] Are error conditions handled gracefully?
- [ ] Are return types consistent?

### Security
- [ ] Is user input validated and sanitized?
- [ ] No hardcoded secrets or credentials?
- [ ] No SQL/OS command injection vectors?
- [ ] No XSS vulnerabilities?
- [ ] Rate limiting on expensive operations?

### Performance
- [ ] No unnecessary computations?
- [ ] Appropriate data structures used?
- [ ] No N+1 patterns?
- [ ] Memory-efficient for large inputs?

### Maintainability
- [ ] Code is readable without comments?
- [ ] Functions are single-purpose?
- [ ] No code duplication (DRY)?
- [ ] Naming is clear and consistent?

### Testing
- [ ] Tests exist for new code?
- [ ] Edge cases are tested?
- [ ] Tests are independent?
- [ ] All tests pass?

## Review Comments

### Style
```
[style] Consider using a more descriptive name here.
[style] This line exceeds 100 characters.
[style] Missing blank line between functions.
```

### Bugs
```
[bug] This will fail when `values` is empty — `min()` raises ValueError.
[bug] Race condition: `shared_state` accessed without lock.
[bug] Off-by-one: `range(len(arr))` should be `range(1, len(arr))`.
```

### Performance
```
[perf] O(n²) — consider using a set for O(1) lookups.
[perf] This regex is compiled on every call — move to module level.
```

### Security
```
[security] User input rendered directly — use escape().
[security] No length validation — potential DoS.
[security] Logging sensitive data — redact before logging.
```

### Suggestions
```
[suggestion] Extract this into a named function for readability.
[suggestion] Consider using `functools.lru_cache` here.
[suggestion] This could be simplified with a list comprehension.
```

## Self-Review Checklist

Before pushing, review your own code:

```bash
# View staged changes
git diff --staged

# View all changes
git diff

# Check for common issues
git diff --stat  # How many files changed?
```

Ask yourself:
1. Would I understand this code in 6 months?
2. Did I test the happy path AND error paths?
3. Am I introducing any new dependencies?
4. Does this break any existing API contracts?
5. Is the commit message clear?

## Review Workflow

1. **First pass** — Read the PR description, understand intent
2. **Second pass** — Line-by-line code review
3. **Third pass** — Check tests and documentation
4. **Summary** — Provide actionable feedback with priorities:
   - **Must fix** — Bugs, security issues
   - **Should fix** — Performance, maintainability
   - **Consider** — Style, suggestions
   - **Nit** — Minor preference, optional

## Rules

- Review code, not people
- Be specific — point to exact lines and explain why
- Suggest solutions, not just problems
- Distinguish between must-fix and nice-to-have
- Acknowledge good code too
