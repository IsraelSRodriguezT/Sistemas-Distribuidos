#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

IP="${1:-}"

if [ -z "$IP" ]; then
    echo "Uso: ./run-laboratorio.sh <IP_DE_LA_MAQUINA_BROKERS>"
    exit 1
fi

echo "Verificando conexion con la maquina de brokers ($IP)..."

for puerto in 1883 5672; do
    if ! (echo > "/dev/tcp/$IP/$puerto") 2>/dev/null; then
        echo "ERROR: no se puede conectar a $IP:$puerto."
        echo "Verifica que la maquina A tenga Mosquitto y RabbitMQ levantados"
        echo "y que los puertos 1883 y 5672 esten habilitados en su firewall."
        exit 1
    fi
done

export MQTT_BROKER="$IP"
export RABBITMQ_HOST="$IP"

echo "Levantando app, puente y simulador en Docker..."
docker compose -f docker-compose-lab.yml up --build -d

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
echo "Panel RabbitMQ: http://$IP:15672  (admin / admin123)"
echo "Logs:           docker compose -f docker-compose-lab.yml logs -f"
echo "Detener:        docker compose -f docker-compose-lab.yml down"
