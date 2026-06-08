MiRenalApp (Kidnely Health) - Guía de Despliegue

Este proyecto utiliza Docker y Docker Compose para empaquetar y ejecutar tanto la aplicación web (Django) como el motor de base de datos (PostgreSQL 15) de forma centralizada en un único servidor.

🛠️ Requisitos Previos
Docker y Docker Compose instalados en el servidor de despliegue.

Tener creada la red de Docker compartida (si utilizas un contenedor proxy inverso externo como Nginx):

Bash
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
sudo docker-compose up -d --build
(Nota: Si tu sistema utiliza la versión moderna de Docker, puedes usar sudo docker compose up -d --build).

⚡ Tareas de Inicialización (Configuración de Django)
Una vez que los contenedores estén completamente activos (Up), ejecuta los comandos de control de Django dentro del contenedor de la aplicación web:

1. Correr migraciones de la base de datos
Crea las tablas correspondientes dentro de PostgreSQL ejecutando:

Bash
sudo docker exec -it mirenal_app python manage.py migrate
2. Recolectar archivos estáticos
Prepara el entorno para servir CSS, JavaScript e imágenes correctamente:

Bash
sudo docker exec -it mirenal_app python manage.py collectstatic --noinput
3. Crear el administrador del sistema
Genera la cuenta de superusuario para tener acceso total al panel de administración:

Bash
sudo docker exec -it mirenal_app python manage.py createsuperuser
🔍 Comandos Útiles de Monitoreo
Ver el estado de los servicios: sudo docker ps o sudo docker-compose ps

Ver los logs de la aplicación en tiempo real: sudo docker-compose logs -f web

Reiniciar el proyecto completo: sudo docker-compose restart

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
