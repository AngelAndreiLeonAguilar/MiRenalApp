# MiRenalApp

MiRenalApp es una plataforma web integral desarrollada con Django y PostgreSQL, diseñada para facilitar la interacción entre profesionales de la salud y pacientes, enfocándose en la evaluación del riesgo nutricional y el fomento de una comunidad activa mediante un foro interactivo.

---

# 🚀 Características Principales

## 🏥 Sector Salud y Herramientas

### Calculadora de IMC

Herramienta rápida para determinar el Índice de Masa Corporal (IMC) del usuario.

### Test de Riesgo Nutricional

Evaluación dinámica basada en parámetros clínicos para detectar alertas preventivas relacionadas con el estado nutricional.

### Panel Médico

Área restringida para profesionales de la salud con herramientas específicas de gestión y seguimiento.

---

## 💬 Foro Comunitario

### Lectura Pública

Cualquier visitante puede consultar las experiencias compartidas por la comunidad.

### Interacción Protegida

Solo usuarios autenticados pueden publicar opiniones, comentar y participar activamente.

### Sistema de Valoración

Calificación mediante estrellas y sistema de "Likes" y "Dislikes" para destacar contenido relevante.

### Moderación Administrativa

Herramientas para la gestión de usuarios y moderación de contenido.

---

## 👤 Gestión de Usuarios

### Registro y Autenticación

Sistema de registro e inicio de sesión seguro.

### Perfiles Personalizados

Cada usuario dispone de un perfil donde puede gestionar su información personal y fotografía.

# 🛠️ Tecnologías Utilizadas

* Python 3.11
* Django 5.x
* PostgreSQL 15
* Docker
* Docker Compose
* Nginx
* Gunicorn

---

# 📋 Requisitos Previos

Antes de comenzar asegúrese de tener instalado:

* Git
* Docker Desktop
* Docker Compose

Verificar instalación:

```bash
docker --version
docker compose version
git --version
```

---

# 📥 Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd MiRenalApp
```

---

## 2. Crear archivo de configuración

### Windows

```powershell
copy .env.example .env
notepad .env
```

### Linux

```bash
cp .env.example .env
nano .env
```

---

## 3. Configurar variables de entorno

Editar el archivo `.env` y ajustar los valores según el entorno.

Ejemplo:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=mirenalapp_db
DB_USER=manuel
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

---

## 4. Construir e iniciar los contenedores

```bash
docker compose up --build
```

O en segundo plano:

```bash
docker compose up -d --build
```

---

# ⚙️ Inicialización Automática

El proyecto incorpora un script de inicio (`entrypoint.sh`) que realiza automáticamente:

1. Esperar a que PostgreSQL esté disponible.
2. Ejecutar migraciones de Django.
3. Recolectar archivos estáticos.
4. Iniciar Gunicorn.

No es necesario ejecutar migraciones manualmente durante el primer despliegue.

---

# 👤 Crear Usuario Administrador

Una vez iniciado el sistema:

```bash
docker exec -it django_app python manage.py createsuperuser
```

Seguir las instrucciones para crear la cuenta administradora.

---

# 🔄 Migraciones Manuales

Si se realizan cambios en los modelos:

```bash
docker exec -it django_app python manage.py makemigrations
docker exec -it django_app python manage.py migrate
```

---

# 🌐 Acceso al Sistema

Aplicación principal:

```text
http://localhost:8000
```

Panel administrativo:

```text
http://localhost:8000/admin
```

---

# 📁 Estructura del Proyecto

```text
MiRenalApp/
│
├── apps/
│   ├── blog/
│   ├── citas/
│   ├── pacientes/
│   └── usuarios/
│
├── MiRenalApp/
├── templates/
├── media/
├── staticfiles/
│
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── entrypoint.sh
├── requirements.txt
├── manage.py
└── README.md
```

---

# 🐳 Administración de Docker

Ver contenedores:

```bash
docker ps
```

Detener contenedores:

```bash
docker compose down
```

Reiniciar:

```bash
docker compose restart
```

Reconstruir completamente:

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

---

# ❗ Solución de Problemas

## Error: password authentication failed for user

Si se modificaron las credenciales de PostgreSQL después de haber creado el volumen:

```bash
docker compose down
docker volume rm mirenalapp_postgres_data
docker compose up --build
```

Esto recreará la base de datos utilizando las credenciales actuales definidas en `.env`.

---

## Error: SECRET_KEY not found

Verificar que exista el archivo `.env` y contenga:

```env
SECRET_KEY=your-secret-key
```

---

## Error: nginx-proxy-network not found

Crear la red manualmente:

```bash
docker network create nginx-proxy-network
```

---

# 🔒 Seguridad

* Nunca subir el archivo `.env` al repositorio.
* Mantener `.env` incluido en `.gitignore`.
* Utilizar contraseñas seguras en producción.
* Configurar `DEBUG=False` en producción.
* Configurar correctamente `ALLOWED_HOSTS`.
* Utilizar HTTPS en ambientes productivos.

---

# 📄 Licencia

Proyecto académico desarrollado con fines educativos y de investigación.
