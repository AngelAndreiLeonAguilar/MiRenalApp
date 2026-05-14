MiRenalApp - Guía de Despliegue
Este proyecto utiliza Docker para facilitar su ejecución.

Requisitos
Docker y Docker Compose instalados.

Pasos para ejecutar:
Clonar el repositorio.

Crear un archivo .env basado en .env.example.

Ejecutar: docker-compose up -d --build.

Correr migraciones: docker exec -it mirenal_app python manage.py migrate.

Recolectar archivos estáticos: docker exec -it mirenal_app python manage.py collectstatic --noinput.

Crear el administrador: docker exec -it mirenal_app python manage.py createsuperuser.

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

Seguridad: Sistema robusto de autenticación, recuperación de contraseña por correo electrónico y endurecimiento de servidor (Fail2Ban, UFW).
