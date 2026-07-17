---
name: agent-teams
description: Use when coordinating multiple agent sessions, peer-to-peer messaging between agents, or managing distributed work. Trigger on phrases like "agent team", "coordinate agents", "peer messaging", "distributed work", "parallel agents", "multi-session", or when managing complex multi-agent workflows.
---

# Agent Teams Skill

Coordinate multiple agent sessions with peer-to-peer messaging.

## Team Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Leader     │────▶│  Worker A   │     │  Worker B   │
│  (Primary)  │────▶│  (Research) │     │  (Implement)│
│             │◀────│             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                        │
       └────────────────────────────────────────┘
                    Shared Context
```

## Communication Patterns

### 1. Leader-Worker
```
Leader assigns tasks → Workers execute → Workers report back
```

### 2. Peer-to-Peer
```
Agent A ←→ Agent B (direct communication)
Agent A ←→ Agent C (direct communication)
```

### 3. Pub/Sub
```
Agent A publishes message → All subscribers receive
```

## Message Format

```json
{
  "id": "msg_123",
  "from": "agent-a",
  "to": "agent-b",
  "type": "task|result|question|update",
  "subject": "Implement financial module",
  "body": "Add depreciation calculator with 3 methods",
  "priority": "high|medium|low",
  "timestamp": "2024-01-15T14:30:00Z",
  "metadata": {}
}
```

## Team Coordination

### Spawning Team Members
```python
# Leader spawns workers
worker_a = task(
    description="Research depreciation methods",
    prompt="Research straight-line, declining balance, and sum-of-years-digits depreciation. Return formulas and examples.",
    subagent_type="general"
)

worker_b = task(
    description="Implement depreciation calculator",
    prompt="Implement depreciation calculator in core/financial.py with 3 methods. Use the formulas provided.",
    subagent_type="general"
)
```

### Task Distribution
```python
# Distribute work across team
tasks = [
    {"agent": "worker-a", "task": "Research API design"},
    {"agent": "worker-b", "task": "Write unit tests"},
    {"agent": "worker-c", "task": "Update documentation"},
]

# Each worker picks up tasks independently
# Results are collected at the end
```

### Result Aggregation
```python
# Collect results from workers
results = []
for worker in workers:
    result = worker.get_result()
    results.append(result)

# Merge results
merged = merge_results(results)
```

## Shared Context

### Through Files
```bash
# Workers communicate via shared files
echo "Research complete" > .opencode/team/research-status.txt
echo '{"methods": [...]}' > .opencode/team/research-results.json

# Other workers read status
cat .opencode/team/research-status.txt
```

### Through Event Stream
```python
# Log team events
log_event("team", "worker-a", "task_complete", "Research done")
log_event("team", "worker-b", "task_start", "Starting implementation")
```

## Team Roles

| Role | Responsibility | Skills |
|------|---------------|--------|
| Leader | Plan, assign, coordinate | architect-mode, multi-agent |
| Researcher | Gather information | explore, semantic-search |
| Implementer | Write code | testing, debugging |
| Reviewer | Check quality | code-review, security |
| Tester | Validate changes | testing, browser-testing |
| Documenter | Update docs | documentation |

## Coordination Patterns

### Sequential Pipeline
```
Research → Implement → Test → Review → Deploy
   A          B          C       D        E
```

### Parallel Execution
```
    ┌→ Research ─┐
Plan├→ Implement ─┼→ Merge
    └→ Test    ─┘
```

### Fan-Out/Fan-In
```
        ┌→ Worker 1 ─┐
Task ───┼→ Worker 2 ─┼→ Aggregate
        └→ Worker 3 ─┘
```

## Conflict Resolution

```python
# When workers produce conflicting changes
def resolve_conflicts(changes):
    """Resolve merge conflicts between workers."""
    # 1. Identify conflicts
    conflicts = find_conflicts(changes)

    # 2. Apply priority rules
    for conflict in conflicts:
        if conflict.priority == "high":
            apply_change(conflict.high_priority)
        else:
            # Ask leader for decision
            ask_leader(conflict)

    # 3. Merge non-conflicting changes
    merge(changes)
```

## Rules

- Clear task boundaries before spawning workers
- Use shared files for inter-agent communication
- Log all team events for debugging
- Aggregate results carefully before presenting
- Resolve conflicts by priority or ask user
- Don't over-parallelize — some tasks need sequence
