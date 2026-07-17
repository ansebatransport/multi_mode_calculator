---
name: database
description: Use when managing databases, running SQL queries, designing schemas, or migrating data. Trigger on phrases like "database", "SQL", "SQLite", "PostgreSQL", "query", "schema", "migration", "table", "INSERT", "SELECT", "UPDATE", "DELETE", "index", or when working with .db, .sqlite files.
---

# Database Skill

Manage databases with SQL for the calculator project.

## SQLite (Default — No Setup Needed)

```bash
# Create/open database
sqlite3 calculator.db

# Commands (inside sqlite3)
.tables                    # List all tables
.schema                    # Show table definitions
.headers on                # Show column headers
.mode column               # Pretty output
.mode json                 # JSON output

# Run SQL file
sqlite3 calculator.db < schema.sql

# One-shot query
sqlite3 calculator.db "SELECT * FROM history;"

# Export to CSV
sqlite3 calculator.db -csv -header "SELECT * FROM history;" > export.csv

# Export to JSON
sqlite3 calculator.db -json "SELECT * FROM history;" | python3 -m json.tool
```

## Schema Design

### Calculator Schema

```sql
-- schema.sql

-- User settings
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Calculation history
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT NOT NULL,
    result TEXT NOT NULL,
    mode TEXT NOT NULL DEFAULT 'standard',
    angle_mode TEXT DEFAULT 'radians',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saved calculations (favorites)
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    expression TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User-defined functions (future)
CREATE TABLE IF NOT EXISTS user_functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    expression TEXT NOT NULL,
    parameters TEXT,  -- JSON array of parameter names
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial presets
CREATE TABLE IF NOT EXISTS financial_presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,  -- 'mortgage', 'car_loan', etc.
    name TEXT NOT NULL,
    parameters TEXT NOT NULL,  -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_history_created ON history(created_at);
CREATE INDEX IF NOT EXISTS idx_history_mode ON history(mode);
CREATE INDEX IF NOT EXISTS idx_favorites_name ON favorites(name);
```

### Migration Pattern

```sql
-- migrations/001_initial.sql
-- Run: sqlite3 calculator.db < migrations/001_initial.sql

-- Version tracking
CREATE TABLE IF NOT EXISTS migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Check if migration applied
-- SELECT * FROM migrations WHERE version = 1;
```

## CRUD Operations

### Insert

```sql
-- Single row
INSERT INTO history (expression, result, mode)
VALUES ('2 + 3', '5', 'standard');

-- Multiple rows
INSERT INTO history (expression, result, mode) VALUES
    ('sin(pi/4)', '0.7071067811865475', 'scientific'),
    ('FF + 1', '256', 'programmer'),
    ('100 * 0.05', '5', 'financial');

-- Insert and get ID
INSERT INTO favorites (name, expression) VALUES ('Quick calc', '2^10');
SELECT last_insert_rowid();
```

### Select

```sql
-- All rows
SELECT * FROM history;

-- With filtering
SELECT * FROM history WHERE mode = 'financial';

-- With ordering
SELECT * FROM history ORDER BY created_at DESC LIMIT 10;

-- Count
SELECT COUNT(*) FROM history;

-- Aggregate
SELECT mode, COUNT(*) as count FROM history GROUP BY mode;

-- Search
SELECT * FROM history WHERE expression LIKE '%sin%';

-- JSON export
SELECT json_group_array(
    json_object(
        'id', id,
        'expression', expression,
        'result', result
    )
)
FROM history;
```

### Update

```sql
-- Single row
UPDATE settings SET value = 'degrees' WHERE key = 'angle_mode';

-- Multiple rows
UPDATE history SET mode = 'standard' WHERE mode = '';
```

### Delete

```sql
-- Single row
DELETE FROM history WHERE id = 123;

-- Multiple rows
DELETE FROM history WHERE created_at < date('now', '-30 days');

-- All rows
DELETE FROM history;

-- Vacuum to reclaim space
VACUUM;
```

## Python Integration

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('calculator.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())

def save_calculation(expression: str, result: str, mode: str = 'standard'):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO history (expression, result, mode) VALUES (?, ?, ?)",
            (expression, result, mode)
        )
        conn.commit()

def get_history(limit: int = 50) -> list:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
```

## Performance Tips

```sql
-- Add index for frequent queries
CREATE INDEX idx_history_mode ON history(mode);
CREATE INDEX idx_history_created ON history(created_at);

-- Analyze query plan
EXPLAIN QUERY PLAN
SELECT * FROM history WHERE mode = 'financial';

-- Check database integrity
PRAGMA integrity_check;

-- Database size
PRAGMA page_count;
PRAGMA page_size;
```

## Backup & Restore

```bash
# Backup
sqlite3 calculator.db ".backup backup.db"

# Or copy
cp calculator.db backup_$(date +%Y%m%d).db

# Restore
sqlite3 calculator.db ".restore backup.db"
```

## Rules

- ALWAYS use parameterized queries (never string concatenation)
- Use transactions for multi-step operations
- Add indexes for frequently queried columns
- Back up database before migrations
- Use `INTEGER PRIMARY KEY` for auto-increment IDs
- Store JSON as TEXT, parse in application layer
