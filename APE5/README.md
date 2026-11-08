# Práctica 5 — Mensajería Distribuida con MQTT y RabbitMQ

Simulación de una flota de vehículos que publica telemetría por MQTT, la almacena en SQLite y la reenvía a colas durables de RabbitMQ.


## Ejecución

### Con Docker (un solo comando, requiere Docker)

```bash
./run.sh
```

Levanta Mosquitto, RabbitMQ, el suscriptor, el puente y el simulador. Los logs muestran en vivo las lecturas, las inserciones y las alertas. `Ctrl+C` detiene los servicios.

- Panel de RabbitMQ: `http://localhost:15672` — usuario `flota`, contraseña `flota123`.
- Base SQLite: `./telemetria.db` (se crea/actualiza en la carpeta del proyecto).

Para limpiar los contenedores:

```bash
docker compose down      # conserva las colas
docker compose down -v   # elimina también el volumen de RabbitMQ
```

### Sin Docker (manual)

Requiere Python 3 y los brokers corriendo en Docker:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
docker compose up -d mosquitto rabbitmq
```

Luego, en tres terminales:

```bash
.venv/bin/python suscriptor_almacenador.py
.venv/bin/python mqtt_rabbitmq_bridge.py
.venv/bin/python simulador_sensores.py
```

## Estructura

```
Practica5/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.sh
├── mosquitto/
│   ├── config/mosquitto.conf
│   └── data/
├── simulador_sensores.py
├── suscriptor_almacenador.py
├── mqtt_rabbitmq_bridge.py
├── telemetria.db          # se crea al ejecutar
└── README.md
```
## Arquitectura

```text
simulador_sensores.py
        │  MQTT (flota/#)
        ▼
mosquitto (1883)
        │
        ├──────────────► suscriptor_almacenador.py ──► telemetria.db
        │
        └──────────────► mqtt_rabbitmq_bridge.py ───► RabbitMQ (5672)
                                                          ├── cola.gps.telemetria
                                                          ├── cola.alertas.temperatura
                                                          └── cola.combustible.nivel
```

## Funcionamiento

### simulador_sensores.py
- Cada 5 segundos publica 9 mensajes (GPS, temperatura y combustible para `VH-001`, `VH-002` y `VH-003`).
- Topics: `flota/{vehiculo}/gps`, `flota/{vehiculo}/temperatura`, `flota/{vehiculo}/combustible`.
- Usa QoS 1 y publica JSON con marca de tiempo UTC.

### suscriptor_almacenador.py
- Se suscribe a `flota/+/gps`, `flota/+/temperatura` y `flota/+/combustible`.
- Valida el JSON y guarda cada lectura en SQLite (`gps_data`, `temp_data`, `fuel_data`).
- Marca alertas cuando la temperatura supera 4 °C o el combustible baja de 20 %.

### mqtt_rabbitmq_bridge.py
- Escucha todo `flota/#` y reenvía a RabbitMQ.
- GPS → `cola.gps.telemetria`; temperatura alta → `cola.alertas.temperatura`; combustible bajo → `cola.combustible.nivel`.
- Las colas son durables y los mensajes persistentes; reintenta la conexión si RabbitMQ no está disponible.

### Brokers
- **Mosquitto** (`:1883`): broker MQTT con acceso anónimo y persistencia en `mosquitto/data`.
- **RabbitMQ** (`:5672`, panel `:15672`): colas durables declaradas por el puente.

### Variables de entorno
- `MQTT_BROKER` (por defecto `localhost`): host del broker MQTT.
- `RABBITMQ_HOST`, `RABBITMQ_PUERTO`, `RABBITMQ_USER`, `RABBITMQ_PASS`: conexión AMQP del puente.

## Verificar datos

Opcional: requiere `sqlite3` en el host. La base se crea en `./telemetria.db`.

```bash
sqlite3 -header -column telemetria.db \
  "SELECT id, vehicle_id, lat, lng, speed, timestamp FROM gps_data ORDER BY id DESC LIMIT 9;"

sqlite3 -header -column telemetria.db \
  "SELECT * FROM temp_data WHERE temperature > 4 ORDER BY id DESC;"

sqlite3 -header -column telemetria.db \
  "SELECT * FROM fuel_data WHERE fuel_level < 20 ORDER BY id DESC;"
```
