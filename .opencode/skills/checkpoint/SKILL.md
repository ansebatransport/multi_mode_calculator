---
name: checkpoint
description: Use before making significant code changes, during refactoring, or before risky operations to enable rollback. Trigger on phrases like "save checkpoint", "snapshot", "undo point", "before I change", "rollback", "revert", "restore", or when about to modify multiple files.
---

# Checkpoint Skill

Create file snapshots before changes. Enable safe experimentation.

## Checkpoint Storage

```
.opencode/checkpoints/
  ├── checkpoint_20240115_143022/
  │   ├── manifest.json      # Metadata
  │   ├── src/engine.py      # Snapshot
  │   ├── src/financial.py   # Snapshot
  │   └── tests/test_engine.py
  └── checkpoint_20240115_150045/
      └── ...
```

## Create Checkpoint

```bash
# Manual checkpoint
CHECKPOINT_DIR=".opencode/checkpoints/checkpoint_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$CHECKPOINT_DIR"

# Save manifest
cat > "$CHECKPOINT_DIR/manifest.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "description": "Before refactoring financial module",
  "files": ["core/financial.py", "core/engine.py"],
  "branch": "feature/new-features",
  "commit": "$(git rev-parse HEAD)"
}
EOF

# Copy files
for file in core/financial.py core/engine.py tests/test_engine.py; do
    mkdir -p "$CHECKPOINT_DIR/$(dirname $file)"
    cp "$file" "$CHECKPOINT_DIR/$file"
done

echo "Checkpoint created: $CHECKPOINT_DIR"
```

## Restore Checkpoint

```bash
# List checkpoints
ls -lt .opencode/checkpoints/

# Restore specific checkpoint
CHECKPOINT=".opencode/checkpoints/checkpoint_20240115_143022"

# Read manifest
cat "$CHECKPOINT/manifest.json" | python3 -m json.tool

# Restore files
for file in $(cat "$CHECKPOINT/manifest.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for f in data['files']:
    print(f)
"); do
    cp "$CHECKPOINT/$file" "$file"
    echo "Restored: $file"
done
```

## Auto-Checkpoint Before Risky Operations

```bash
# Before git operations
auto_checkpoint() {
    local description=$1
    shift
    local files=("$@")

    CHECKPOINT_DIR=".opencode/checkpoints/auto_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$CHECKPOINT_DIR"

    echo "{\"timestamp\":\"$(date -Iseconds)\",\"description\":\"$description\",\"files\":[$(printf '\"%s\",' "${files[@]}" | sed 's/,$//')]}" > "$CHECKPOINT_DIR/manifest.json"

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            mkdir -p "$CHECKPOINT_DIR/$(dirname $file)"
            cp "$file" "$CHECKPOINT_DIR/$file"
        fi
    done

    echo "$CHECKPOINT_DIR"
}

# Usage
CP=$(auto_checkpoint "Before refactoring" "core/engine.py" "core/financial.py")
# ... do work ...
# If something goes wrong:
# cp $CP/core/engine.py core/engine.py
```

## Checkpoint History

```bash
# Show all checkpoints with descriptions
for dir in .opencode/checkpoints/*/; do
    if [ -f "$dir/manifest.json" ]; then
        desc=$(python3 -c "import json; print(json.load(open('$dir/manifest.json'))['description'])")
        timestamp=$(basename "$dir" | sed 's/checkpoint_//' | sed 's/_/ /' | sed 's/\(..\)\(..\)\(..\) \(..\)\(..\)\(..\)/\1-\2-\3 \4:\5:\6/')
        echo "$timestamp: $desc"
    fi
done | sort -r

# Cleanup old checkpoints (keep last 20)
ls -dt .opencode/checkpoints/*/ | tail -n +21 | xargs rm -rf
```

## Git Integration

```bash
# Create checkpoint before commit
checkpoint_before_commit() {
    local msg=$1
    CHECKPOINT_DIR=".opencode/checkpoints/pre_commit_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$CHECKPOINT_DIR"

    git diff --name-only > "$CHECKPOINT_DIR/files.txt"
    while read file; do
        if [ -f "$file" ]; then
            mkdir -p "$CHECKPOINT_DIR/$(dirname $file)"
            cp "$file" "$CHECKPOINT_DIR/$file"
        fi
    done < "$CHECKPOINT_DIR/files.txt"

    echo "{\"timestamp\":\"$(date -Iseconds)\",\"description\":\"Pre-commit: $msg\",\"files\":[$(cat "$CHECKPOINT_DIR/files.txt" | sed 's/.*/\"&\"/' | tr '\n' ',')],\"commit\":\"$(git rev-parse HEAD)\"}" > "$CHECKPOINT_DIR/manifest.json"
}

# Quick undo last commit
git reset HEAD~1
# Restore files from checkpoint
```

## Rules

- ALWAYS create checkpoint before large refactors
- ALWAYS create checkpoint before destructive git operations (reset, rebase)
- Keep checkpoints for at least 7 days
- Limit to 50 checkpoints max (auto-cleanup old ones)
- Store manifest with every checkpoint (timestamp, files, commit)
- NEVER store secrets or credentials in checkpoints
