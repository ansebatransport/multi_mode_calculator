---
name: playbook
description: Use when creating reusable session workflows, documenting repeatable processes, or following established procedures. Trigger on phrases like "playbook", "runbook", "workflow", "procedure", "how to", "step by step", "standard process", or when documenting recurring tasks.
---

# Playbook Skill

Reusable session blueprints for common workflows.

## Playbook Storage

```
.opencode/playbooks/
  ├── new-feature.md         # Adding a new feature
  ├── bug-fix.md             # Investigating and fixing bugs
  ├── release.md             # Preparing a release
  ├── refactor.md            # Refactoring modules
  ├── api-endpoint.md        # Adding API endpoints
  ├── financial-module.md    # Working with financial calculations
  └── custom/
      └── user-specific.md
```

## Playbook Format

```markdown
# Playbook: [Name]

## Trigger
When [specific situation], follow this playbook.

## Steps

### 1. [Step Name]
**Action**: [what to do]
**Check**: [how to verify]
**Time**: [estimated time]

### 2. [Step Name]
...

## Checklist
- [ ] Step 1 completed
- [ ] Step 2 completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changes committed

## Rollback
If [failure condition]:
1. [recovery step]
2. [recovery step]

## Notes
- [additional context]
```

## Pre-Built Playbooks

### New Feature Playbook
```markdown
# Playbook: New Feature

## Trigger
Adding a new calculator mode or API endpoint.

## Steps

### 1. Research & Plan
- Review existing patterns in core/
- Check if similar functionality exists
- Plan module structure
**Check**: Have clear design before coding

### 2. Create Core Module
- Write pure Python in core/
- Follow existing naming conventions
- Add type hints to all functions
**Check**: Module works standalone

### 3. Add Tests
- Create tests/core/test_<module>.py
- Test happy path + edge cases
- Test error handling
**Check**: python -m pytest tests/ -x -q passes

### 4. Add API Endpoint
- Add route in apps/web/app.py
- Add request validation
- Add error handling
**Check**: curl test returns expected response

### 5. Update Frontend
- Add UI elements if needed
- Wire up button handlers
- Test in browser
**Check**: UI works in http://localhost:5000

### 6. Update Docs
- Update ARCHITECTURE.md
- Update TEST_GUIDE.md if new test values
- Add docstrings
**Check**: Docs reflect new feature

### 7. Commit
- Conventional commit message
- Push to feature/new-features
**Check**: git log shows clean history
```

### Bug Fix Playbook
```markdown
# Playbook: Bug Fix

## Trigger
User reports incorrect calculation or error.

## Steps

### 1. Reproduce
- Get exact input that causes bug
- Verify bug exists on current code
**Check**: Bug is reproducible

### 2. Isolate
- Find which module causes the issue
- Add print/debug statements
- Narrow to specific function
**Check**: Root cause identified

### 3. Check Tests
- Run existing tests: python -m pytest tests/ -x -q
- Check if any test covers this case
**Check**: Test gap identified

### 4. Fix
- Make minimal change to fix
- Don't refactor while fixing
- Verify fix works
**Check**: Original input now produces correct output

### 5. Add Regression Test
- Add test case for this bug
- Test edge cases too
**Check**: New test passes

### 6. Full Test Run
- Run all tests
- Check for regressions
**Check**: All 860+ tests pass

### 7. Commit
- "fix(module): description of fix"
- Include regression test
```

### Release Playbook
```markdown
# Playbook: Release

## Trigger
Preparing stable release to main branch.

## Steps

### 1. Code Freeze
- No new features after this point
- Only bug fixes allowed
**Check**: Feature freeze confirmed

### 2. Full Test Suite
- Run all tests: python -m pytest tests/ -x -v
- Fix any failures
**Check**: 100% tests passing

### 3. Security Review
- Review all API endpoints
- Check input validation
- Test error handling
**Check**: No security issues found

### 4. Performance Check
- Profile key operations
- Check memory usage
- Verify no regressions
**Check**: Performance acceptable

### 5. Documentation Update
- Update README.md
- Update CHANGELOG.md
- Verify all links work
**Check**: Docs are complete

### 6. Merge to Main
- Create PR: feature/new-features → main
- Review all changes
- Merge with squash
**Check**: Clean merge, no conflicts

### 7. Tag Release
- Create git tag
- Update version numbers
**Check**: Tag created successfully
```

## Custom Playbooks

Create your own playbooks for recurring tasks:

```bash
# Template
cat > .opencode/playbooks/custom/my-workflow.md << 'EOF'
# Playbook: My Workflow

## Trigger
[When to use this playbook]

## Steps
### 1. [Step]
[Details]

## Checklist
- [ ] Step 1 done
EOF
```

## Rules

- Save playbooks after discovering repeatable processes
- Update playbooks when processes change
- Reference playbooks at session start
- Keep playbooks concise and actionable
- Include time estimates for planning
