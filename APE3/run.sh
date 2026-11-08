#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

docker compose up --build -d

echo ""
echo "Esperando a que los servicios respondan (la primera vez puede tardar varios minutos)..."

for _ in $(seq 1 90); do
    listos=0
    for puerto in 8080 8082 8083 8084 8085; do
        if (echo > "/dev/tcp/127.0.0.1/$puerto") 2>/dev/null; then
            listos=$((listos + 1))
        fi
    done
    if [ "$listos" -eq 5 ]; then
        break
    fi
    sleep 2
done

echo ""
echo "SyncLab disponible en http://localhost:5500"
echo "Logs:     docker compose logs -f"
echo "Detener:  docker compose down"

if command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:5500 >/dev/null 2>&1 || true
fi
