---
name: file-manager
description: Use when organizing, renaming, moving, deleting, or bulk-operating on files. Trigger on phrases like "rename files", "move files", "organize", "bulk rename", "find and replace filenames", "cleanup", "sort files", "file management", "batch", or when managing multiple files at once.
---

# File Manager Skill

Bulk file operations, organization, and cleanup.

## File Discovery

```bash
# List files by type
ls -la *.py
ls -la **/*.js  # Recursive (with globstar)

# Find files by pattern
find . -name "*.py" -type f
find . -name "*.py" -not -path "./.venv/*"

# Find by size
find . -size +1M -type f
find . -size -1k -type f

# Find by date
find . -name "*.py" -mtime -7       # Modified in last 7 days
find . -name "*.py" -mtime +30      # Modified more than 30 days ago

# Find empty files
find . -empty -type f

# Find duplicate names
find . -type f -printf '%f\n' | sort | uniq -d

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

## Bulk Rename

```bash
# Rename extension
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# Add prefix
for f in *.py; do mv "$f" "prefix_$f"; done

# Remove prefix
for f in prefix_*.py; do mv "$f" "${f#prefix_}"; done

# Lowercase all filenames
for f in *; do mv "$f" "$(echo $f | tr '[:upper:]' '[:lower:]')"; done

# Replace spaces with underscores
for f in *\ *; do mv "$f" "${f// /_}"; done

# Sequential numbering
n=1; for f in *.jpg; do mv "$f" "photo_$(printf '%03d' $n).jpg"; n=$((n+1)); done
```

## Bulk Move

```bash
# Move by extension
mkdir -p images documents code
mv *.jpg *.png *.gif images/
mv *.pdf *.doc documents/
mv *.py *.js code/

# Move by date
find . -name "*.log" -mtime +30 -exec mv {} /archive/ \;

# Move to organized structure
for f in *.py; do
    dir=$(head -1 "$f" | grep -oP '(?<=# Module: )\w+' || echo "misc")
    mkdir -p "$dir"
    mv "$f" "$dir/"
done
```

## Bulk Delete

```bash
# Delete by extension
rm -f *.pyc
rm -f __pycache__/*.pyc

# Delete old files
find . -name "*.log" -mtime +30 -delete
find . -name "*.tmp" -delete

# Delete empty directories
find . -type d -empty -delete

# Delete with confirmation
find . -name "*.bak" -exec rm -i {} \;

# Dry run (show what would be deleted)
find . -name "*.pyc" -print
```

## File Organization Templates

### Project Cleanup
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Remove test cache
rm -rf .pytest_cache
rm -rf .coverage htmlcov

# Remove build artifacts
rm -rf dist build *.egg-info

# Remove IDE files
rm -rf .vscode .idea *.swp *.swo
```

### Organize by Type
```bash
#!/bin/bash
# organize.sh — Sort files into folders by extension

for file in *; do
    [ -f "$file" ] || continue
    ext="${file##*.}"
    case "$ext" in
        py)     dir="python" ;;
        js|ts)  dir="javascript" ;;
        c|h)    dir="c" ;;
        cpp|hpp) dir="cpp" ;;
        rs)     dir="rust" ;;
        cs)     dir="csharp" ;;
        jpg|png|gif) dir="images" ;;
        pdf)    dir="documents" ;;
        *)      dir="other" ;;
    esac
    mkdir -p "$dir"
    mv "$file" "$dir/"
done
```

### Backup Script
```bash
#!/bin/bash
# backup_project.sh

PROJECT_DIR="/home/mulugeta/projects/multi_mode_calculator"
BACKUP_DIR="/home/mulugeta/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="calculator_$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.venv' \
    --exclude='node_modules' \
    -C "$(dirname $PROJECT_DIR)" \
    "$(basename $PROJECT_DIR)"

echo "Backup created: $BACKUP_DIR/$BACKUP_NAME"

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/calculator_*.tar.gz | tail -n +11 | xargs rm -f
```

## File Analysis

```bash
# Lines of code by language
find . -name "*.py" -exec wc -l {} + | tail -1
find . -name "*.js" -exec wc -l {} + | tail -1
find . -name "*.html" -exec wc -l {} + | tail -1
find . -name "*.css" -exec wc -l {} + | tail -1

# Total project size
du -sh .
du -sh */ | sort -rh

# Largest files
find . -type f -exec du -h {} + | sort -rh | head -20

# File count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

## Rules

- ALWAYS dry-run bulk operations first (use `echo` or `-print`)
- NEVER delete without checking what will be removed
- Use `mv -i` for interactive moves (prompts before overwrite)
- Test bulk rename scripts on a copy first
- Keep backup before major file operations
- Use `find` with `-maxdepth` to limit search scope
