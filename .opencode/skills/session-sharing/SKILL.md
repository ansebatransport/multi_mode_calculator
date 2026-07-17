---
name: session-sharing
description: Use when sharing workspace links, exporting session history, or collaborating with others. Trigger on phrases like "share session", "export session", "session link", "collaborate", "share workspace", "session history", or when distributing work to others.
---

# Session Sharing Skill

Share workspace sessions and collaborate with others.

## Session Export Format

### JSON Export
```json
{
  "session": {
    "id": "session_20240115_143022",
    "start": "2024-01-15T14:30:22Z",
    "end": "2024-01-15T16:45:30Z",
    "branch": "feature/new-features",
    "commit": "abc123"
  },
  "context": {
    "project": "multi_mode_calculator",
    "objective": "Add depreciation calculator",
    "files_changed": [
      "core/financial.py",
      "tests/core/test_financial.py"
    ]
  },
  "events": [
    {
      "timestamp": "2024-01-15T14:30:22Z",
      "type": "action",
      "tool": "read",
      "input": "core/financial.py"
    }
  ],
  "learnings": [
    "Depreciation uses straight-line method"
  ],
  "decisions": [
    {
      "decision": "Use 3 depreciation methods",
      "reason": "Industry standard"
    }
  ]
}
```

## Export Session

```python
import json
from datetime import datetime

class SessionExporter:
    def __init__(self, session_dir=".opencode"):
        self.session_dir = session_dir

    def export(self, session_id: str) -> dict:
        """Export session data."""
        session = {
            "session": self.get_session_info(session_id),
            "context": self.get_context(),
            "events": self.get_events(session_id),
            "learnings": self.get_learnings(),
            "decisions": self.get_decisions(session_id)
        }
        return session

    def save(self, session_id: str, output_file: str):
        """Save session to file."""
        session = self.export(session_id)
        with open(output_file, 'w') as f:
            json.dump(session, f, indent=2)
        print(f"Session exported to {output_file}")

    def get_session_info(self, session_id: str) -> dict:
        """Get session metadata."""
        return {
            "id": session_id,
            "start": "2024-01-15T14:30:22Z",
            "end": datetime.now().isoformat(),
            "branch": self.get_git_branch(),
            "commit": self.get_git_commit()
        }

    def get_context(self) -> dict:
        """Get session context."""
        return {
            "project": "multi_mode_calculator",
            "objective": "Current task objective"
        }

    def get_events(self, session_id: str) -> list:
        """Get session events."""
        events_file = f"{self.session_dir}/events/{session_id}.jsonl"
        if os.path.exists(events_file):
            with open(events_file) as f:
                return [json.loads(line) for line in f]
        return []

    def get_learnings(self) -> list:
        """Get learnings from session."""
        learnings_file = f"{self.session_dir}/learnings.md"
        if os.path.exists(learnings_file):
            with open(learnings_file) as f:
                return [line.strip() for line in f if line.strip().startswith("-")]
        return []

    def get_decisions(self, session_id: str) -> list:
        """Get decisions made in session."""
        return []
```

## Share Session

### Generate Shareable Link
```bash
# Create session archive
SESSION_ID="session_20240115_143022"
tar -czf "/tmp/${SESSION_ID}.tar.gz" \
    ".opencode/events/${SESSION_ID}.jsonl" \
    ".opencode/learnings.md"

# Upload to shared storage (if available)
# scp /tmp/${SESSION_ID}.tar.gz user@server:/shared/sessions/
```

### Create Session Summary
```bash
# Generate markdown summary
python3 -c "
import json

# Load session data
with open('.opencode/events/session_20240115.jsonl') as f:
    events = [json.loads(line) for line in f]

# Create summary
print('# Session Summary')
print('')
print('## Objective')
print('Add depreciation calculator to financial module')
print('')
print('## Activities')
for e in events[:10]:
    print(f'- {e[\"type\"]}: {e[\"tool\"]} ({e[\"status\"]})')
print('')
print('## Files Changed')
print('- core/financial.py')
print('- tests/core/test_financial.py')
print('')
print('## Learnings')
print('- Depreciation uses straight-line method')
print('- Added 3 depreciation methods')
"
```

## Import Session

```python
class SessionImporter:
    def __init__(self, session_dir=".opencode"):
        self.session_dir = session_dir

    def import_session(self, archive_file: str):
        """Import session from archive."""
        import tarfile

        with tarfile.open(archive_file, 'r:gz') as tar:
            tar.extractall(self.session_dir)

        print(f"Session imported to {self.session_dir}")

    def apply_learnings(self, session_file: str):
        """Apply learnings from shared session."""
        with open(session_file) as f:
            session = json.load(f)

        # Add learnings to current session
        learnings_file = f"{self.session_dir}/learnings.md"
        with open(learnings_file, 'a') as f:
            for learning in session.get('learnings', []):
                f.write(f"\n- [IMPORTED] {learning}")

        print(f"Applied {len(session.get('learnings', []))} learnings")
```

## Collaboration Workflow

### Share for Review
```bash
# Export session
python3 session_exporter.py export session_20240115_143022

# Create pull request with session context
gh pr create --title "Add depreciation calculator" \
    --body "## Session Summary
- Objective: Add depreciation calculator
- Files changed: core/financial.py, tests/core/test_financial.py
- Learnings: [list]

Session archive: session_20240115_143022.tar.gz"
```

### Share for Continuation
```bash
# Export current session
python3 session_exporter.py export current

# Other agent imports and continues
python3 session_importer.py import session_20240115_143022.tar.gz
python3 session_importer.py apply-learnings session_20240115_143022.json
```

## Session URL Format

```
opencode://session/{session_id}
opencode://session/{session_id}/events
opencode://session/{session_id}/learnings
opencode://session/{session_id}/files
```

## Rules

- Export sessions before major changes
- Include learnings in exports
- Version control session archives
- Clean up old sessions (> 30 days)
- Never export sensitive data (tokens, passwords)
- Document session objectives clearly
