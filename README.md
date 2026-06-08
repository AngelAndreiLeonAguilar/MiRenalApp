# MiRenalApp (Kidnely Health) - Guía de Despliegue

Este proyecto utiliza Docker y Docker Compose para empaquetar y ejecutar tanto la aplicación web (Django) como el motor de base de datos (PostgreSQL 15) de forma centralizada en un único servidor.

## 🛠️ Requisitos Previos
* Docker y Docker Compose instalados en el servidor de despliegue.
* Tener creada la red de Docker compartida (si utilizas un contenedor proxy inverso externo como Nginx):
  ```bash
  sudo docker network create nginx-proxy-network
🚀 Pasos para ejecutar el Despliegue
Sigue estos pasos en la terminal de tu servidor para poner en marcha la aplicación:

1. Clonar el repositorio
Bash
git clone <URL_DE_TU_REPOSITORIO>
cd MiRenalApp
2. Configurar el archivo de entorno
Crea tu archivo .env a partir de la plantilla de ejemplo y configura tus credenciales de producción y bases de datos:

Bash
cp .env.example .env
nano .env
3. Construir y levantar los contenedores
Ejecuta el siguiente comando para compilar la imagen de Django e iniciar ambos servicios (web y db) en segundo plano:

Bash
sudo docker compose up -d --build
⚡ Automatización e Inicialización del Sistema
El contenedor está diseñado con un script de inicio inteligente (entrypoint.sh). Al ejecutar el comando anterior, el sistema realiza de forma automática las siguientes tareas:

Espera a que el motor PostgreSQL esté listo para recibir conexiones.

Ejecuta de forma interna las migraciones de la base de datos (migrate).

Recolecta todos los archivos estáticos e imágenes del proyecto (collectstatic) para que Nginx los sirva decorados.

👤 Crear el administrador del sistema (Único paso manual requerido)
Una vez que los contenedores estén completamente activos, el único comando manual que debes ejecutar para generar tu cuenta de acceso total al panel de administración es:

Bash
sudo docker exec -it django_app python manage.py createsuperuser
🔄 Comando de Migración Manual (En caso de emergencia)
Si en el futuro realizas cambios en los modelos de Django y necesitas forzar las migraciones manualmente sin reiniciar los contenedores, usa el contenedor correcto:

Bash
sudo docker exec -it django_app python manage.py migrate

# MiRenalApp es una plataforma web integral diseñada para facilitar la interacción entre profesionales de la salud y pacientes, enfocándose en la evaluación del riesgo nutricional y el fomento de una comunidad activa a través de un foro interactivo.

#🚀 Características Principales
#🏥 Sector Salud y Herramientas
Calculadora de IMC: Herramienta rápida para determinar el índice de masa corporal.

Test de Riesgo Nutricional: Evaluación dinámica basada en parámetros clínicos para detectar alertas preventivas.

Panel Médico: Área restringida para profesionales con herramientas de gestión específicas.

#💬 Foro Comunitario
Lectura Pública: Cualquier visitante puede leer las experiencias de la comunidad.

Interacción Protegida: Solo usuarios autenticados pueden publicar opiniones y calificar el servicio.

Sistema de Valoración: Calificación por estrellas y sistema de "Likes/Dislikes" para destacar contenido relevante.

Moderación Activa: Herramientas para administradores que permiten moderar comentarios y gestionar usuarios.

#👤 Gestión de Usuarios
Perfiles Personalizados: Cada usuario cuenta con un perfil donde puede subir su imagen y gestionar su información personal.
