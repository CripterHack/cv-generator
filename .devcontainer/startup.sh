#!/bin/bash
set -e

echo "Starting DevContainer services..."

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

sudo chmod 666 /var/run/docker.sock 2>/dev/null || true
sudo usermod -aG docker vscode 2>/dev/null || true

mkdir -p /home/vscode/.npm-global
npm config set prefix '/home/vscode/.npm-global'
export PATH=/home/vscode/.npm-global/bin:$PATH

echo "Starting Redis..."
docker compose -f "$REPO_ROOT/.devcontainer/docker-compose.yml" up -d redis

echo "Waiting for Redis to be ready..."
sleep 5

echo "Redis started. Use './bin/dev' or run backend/frontend manually."
echo "   Backend:  cd web/backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo "   Frontend: cd web/frontend && npm start"
