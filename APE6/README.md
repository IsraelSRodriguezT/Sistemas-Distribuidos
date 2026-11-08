# Práctica 6 — Monitoreo de Flota con MQTT, RabbitMQ y Spring Boot

Flujo completo de telemetría: un simulador publica datos por MQTT, un puente los reenvía a RabbitMQ, y una aplicación Spring Boot los consume, los guarda en H2 y los expone mediante una API REST.


## Ejecución

Solo se necesita **Docker**. No hace falta instalar Java, Maven ni Python: cada servicio se construye dentro de su contenedor.

### Uso normal — una sola máquina

```bash
./run.sh
```

Levanta Mosquitto, RabbitMQ, la app Spring, el puente y el simulador. La primera ejecución tarda varios minutos porque Maven descarga las dependencias.

- API: `http://localhost:8080/api/fleet/status`
- Telemetría: `http://localhost:8080/api/fleet/vehicle/VH-001/telemetria`
- Panel RabbitMQ: `http://localhost:15672` — usuario `admin`, contraseña `admin123`

```bash
docker compose logs -f fleet-monitor puente simulador   # ver el flujo
docker compose down                                     # detener
```

### Laboratorio (dos máquinas)

Ambas máquinas necesitan Docker.

#### Máquina A — brokers (Mosquitto + RabbitMQ)

1. Obtén la IP de esta máquina (la que asigne el access point):
   ```bash
   ip addr | grep "inet "
   # o: hostname -I
   ```
2. Levanta los brokers desde la carpeta del proyecto:
   ```bash
   docker compose up -d mosquitto rabbitmq
   docker compose ps
   ```
3. Habilita los puertos en el firewall, si está activo:
   ```bash
   # ufw
   sudo ufw allow 1883/tcp
   sudo ufw allow 5672/tcp
   sudo ufw allow 15672/tcp

   # firewalld
   sudo firewall-cmd --add-port=1883/tcp --add-port=5672/tcp --add-port=15672/tcp --permanent
   sudo firewall-cmd --reload
   ```
4. Panel de RabbitMQ desde cualquier máquina: `http://<IP_MAQUINA_A>:15672` (`admin` / `admin123`).

#### Máquina B — aplicación, puente y simulador

Un solo comando, pasando la IP de la máquina A:

```bash
./run-laboratorio.sh <IP_MAQUINA_A>
```

El script:
1. Verifica que la máquina A responde en `1883` y `5672`.
2. Construye y levanta en Docker la app, el puente y el simulador.
3. Los conecta a los brokers de A mediante `MQTT_BROKER` y `RABBITMQ_HOST`.
4. Espera a que la API esté disponible y muestra las URLs.

- API en B: `http://localhost:8080/api/fleet/status`
- Panel RabbitMQ: `http://<IP_MAQUINA_A>:15672`
- Detener: `docker compose -f docker-compose-lab.yml down`

Si quieres consultar la API desde la máquina A, habilita el `8080` en B (`sudo ufw allow 8080/tcp` o el equivalente en firewalld) y usa `http://<IP_MAQUINA_B>:8080/...`.

## Estructura

```
Practica6/
├── Dockerfile                 # App Spring (multi-etapa Maven → JRE)
├── docker-compose.yml         # Todo en una máquina: brokers + app + puente + simulador
├── docker-compose-lab.yml     # Laboratorio: app + puente + simulador (brokers remotos)
├── pom.xml
├── run.sh                     # Uso normal en una sola máquina
├── run-laboratorio.sh         # Laboratorio de dos máquinas
├── mosquitto/
│   └── config/mosquitto.conf
├── mqtt/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── mqtt_rabbitmq_bridge.py
│   ├── simulador_sensores.py
│   └── suscriptor_almacenador.py   # de la práctica anterior; no se usa aquí
└── src/main/java/com/fleet/monitor/
    ├── config/RabbitMQConfig.java
    ├── consumer/GpsConsumer.java
    ├── consumer/AlertConsumer.java
    ├── controller/FleetController.java
    ├── model/GpsMessage.java
    └── repository/GpsDataRepository.java
```

## Arquitectura

```text
simulador_sensores.py
        │  MQTT (flota/#)
        ▼
mosquitto (1883)
        │
        ▼
mqtt_rabbitmq_bridge.py
        │  exchange.fleet
        ├── gps.routing   ──► cola.gps.telemetria        ──► GpsConsumer ──► H2
        ├── temp.alert    ──► cola.alertas.temperatura   ──► AlertConsumer ──► cola.notificaciones
        └── fuel.routing  ──► cola.combustible.nivel     ──► AlertConsumer ──► cola.notificaciones
                                                                    │
                                                          API REST (:8080)
```

## Funcionamiento

### Simulador
- Publica cada 5 segundos 9 mensajes (GPS, temperatura y combustible para `VH-001`, `VH-002` y `VH-003`).
- Topics: `flota/{vehiculo}/gps`, `flota/{vehiculo}/temperatura` y `flota/{vehiculo}/combustible`.

### Puente MQTT → RabbitMQ
- Escucha `flota/#` y publica en el exchange directo `exchange.fleet`.
- GPS → `gps.routing` (`cola.gps.telemetria`).
- Temperatura mayor a 4 °C → `temp.alert` (`cola.alertas.temperatura`).
- Combustible menor a 20 % → `fuel.routing` (`cola.combustible.nivel`).
- Declara colas durables y publica mensajes persistentes.

### Aplicación Spring Boot
- `GpsConsumer`: consume `cola.gps.telemetria`, convierte el JSON y guarda cada lectura en H2 (`gps_data`).
- `AlertConsumer`: consume las colas de temperatura y combustible, y reenvía las alertas a `cola.notificaciones`.
- `FleetController`: expone el estado de la flota y la telemetría por vehículo.

### Base de datos
- H2 **en memoria** (`jdbc:h2:mem:fleetdb`), embebida en la aplicación.
- Hibernate crea la tabla `gps_data` al iniciar.
- Los datos se pierden al reiniciar el contenedor de la app.

## Endpoints

```bash
# Resumen de la flota
curl http://localhost:8080/api/fleet/status

# Últimas 20 lecturas GPS de un vehículo
curl http://localhost:8080/api/fleet/vehicle/VH-001/telemetria
```

Ejemplo de `/status`:

```json
{
  "totalVehicles": 3,
  "totalReadings": 45,
  "lastUpdate": "2026-11-08T05:30:00Z",
  "timestamp": "2026-11-08T05:30:12.345+00:00"
}
```

## Verificar RabbitMQ

- Panel: `http://localhost:15672` (`admin` / `admin123`) en la prueba local, o `http://<IP_MAQUINA_A>:15672` en el laboratorio.
- Colas esperadas: `cola.gps.telemetria`, `cola.alertas.temperatura`, `cola.combustible.nivel` y `cola.notificaciones`.

```bash
docker exec rabbitmq_broker rabbitmqctl list_queues name messages
```

## Notas

- `suscriptor_almacenador.py` pertenece a la práctica anterior (SQLite); en esta práctica el almacenamiento lo hace Spring con H2 y no forma parte del flujo.
- `.venv` y `target` no se suben al repositorio (están en `.gitignore`).
