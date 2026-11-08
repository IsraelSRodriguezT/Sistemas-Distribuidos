#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Arranca el servidor (si ya está activo, no lo reinicia) y envía un mensaje
docker compose up -d --build servidor
docker compose run --rm cliente

echo ""
echo "El servidor sigue activo. Para enviar otro mensaje: ./run.sh"
echo "Para detenerlo: docker compose down"
