---
name: scheduled-routines
description: Use when setting up recurring tasks, cron jobs, or automated schedules. Trigger on phrases like "schedule", "cron", "recurring", "daily", "weekly", "automated", "nightly", "periodic", "timer", or when setting up automatic runs.
---

# Scheduled Routines Skill

Recurring automated tasks (nightly tests, daily health checks, etc.).

## Routine Types

| Type | Frequency | Use For |
|------|-----------|---------|
| Health Check | Every 5 min | Server uptime monitoring |
| Test Suite | Nightly | Full test run, report failures |
| Dependency Audit | Weekly | Check for security patches |
| Backup | Daily | Project backup |
| Lint | On commit | Code quality |
| Performance | Weekly | Benchmark tracking |
| Documentation | On release | Auto-update docs |

## Cron Setup

```bash
# Edit crontab
crontab -e

# View current crontab
crontab -l
```

## Common Routines

### Health Check (Every 5 minutes)
```bash
# Check server is running
*/5 * * * * curl -sf http://localhost:5000/api/health > /dev/null || \
    (cd /home/mulugeta/projects/multi_mode_calculator && python3 apps/web/run.py &)
```

### Nightly Test Suite
```bash
# Run full test suite at 2 AM
0 2 * * * cd /home/mulugeta/projects/multi_mode_calculator && \
    python -m pytest tests/ -x -q --tb=short > /tmp/test_results_$(date +\%Y\%m\%d).log 2>&1
```

### Weekly Dependency Audit
```bash
# Check for outdated packages every Monday
0 9 * * 1 cd /home/mulugeta/projects/multi_mode_calculator && \
    pip list --outdated > /tmp/outdated_packages.log 2>&1
```

### Daily Backup
```bash
# Backup project daily at midnight
0 0 * * * cd /home/mulugeta/projects && \
    tar -czf /home/mulugeta/backups/calculator_$(date +\%Y\%m\%d).tar.gz \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    multi_mode_calculator/
```

### Weekly Performance Benchmark
```bash
# Run performance benchmark every Sunday
0 10 * * 0 cd /home/mulugeta/projects/multi_mode_calculator && \
    python -c "
import time
from core.engine import MathEngine
e = MathEngine()
start = time.time()
for _ in range(10000):
    e.calculate('sin(pi/4) + cos(pi/4)')
duration = time.time() - start
print(f'$(date +\%Y-\%m-\%d): 10k calculations in {duration:.3f}s') >> /tmp/perf_benchmark.log
"
```

## Routine Manager

```bash
#!/bin/bash
# routine-manager.sh

CRON_FILE="/tmp/calculator_crontab"
LOG_DIR="/home/mulugeta/projects/multi_mode_calculator/.opencode/logs"

mkdir -p "$LOG_DIR"

add_routine() {
    local name=$1
    local schedule=$2
    local command=$3

    echo "# $name" >> "$CRON_FILE"
    echo "$schedule $command >> $LOG_DIR/${name}.log 2>&1" >> "$CRON_FILE"
    echo "" >> "$CRON_FILE"

    crontab "$CRON_FILE"
    echo "Added routine: $name ($schedule)"
}

list_routines() {
    echo "Active routines:"
    crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | while read line; do
        echo "  $line"
    done
}

remove_routine() {
    local name=$1
    sed -i "/# $name/,/^$/d" "$CRON_FILE"
    crontab "$CRON_FILE"
    echo "Removed routine: $name"
}

case "$1" in
    add)    add_routine "$2" "$3" "$4" ;;
    list)   list_routines ;;
    remove) remove_routine "$2" ;;
    *)      echo "Usage: $0 {add|list|remove}" ;;
esac
```

## Monitoring Routine Output

```bash
# Check routine logs
tail -20 /home/mulugeta/projects/multi_mode_calculator/.opencode/logs/*.log

# Check for failures
grep -l "ERROR\|FAILED\|Traceback" /home/mulugeta/projects/multi_mode_calculator/.opencode/logs/*.log

# Get last test results
cat /tmp/test_results_$(date +%Y%m%d).log

# Get performance trend
cat /tmp/perf_benchmark.log
```

## Systemd Timer (Alternative to Cron)

```ini
# ~/.config/systemd/user/calculator-health.service
[Unit]
Description=Calculator Health Check

[Service]
Type=oneshot
ExecStart=/usr/bin/curl -sf http://localhost:5000/api/health
```

```ini
# ~/.config/systemd/user/calculator-health.timer
[Unit]
Description=Run health check every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=default.target
```

```bash
# Enable timer
systemctl --user enable calculator-health.timer
systemctl --user start calculator-health.timer
```

## Rules

- Log all routine output to files
- Set up failure notifications (email/Slack)
- Keep routine scripts simple and idempotent
- Test routines before enabling
- Monitor routine health periodically
- Use absolute paths in cron jobs
- Escape % in cron dates
