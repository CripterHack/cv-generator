#!/bin/bash

# Función para manejar la señal SIGINT (Ctrl+C)
trap 'kill 0' SIGINT

# Iniciar servicios en paralelo
echo "🚀 Iniciando servicios..."

# Iniciar backend
cd web/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Iniciar frontend
cd ../frontend
npm start &

# Esperar a que todos los procesos terminen
wait
