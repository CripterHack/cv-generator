#!/bin/bash
set -e

echo "🚀 Iniciando servicios..."

# Asegurar que el usuario tenga acceso al socket de Docker
echo "🔧 Configurando permisos de Docker..."
sudo chmod 666 /var/run/docker.sock
sudo usermod -aG docker vscode

# Configurar permisos de npm
echo "🔧 Configurando permisos de npm..."
mkdir -p /home/vscode/.npm-global
npm config set prefix '/home/vscode/.npm-global'
export PATH=/home/vscode/.npm-global/bin:$PATH

# Instalar dependencias del backend
echo "📦 Instalando dependencias del backend..."
cd /workspaces/cv-generator/web/backend
pip install --user -r requirements.txt

# Crear directorio api si no existe
if [ ! -d "api" ]; then
    mkdir -p api
    touch api/__init__.py
    # Crear cv_endpoints.py si no existe
    if [ ! -f "api/cv_endpoints.py" ]; then
        cat > api/cv_endpoints.py << EOL
from fastapi import APIRouter

router = APIRouter()

@router.get("/cv")
async def get_cv():
    return {"message": "CV endpoint"}
EOL
    fi
fi

# Iniciar Redis
echo "📦 Iniciando Redis..."
cd /workspaces/cv-generator
docker-compose -f .devcontainer/docker-compose.yml up -d redis

# Esperar a que Redis esté listo
echo "⏳ Esperando a que Redis esté listo..."
sleep 5

# Iniciar backend
# echo "🔧 Iniciando backend..."
# cd /workspaces/cv-generator/web/backend
# python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Esperar a que el backend esté listo
# echo "⏳ Esperando a que el backend esté listo..."
# sleep 5

# Iniciar frontend
# echo "🌐 Iniciando frontend..."
# cd /workspaces/cv-generator/web/frontend

# Limpiar node_modules y reinstalar dependencias
# echo "🧹 Limpiando instalación anterior..."
# rm -rf node_modules package-lock.json
# npm cache clean --force

# echo "📦 Instalando dependencias del frontend..."
# export NODE_OPTIONS="--max-old-space-size=4096"
# npm install --legacy-peer-deps

# echo "🚀 Iniciando aplicación frontend..."
# BROWSER=none npm start &

# Mantener el script en ejecución
# wait