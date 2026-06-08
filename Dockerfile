# Usar la imagen oficial de Python en su versión ligera
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc y asegurar salida inmediata de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Modificación Observación 7: Se elimina 'gcc' y 'libpq-dev'. Ya no hacen falta 
# porque usas psycopg2-binary, reduciendo el tamaño y tiempo de construcción.
# Instalamos netcat-openbsd para permitirle al script comprobar la base de datos.
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalar los requerimientos de Python del proyecto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Modificación Observación 6: Fijamos una versión estable de gunicorn para evitar sorpresas
RUN pip install --no-cache-dir gunicorn==21.2.0

# Copiar el proyecto de forma autónoma
COPY . /app/

# Modificación Observación N1: Copiar el script de automatización y darle permisos de ejecución
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Modificación Observación N1: Cambiamos el inicio directo por el punto de entrada automatizado
ENTRYPOINT ["/entrypoint.sh"]