#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Iniciando Practica 5 (MQTT + RabbitMQ)..."
echo "Panel RabbitMQ: http://localhost:15672  (flota / flota123)"
echo "Base de datos:  ./telemetria.db"
echo "Ctrl+C detiene los servicios."
echo ""

docker compose up --build
