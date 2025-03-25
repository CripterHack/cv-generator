#!/bin/bash
set -e

check_service() {
    local service=$1
    local port=$2
    local max_attempts=$3
    local attempt=1

    echo "Verificando $service en puerto $port..."
    while ! nc -z localhost $port; do
        if [ $attempt -eq $max_attempts ]; then
            echo "❌ $service no está disponible después de $max_attempts intentos"
            return 1
        fi
        echo "⏳ Intento $attempt de $max_attempts..."
        sleep 2
        ((attempt++))
    done
    echo "✅ $service está funcionando correctamente"
    return 0
}

# Verificar servicios
check_service "Frontend" 3000 5
check_service "Backend" 8000 5
check_service "Redis" 6379 5 