#!/bin/bash
set -e

echo "Setting up development environment..."

mkdir -p /home/vscode/.npm-global
npm config set prefix '/home/vscode/.npm-global'
export PATH=/home/vscode/.npm-global/bin:$PATH
echo 'export PATH=/home/vscode/.npm-global/bin:$PATH' >> /home/vscode/.bashrc

python3 --version
node --version
npm --version
docker --version
docker compose version

git config --global pull.rebase true
git config --global core.autocrlf input

echo "Installing backend dependencies..."
cd web/backend
pip install -r requirements.txt

echo "Installing frontend dependencies..."
cd ../frontend
npm install --legacy-peer-deps

cd ../..
REPO_ROOT="$(pwd)"

if [ ! -f web/backend/.env ]; then
    cat > web/backend/.env << 'EOF'
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
CORS_ORIGINS=["http://localhost:3000"]
EOF
fi

if [ ! -f web/frontend/.env ]; then
    cat > web/frontend/.env << 'EOF'
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEFAULT_LANGUAGE=es
REACT_APP_ENABLE_MOCK_API=false
EOF
fi

chmod +x bin/dev
chmod +x .devcontainer/startup.sh
chmod +x .devcontainer/healthcheck.sh

echo "Setup complete. Run './bin/dev' or start services manually."
