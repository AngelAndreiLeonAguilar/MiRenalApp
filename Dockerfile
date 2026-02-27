# Imagen base con Python
FROM python:3.11

# Configuración del directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto: migrar y correr el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]