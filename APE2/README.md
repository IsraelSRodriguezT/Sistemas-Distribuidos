# Práctica 2 - Servidor Cliente con Archivos Compartidos

Servicio activo que procesa mensajes usando archivos de texto como canal de comunicación.

## Ejecución

### Con Docker (recomendado, requiere Docker)

```bash
./run.sh
```

Arranca el servidor y envía un mensaje. Para enviar otro, vuelve a ejecutar `./run.sh`.
Para detener el servidor: `docker compose down`.

### Sin Docker (dos terminales)

Primero entra al directorio del proyecto (donde está este README):

```bash
cd Practica2
```

Terminal 1 (servidor):

```bash
python3 servidor/servidor.py
```

Terminal 2 (cliente):

```bash
python3 cliente/cliente.py
```

## Estructura

```
Practica2/
├── servidor/servidor.py      # Servicio activo
├── cliente/cliente.py        # Cliente
├── compartido/               # Carpeta de comunicación (fuera de ambos)
│   ├── entrada_servidor.txt  # Mensajes del cliente
│   └── salida_servidor.txt   # Respuestas del servidor
├── Dockerfile
├── docker-compose.yml
└── run.sh
```

## Funcionamiento

### Servidor
- Se ejecuta continuamente y revisa `compartido/entrada_servidor.txt` cada 2 segundos.
- Detecta solo el contenido nuevo y guarda la posición leída en `compartido/.ultima_posicion.txt`, así no reprocesa mensajes.
- Procesa cada mensaje (lo convierte a mayúsculas y lo invierte) y escribe el resultado en `compartido/salida_servidor.txt`.
- Maneja archivos vacíos y reinicia la posición si el archivo se vacía.

### Cliente
- Pide un mensaje al usuario y lo escribe en `entrada_servidor.txt`.
- Espera 3 segundos (latencia simulada) y lee la última respuesta de `salida_servidor.txt`.
- Muestra el resultado en pantalla.
- Solo conoce los archivos de entrada y salida; no asume cómo funciona el servidor.
