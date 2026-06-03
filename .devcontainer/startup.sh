#!/bin/bash
set -e

echo "🚀 Starting DevContainer services..."

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Ensure Docker socket access
echo "🔧 Configuring Docker permissions..."
sudo chmod 666 /var/run/docker.sock 2>/dev/null || true
sudo usermod -aG docker vscode 2>/dev/null || true

# Configure npm permissions
echo "🔧 Configuring npm permissions..."
mkdir -p /home/vscode/.npm-global
npm config set prefix '/home/vscode/.npm-global'
export PATH=/home/vscode/.npm-global/bin:$PATH

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd "$REPO_ROOT/web/backend"
pip install --user -r requirements.txt 2>/dev/null || pip install -r requirements.txt 2>/dev/null || true

# Start Redis via DevContainer docker-compose
echo "📦 Starting Redis..."
cd "$REPO_ROOT"
docker-compose -f .devcontainer/docker-compose.yml up -d redis

echo "⏳ Waiting for Redis to be ready..."
sleep 5

echo "✅ Redis started. Use './dev.sh start' or run backend/frontend manually."
echo "   Backend:  cd web/backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo "   Frontend: cd web/frontend && npm start"
