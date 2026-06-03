#!/bin/bash
set -e

check_service() {
    local service=$1
    local port=$2
    local max_attempts=$3
    local attempt=1

    echo "Verifying $service on port $port..."
    while ! nc -z localhost $port; do
        if [ $attempt -eq $max_attempts ]; then
            echo "❌ $service not available after $max_attempts attempts"
            return 1
        fi
        echo "⏳ Attempt $attempt of $max_attempts..."
        sleep 2
        ((attempt++))
    done
    echo "✅ $service is running"
    return 0
}

# Redis is the only auto-started service in the DevContainer
check_service "Redis" 6379 5

# Check optional services (may not be running)
echo ""
echo "Optional services (start manually if needed):"
nc -z localhost 8000 2>/dev/null && echo "✅ Backend (port 8000) is running" || echo "ℹ️  Backend (port 8000) not running — start with: cd web/backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
nc -z localhost 3000 2>/dev/null && echo "✅ Frontend (port 3000) is running" || echo "ℹ️  Frontend (port 3000) not running — start with: cd web/frontend && npm start"
