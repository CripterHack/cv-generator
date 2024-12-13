#!/bin/bash

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    if [ "$(uname)" == "Linux" ]; then
        echo "DISPLAY=$DISPLAY" > .env
    elif [ "$(uname)" == "Darwin" ]; then
        # Para macOS
        echo "DISPLAY=host.docker.internal:0" > .env
    else
        # Para Windows
        echo "DISPLAY=host.docker.internal:0.0" > .env
    fi
fi

# Permitir conexiones X11 desde cualquier host
if [ "$(uname)" == "Linux" ]; then
    xhost +local:root
fi 