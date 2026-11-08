FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_rabbitmq_bridge.py simulador_sensores.py ./

CMD ["python", "simulador_sensores.py"]
