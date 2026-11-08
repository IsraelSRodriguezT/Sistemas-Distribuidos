# Práctica 3 - Simulador de Concurrencia con Microservicios

Conjunto de microservicios Spring Boot y un frontend web para visualizar problemas clásicos de sincronización: semáforos, exclusión mutua, productor-consumidor y políticas de acceso.

## Ejecución

### Con Docker (recomendado, requiere Docker)

```bash
./run.sh
```

Construye y arranca los seis contenedores, espera a que los servicios respondan e intenta abrir el navegador. Si no se abre automáticamente, entra a:

```
http://localhost:5500
```

La primera ejecución tarda varios minutos porque Maven descarga las dependencias.

```bash
docker compose logs -f   # ver logs
docker compose down      # detener todo
```

### Sin Docker (requiere Java 17 y Maven; el wrapper `./mvnw` viene incluido)

Cada servicio en su propia terminal:

```bash
cd estacionamiento-service && ./mvnw spring-boot:run
cd cajero-service && ./mvnw spring-boot:run
cd fabrica-service && ./mvnw spring-boot:run
cd puente-service && ./mvnw spring-boot:run
cd impresion-service && ./mvnw spring-boot:run
```

Frontend (debe servirse en el puerto 5500 por la configuración CORS del cajero):

```bash
cd frontend
python3 -m http.server 5500
```

## Estructura

```
SyncLab/
├── estacionamiento-service/   # Puerto 8080
├── cajero-service/            # Puerto 8082
├── fabrica-service/           # Puerto 8083
├── puente-service/            # Puerto 8084
├── impresion-service/         # Puerto 8085
├── frontend/                  # Puerto 5500
├── docker-compose.yml
└── run.sh
```

Cada servicio tiene su propio `Dockerfile` multi-etapa (Maven → JRE 17).

## Funcionamiento

### Servicios

- **estacionamiento-service** (`:8080`): semáforo contador con capacidad de cuatro plazas; los vehículos esperan cuando no hay espacio y se liberan al salir.
- **cajero-service** (`:8082`): exclusión mutua sobre un saldo compartido; simula operaciones con mutex y sin mutex para comparar resultados.
- **fabrica-service** (`:8083`): productor-consumidor con buffer limitado; ejecución secuencial y concurrente, con eventos en vivo mediante SSE.
- **puente-service** (`:8084`): cruce de vehículos en dos direcciones con distintas políticas de acceso y análisis de inanición; eventos en vivo mediante SSE.
- **impresion-service** (`:8085`): flujo por etapas (diseño → revisión → impresión) usando el patrón command.

### Frontend

- Interfaz estática que consume las APIs REST y SSE de cada servicio; `frontend/js/config.js` define las URLs.
- Páginas por ejercicio: `index.html` (estacionamiento), `ejercicio2.html` (cajero), `ejercicio3.html` (fábrica), `ejercicio4.html` (puente) y `ejercicio5.html` (impresión).
- No contiene lógica de servidor: solo conoce los endpoints de los microservicios.
