---
name: http-client
description: Use when testing APIs, making HTTP requests, checking endpoints, or debugging web services. Trigger on phrases like "test API", "curl", "HTTP request", "check endpoint", "API test", "REST", "POST", "GET", "webhook", "request", "response", or when validating Flask routes.
---

# HTTP Client Skill

Test APIs and web services using curl and other tools.

## curl Reference

### Basic Requests

```bash
# GET request
curl http://localhost:5000/api/health

# GET with pretty JSON
curl -s http://localhost:5000/api/health | python3 -m json.tool

# POST with JSON body
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 3 * 4"}'

# POST with file body
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d @request.json

# PUT request
curl -X PUT http://localhost:5000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"angle_mode": "degrees"}'

# DELETE request
curl -X DELETE http://localhost:5000/api/history/123
```

### Response Inspection

```bash
# Show headers
curl -I http://localhost:5000/api/health

# Show response headers + body
curl -i http://localhost:5000/api/health

# Show only status code
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health

# Show timing
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000

# Verbose output
curl -v http://localhost:5000/api/health
```

### Authentication

```bash
# Basic auth
curl -u user:password http://localhost:5000/api/admin

# Bearer token
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/protected

# API key header
curl -H "X-API-Key: <key>" http://localhost:5000/api/data
```

## API Testing Workflow

```bash
# 1. Start server
cd /home/mulugeta/projects/multi_mode_calculator && python3 apps/web/run.py &

# 2. Wait for startup
sleep 2

# 3. Health check
curl -s http://localhost:5000/api/health | python3 -m json.tool

# 4. Test standard mode
curl -s -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 3"}' | python3 -m json.tool

# 5. Test financial mode
curl -s -X POST http://localhost:5000/api/financial/mortgage \
  -H "Content-Type: application/json" \
  -d '{"principal": 100000, "annual_rate": 0.05, "years": 30}' \
  | python3 -m json.tool

# 6. Test error handling
curl -s -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "1/0"}' | python3 -m json.tool
```

## Batch Testing Script

```bash
#!/bin/bash
# test_api.sh — Run all API tests

BASE_URL="http://localhost:5000"
PASS=0
FAIL=0

test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local expected=$4

    if [ -z "$data" ]; then
        response=$(curl -s -X $method "$BASE_URL$url" -w "\n%{http_code}")
    else
        response=$(curl -s -X $method "$BASE_URL$url" \
            -H "Content-Type: application/json" \
            -d "$data" -w "\n%{http_code}")
    fi

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" = "$expected" ]; then
        echo "✓ $method $url → $status_code"
        PASS=$((PASS + 1))
    else
        echo "✗ $method $url → $status_code (expected $expected)"
        echo "  Response: $body"
        FAIL=$((FAIL + 1))
    fi
}

# Health check
test_endpoint GET "/api/health" "" "200"

# Standard calculator
test_endpoint POST "/api/calculate" '{"expression":"2+3"}' "200"
test_endpoint POST "/api/calculate" '{"expression":"1/0"}' "200"

# Financial
test_endpoint POST "/api/financial/mortgage" \
    '{"principal":100000,"annual_rate":0.05,"years":30}' "200"

echo ""
echo "Results: $PASS passed, $FAIL failed"
```

## Response Analysis

```bash
# Parse JSON with jq
curl -s http://localhost:5000/api/health | jq '.status'
curl -s http://localhost:5000/api/calculate | jq '.result'

# Extract specific field
curl -s -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "sqrt(144)"}' | jq '.result'

# Check array length
curl -s http://localhost:5000/api/history | jq 'length'
```

## Rules

- ALWAYS test both success and error responses
- Check status codes, not just response bodies
- Use pretty-print (`python3 -m json.tool` or `jq`) for readability
- Test with invalid inputs to verify error handling
- Check response headers for content-type
