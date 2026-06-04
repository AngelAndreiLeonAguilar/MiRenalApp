# Usar la imagen oficial de Python en su versión ligera
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc y asegurar salida inmediata de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar psycopg2 (Saneamiento crítico)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar los requerimientos de Python del proyecto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Instalar gunicorn para el manejo de peticiones en producción
RUN pip install --no-cache-dir gunicorn

# Copiar el proyecto de forma autónoma
COPY . /app/

EXPOSE 8000

# comando definitivo que sustituye 'runserver' por Gunicorn
CMD ["gunicorn", "MiRenalApp.wsgi:application", "--bind", "0.0.0.0:8000"]