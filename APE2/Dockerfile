FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copiar solo el código y los archivos de comunicación (vacíos)
COPY servidor/servidor.py ./servidor/
COPY cliente/cliente.py ./cliente/
COPY compartido/entrada_servidor.txt ./compartido/
COPY compartido/salida_servidor.txt ./compartido/

CMD ["python3", "servidor/servidor.py"]
