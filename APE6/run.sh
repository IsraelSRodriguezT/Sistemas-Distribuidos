#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Construyendo y levantando Practica 6 (MQTT + RabbitMQ + Spring Boot)..."
docker compose up --build -d

echo ""
echo "Esperando a que la API responda (la primera vez tarda por Maven)..."

for _ in $(seq 1 150); do
    if (echo > /dev/tcp/127.0.0.1/8080) 2>/dev/null; then
        break
    fi
    sleep 2
done

echo ""
echo "API:            http://localhost:8080/api/fleet/status"
echo "Telemetria:     http://localhost:8080/api/fleet/vehicle/VH-001/telemetria"
echo "Panel RabbitMQ: http://localhost:15672  (admin / admin123)"
echo "Logs:           docker compose logs -f fleet-monitor puente simulador"
echo "Detener:        docker compose down"
