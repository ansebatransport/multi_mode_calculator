---
name: process-monitor
description: Use when managing background processes, monitoring services, checking ports, or restarting failed services. Trigger on phrases like "background process", "monitor", "service", "port check", "restart", "PID", "process status", "kill process", "auto-restart", "health check", or when managing the web server.
---

# Process Monitor Skill

Monitor, manage, and auto-restart background processes.

## Process Management

### View Processes
```bash
# All processes
ps aux

# Filter by name
ps aux | grep python
ps aux | grep flask
ps aux | grep "apps/web/run.py"

# Tree view
ps auxf

# By user
ps -u $USER

# Specific PID info
ps -p <PID> -o pid,ppid,cmd,%mem,%cpu
```

### Kill Processes
```bash
# Graceful stop
kill <PID>

# Force kill
kill -9 <PID>

# Kill by name
pkill -f "run.py"
killall python3

# Kill all matching
ps aux | grep "[p]ython.*run.py" | awk '{print $2}' | xargs kill
```

## Server Management

### Start Server
```bash
# Start in background
cd /home/mulugeta/projects/multi_mode_calculator
setsid python3 apps/web/run.py > /tmp/web_calc.log 2>&1 &

# With nohup
nohup python3 apps/web/run.py > /tmp/web_calc.log 2>&1 &

# Capture PID
echo $! > /tmp/web_calc.pid
```

### Check Server Status
```bash
# Check if running
ps aux | grep "run.py" | grep -v grep

# Check port
lsof -i :5000
ss -tlnp | grep 5000
netstat -tlnp 2>/dev/null | grep 5000

# Health check
curl -s http://localhost:5000/api/health

# Check PID file
cat /tmp/web_calc.pid 2>/dev/null && \
  ps -p $(cat /tmp/web_calc.pid) > /dev/null 2>&1 && \
  echo "Server running" || echo "Server not running"
```

### Restart Server
```bash
# Stop existing
if [ -f /tmp/web_calc.pid ]; then
    kill $(cat /tmp/web_calc.pid) 2>/dev/null
    rm /tmp/web_calc.pid
fi

# Also kill any orphan processes
pkill -f "run.py" 2>/dev/null
sleep 1

# Start fresh
cd /home/mulugeta/projects/multi_mode_calculator
setsid python3 apps/web/run.py > /tmp/web_calc.log 2>&1 &
echo $! > /tmp/web_calc.pid
echo "Server started on port 5000"
```

## Auto-Restart Script

```bash
#!/bin/bash
# auto_restart.sh — Monitor and auto-restart server

APP_NAME="calculator"
PID_FILE="/tmp/web_calc.pid"
LOG_FILE="/tmp/web_calc.log"
APP_CMD="cd /home/mulugeta/projects/multi_mode_calculator && python3 apps/web/run.py"
CHECK_INTERVAL=30
MAX_RESTARTS=5
RESTART_COUNT=0

is_running() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        ps -p "$pid" > /dev/null 2>&1
        return $?
    fi
    return 1
}

start_server() {
    setsid $APP_CMD > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    RESTART_COUNT=$((RESTART_COUNT + 1))
    echo "[$(date)] Server started (PID: $!, restart #$RESTART_COUNT)"
}

stop_server() {
    if [ -f "$PID_FILE" ]; then
        kill $(cat "$PID_FILE") 2>/dev/null
        rm "$PID_FILE"
        echo "[$(date)] Server stopped"
    fi
}

# Trap signals
trap 'stop_server; exit 0' SIGTERM SIGINT

# Main loop
echo "[$(date)] Monitor started for $APP_NAME"

while [ $RESTART_COUNT -lt $MAX_RESTARTS ]; do
    if is_running; then
        # Server is running, check health
        if ! curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
            echo "[$(date)] Health check failed, restarting..."
            stop_server
            sleep 2
            start_server
        fi
    else
        # Server not running, start it
        echo "[$(date)] Server not running, starting..."
        start_server
    fi

    sleep $CHECK_INTERVAL
done

echo "[$(date)] Max restarts ($MAX_RESTARTS) reached. Monitor exiting."
stop_server
```

## Log Monitoring

```bash
# Tail live logs
tail -f /tmp/web_calc.log

# Search logs for errors
grep -i "error" /tmp/web_calc.log
grep -i "traceback" /tmp/web_calc.log

# Last N lines
tail -50 /tmp/web_calc.log

# Log with timestamps
grep "2024" /tmp/web_calc.log | tail -20

# Count errors
grep -c "ERROR" /tmp/web_calc.log
```

## Port Management

```bash
# What's using port 5000?
lsof -i :5000
fuser 5000/tcp 2>/dev/null

# Kill process on port
fuser -k 5000/tcp

# Check all listening ports
ss -tlnp

# Check specific ports
for port in 5000 8080 3000; do
    ss -tlnp | grep ":$port " > /dev/null && \
        echo "Port $port: IN USE" || \
        echo "Port $port: AVAILABLE"
done
```

## System Resource Monitoring

```bash
# CPU and memory
top -b -n 1 | head -20

# Specific process resources
ps -p $(cat /tmp/web_calc.pid) -o pid,%cpu,%mem,cmd

# Disk usage
df -h
du -sh /home/mulugeta/projects/multi_mode_calculator

# Memory
free -h

# Open files for a process
lsof -p $(cat /tmp/web_calc.pid) | wc -l
```

## Rules

- ALWAYS log to files, not terminal, for background processes
- Use PID files to track running processes
- Implement graceful shutdown (SIGTERM, not SIGKILL)
- Monitor health endpoints, not just process existence
- Set maximum restart limits to prevent infinite loops
- Rotate log files to prevent disk fill
- Check port availability before starting servers
