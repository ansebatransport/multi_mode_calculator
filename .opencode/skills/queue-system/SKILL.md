---
name: queue-system
description: Use when queuing follow-up messages, managing task queues, or handling concurrent requests. Trigger on phrases like "queue", "queue up", "batch", "concurrent", "pending", "backlog", "task queue", or when managing multiple pending operations.
---

# Queue System Skill

Queue follow-up messages and manage concurrent tasks.

## Queue Types

| Type | Use For | Priority |
|------|---------|----------|
| Message Queue | User follow-up messages | FIFO |
| Task Queue | Background processing | Priority-based |
| Event Queue | Event handling | Chronological |
| Edit Queue | File edits | Dependent |

## Message Queue

### Store Pending Messages
```python
# .opencode/queue/messages.json
{
  "queue": [
    {
      "id": "msg_001",
      "content": "After that, also add unit tests",
      "timestamp": "2024-01-15T14:30:00Z",
      "status": "pending"
    },
    {
      "id": "msg_002",
      "content": "Then update the documentation",
      "timestamp": "2024-01-15T14:31:00Z",
      "status": "pending"
    }
  ]
}
```

### Process Queue
```python
import json
from pathlib import Path

class MessageQueue:
    def __init__(self, queue_file=".opencode/queue/messages.json"):
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(exist_ok=True)
        self.load()

    def load(self):
        if self.queue_file.exists():
            with open(self.queue_file) as f:
                self.data = json.load(f)
        else:
            self.data = {"queue": []}

    def save(self):
        with open(self.queue_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add(self, message: str):
        """Add message to queue."""
        msg = {
            "id": f"msg_{len(self.data['queue']) + 1:03d}",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        self.data["queue"].append(msg)
        self.save()
        return msg["id"]

    def next(self) -> dict:
        """Get next pending message."""
        for msg in self.data["queue"]:
            if msg["status"] == "pending":
                return msg
        return None

    def complete(self, msg_id: str):
        """Mark message as completed."""
        for msg in self.data["queue"]:
            if msg["id"] == msg_id:
                msg["status"] = "completed"
                break
        self.save()

    def list_pending(self) -> list:
        """List all pending messages."""
        return [m for m in self.data["queue"] if m["status"] == "pending"]
```

## Task Queue

### Priority-Based Task Queue
```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: int
    created: str = field(compare=False)
    task_id: str = field(compare=False)
    description: str = field(compare=False)
    status: str = field(compare=False, default="pending")

class TaskQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0

    def add(self, description: str, priority: int = 5):
        """Add task with priority (lower = higher priority)."""
        self.counter += 1
        task = Task(
            priority=priority,
            created=datetime.now().isoformat(),
            task_id=f"task_{self.counter:03d}",
            description=description
        )
        heapq.heappush(self.queue, task)
        return task.task_id

    def next(self) -> Task:
        """Get highest priority task."""
        if self.queue:
            return heapq.heappop(self.queue)
        return None

    def complete(self, task_id: str):
        """Mark task as completed."""
        # Remove from queue (simplified)
        pass
```

### Usage
```python
queue = TaskQueue()

# Add tasks
queue.add("Fix bug in financial module", priority=1)
queue.add("Add new feature", priority=5)
queue.add("Update documentation", priority=3)

# Process in priority order
while True:
    task = queue.next()
    if not task:
        break
    print(f"Processing: {task.description}")
    # Execute task...
    queue.complete(task.task_id)
```

## Edit Queue

### Batch File Edits
```python
class EditQueue:
    def __init__(self):
        self.edits = []

    def queue_edit(self, file_path: str, old_text: str, new_text: str):
        """Queue a file edit."""
        self.edits.append({
            "file": file_path,
            "old": old_text,
            "new": new_text,
            "applied": False
        })

    def apply_all(self):
        """Apply all queued edits."""
        for edit in self.edits:
            if not edit["applied"]:
                # Read file
                with open(edit["file"], 'r') as f:
                    content = f.read()

                # Apply edit
                new_content = content.replace(edit["old"], edit["new"], 1)

                # Write file
                with open(edit["file"], 'w') as f:
                    f.write(new_content)

                edit["applied"] = True
                print(f"Applied edit to {edit['file']}")

    def rollback(self):
        """Rollback all applied edits."""
        for edit in reversed(self.edits):
            if edit["applied"]:
                # Read file
                with open(edit["file"], 'r') as f:
                    content = f.read()

                # Reverse edit
                new_content = content.replace(edit["new"], edit["old"], 1)

                # Write file
                with open(edit["file"], 'w') as f:
                    f.write(new_content)

                edit["applied"] = False
                print(f"Rolled back edit to {edit['file']}")
```

## Queue Management Commands

```bash
# View pending messages
cat .opencode/queue/messages.json | python3 -m json.tool

# View pending tasks
cat .opencode/queue/tasks.json | python3 -m json.tool

# Clear completed items
python3 -c "
import json
with open('.opencode/queue/messages.json') as f:
    data = json.load(f)
data['queue'] = [m for m in data['queue'] if m['status'] != 'completed']
with open('.opencode/queue/messages.json', 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Rules

- Process queue items in order (FIFO for messages, priority for tasks)
- Mark items as completed after processing
- Keep queue files small (< 100 items)
- Clean up completed items periodically
- Log queue operations for debugging
