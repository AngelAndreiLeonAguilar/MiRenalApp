#!/bin/sh

# Modificación Observación N1: Comprobar que la base de datos esté lista antes de migrar
echo "Esperando a la base de datos en db_network..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "¡Base de datos disponible!"

# Ejecutar las migraciones de Django de manera automática
echo "Ejecutando migraciones de la base de datos..."
python manage.py migrate --noinput

# Recolectar archivos estáticos para que Nginx pueda tomarlos (Tu decorado)
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Arrancar Gunicorn en producción
echo "Iniciando Gunicorn..."
exec gunicorn MiRenalApp.wsgi:application --bind 0.0.0.0:8000