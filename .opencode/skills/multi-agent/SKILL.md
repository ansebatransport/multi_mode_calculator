---
name: multi-agent
description: Use when delegating complex tasks to subagents, coordinating parallel work, or managing multiple workers. Trigger on phrases like "delegate", "parallel task", "subagent", "split work", "coordinate", "worker", "team", or when a task can be divided into independent parts.
---

# Multi-Agent Skill

Coordinate multiple agents for parallel execution and complex tasks.

## Agent Types

| Agent | Mode | Use For |
|-------|------|---------|
| build | primary | Code editing, debugging, implementation |
| plan | subagent | Architecture, design decisions, research |
| general | subagent | Complex analysis, multi-step tasks |
| explore | subagent | Codebase search, file discovery |

## Spawning Subagents

```python
# Use the task tool to spawn agents
# Each agent gets isolated context

# Example: parallel code review
task(
    description="Review security",
    prompt="Review apps/web/app.py for XSS, injection, and input validation issues. Return a list of findings.",
    subagent_type="explore"
)

task(
    description="Review performance",
    prompt="Review core/engine.py and core/financial.py for performance issues. Return bottlenecks.",
    subagent_type="explore"
)

task(
    description="Review test coverage",
    prompt="Compare core/ modules against tests/ to find missing test coverage. Return gaps.",
    subagent_type="explore"
)
```

## Parallel Work Patterns

### Parallel Code Review
```bash
# Spawn multiple reviewers simultaneously
# Each reviews different aspect
# Results collected in parallel

Aspect 1: Security review → Agent A
Aspect 2: Performance review → Agent B
Aspect 3: Style review → Agent C
→ Merge all findings into comprehensive review
```

### Parallel Testing
```bash
# Test multiple modules simultaneously
Module 1: test_engine.py → Agent A
Module 2: test_financial.py → Agent B
Module 3: test_expression_parser.py → Agent C
→ Aggregate results
```

### Parallel Documentation
```bash
# Update multiple docs simultaneously
Doc 1: README.md → Agent A
Doc 2: ARCHITECTURE.md → Agent B
Doc 3: API docs → Agent C
→ Merge into consistent documentation
```

## Task Delegation Pattern

```markdown
When a task is too large for one agent:

1. **Decompose**: Break into independent subtasks
2. **Assign**: Each subtask to a specialized agent
3. **Monitor**: Track progress of each agent
4. **Merge**: Combine results into final output
5. **Verify**: Validate merged result
```

## Context Isolation

Each subagent gets:
- Fresh context (no shared state)
- Specific prompt and task
- Access to relevant tools
- Return summary only (not full output)

Benefits:
- No context pollution
- Parallel execution
- Fault isolation (one failure doesn't affect others)
- Specialized prompting per task

## Coordination Patterns

### Fan-Out/Fan-In
```
        ┌→ Agent A (task 1) ─┐
Task ───┼→ Agent B (task 2) ─┼→ Merge Results
        └→ Agent C (task 3) ─┘
```

### Pipeline
```
Agent A (research) → Agent B (implement) → Agent C (test)
```

### Leader/Worker
```
Leader Agent (plan) ─┬→ Worker 1 (execute)
                     ├→ Worker 2 (execute)
                     └→ Worker 3 (execute)
```

## Rules

- Decompose before delegating — clear subtask boundaries
- Each agent should have a single responsibility
- Merge results carefully — check for conflicts
- Verify merged output before presenting to user
- Use appropriate agent type for each task
- Don't over-parallelize — some tasks need sequential execution
