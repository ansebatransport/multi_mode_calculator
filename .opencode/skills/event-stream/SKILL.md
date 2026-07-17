---
name: event-stream
description: Use when tracking agent actions, logging events, or building audit trails. Trigger on phrases like "event log", "action trail", "audit", "track actions", "what happened", "event history", "action log", or when monitoring agent behavior.
---

# Event Stream Skill

Chronological tracking of all agent actions and observations.

## Event Format

```json
{
  "timestamp": "2024-01-15T14:30:22Z",
  "type": "action|observation|error|decision",
  "agent": "build|plan|general|explore",
  "tool": "bash|edit|write|read|glob|grep",
  "input": "command or file path",
  "output": "result summary",
  "status": "success|failure|pending",
  "metadata": {}
}
```

## Event Storage

```
.opencode/events/
  ├── 2024-01-15.jsonl        # Daily event log
  ├── 2024-01-16.jsonl
  └── sessions/
      ├── session_001.json    # Session summary
      └── session_002.json
```

## Event Types

| Type | Description | Example |
|------|-------------|---------|
| action | Agent performed an action | File edited, command run |
| observation | Agent observed something | File read, search result |
| error | Something went wrong | Test failed, syntax error |
| decision | Agent made a choice | Selected approach, picked option |
| milestone | Task completed | Feature done, bug fixed |
| session | Session lifecycle | Start, pause, end |

## Logging Events

### Manual Logging
```bash
# Log an event
log_event() {
    local type=$1
    local tool=$2
    local input=$3
    local output=$4
    local status=$5

    echo "{\"timestamp\":\"$(date -Iseconds)\",\"type\":\"$type\",\"tool\":\"$tool\",\"input\":\"$input\",\"output\":\"$output\",\"status\":\"$status\"}" \
        >> ".opencode/events/$(date +%Y-%m-%d).jsonl"
}

# Usage
log_event "action" "edit" "core/engine.py" "Fixed pi constant" "success"
log_event "observation" "test" "pytest tests/" "860 passed" "success"
log_event "error" "bash" "python -m pytest" "1 failed" "failure"
```

### Automatic Logging (Hook)
```bash
# .opencode/hooks/log-events.sh
#!/bin/bash
# Hook into tool execution

TOOL=$1
INPUT=$2
OUTPUT=$3

if [[ "$OUTPUT" == *"error"* ]] || [[ "$OUTPUT" == *"Error"* ]]; then
    STATUS="failure"
else
    STATUS="success"
fi

log_event "action" "$TOOL" "$INPUT" "$OUTPUT" "$STATUS"
```

## Querying Events

```bash
# Last N events
tail -20 .opencode/events/$(date +%Y-%m-%d).jsonl

# Events by type
grep '"type":"error"' .opencode/events/*.jsonl

# Events by tool
grep '"tool":"edit"' .opencode/events/*.jsonl

# Events by status
grep '"status":"failure"' .opencode/events/*.jsonl

# Events in time range
python3 -c "
import json
from datetime import datetime, timedelta

start = datetime.now() - timedelta(hours=2)
with open('.opencode/events/$(date +%Y-%m-%d).jsonl') as f:
    for line in f:
        event = json.loads(line)
        ts = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
        if ts >= start:
            print(f\"{event['type']}: {event['tool']} - {event['status']}\")
"
```

## Session Summary

```bash
# Generate session summary
python3 -c "
import json
from collections import Counter

events = []
with open('.opencode/events/$(date +%Y-%m-%d).jsonl') as f:
    for line in f:
        events.append(json.loads(line))

# Count by type
types = Counter(e['type'] for e in events)
tools = Counter(e['tool'] for e in events)
statuses = Counter(e['status'] for e in events)

print('Session Summary:')
print(f'  Total events: {len(events)}')
print(f'  Types: {dict(types)}')
print(f'  Tools used: {dict(tools)}')
print(f'  Success rate: {statuses[\"success\"]/len(events)*100:.1f}%')
"
```

## Audit Trail

```bash
# Complete audit trail for a file
grep '"input":"core/engine.py"' .opencode/events/*.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    print(f\"{e['timestamp']}: {e['type']} via {e['tool']} - {e['status']}\")
"

# Audit trail for a session
cat .opencode/events/sessions/session_001.json | python3 -m json.tool
```

## Real-time Monitoring

```bash
# Watch events in real-time
tail -f .opencode/events/$(date +%Y-%m-%d).jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    icon = '✓' if e['status'] == 'success' else '✗'
    print(f\"{icon} {e['type']}: {e['tool']} ({e['status']})\")
"
```

## Rules

- Log every tool execution
- Include timestamps in ISO format
- Keep event logs for 30 days
- Summarize events at session end
- Never log sensitive data (passwords, tokens)
- Use JSONL format for easy parsing
