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

Calificación mediante estrellas y sistema de Likes y Dislikes para destacar contenido relevante.

### Moderación Administrativa

Herramientas para la gestión de usuarios y moderación de contenido.

---

## 👤 Gestión de Usuarios

### Registro y Autenticación

Sistema de registro e inicio de sesión seguro.

### Perfiles Personalizados

Cada usuario dispone de un perfil donde puede gestionar su información personal y fotografía.

---

# 🛠️ Tecnologías Utilizadas

* Python 3.11
* Django 6.0
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

Editar el archivo `.env`.

Ejemplo:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=mirenalapp_db
DB_USER=postgres
DB_PASSWORD=change_me
DB_HOST=db
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

EMAIL_TIMEOUT=30

CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

SITE_NAME=Kidnely Health
```

---

## 4. Construir e iniciar los contenedores

Primer despliegue:

```bash
docker compose up --build
```

Segundo plano:

```bash
docker compose up -d --build
```

---

# ⚙️ Inicialización Automática

El proyecto incorpora un script `entrypoint.sh` que realiza automáticamente:

1. Esperar a que PostgreSQL esté disponible.
2. Ejecutar migraciones de Django.
3. Recolectar archivos estáticos.
4. Iniciar Gunicorn.

No es necesario ejecutar migraciones manualmente durante el primer despliegue.

---

# 👤 Crear Usuario Administrador

Una vez iniciado el sistema:

```bash
docker compose exec web python manage.py createsuperuser
```

Seguir las instrucciones para crear la cuenta administradora.

---

# 🔄 Migraciones Manuales

Si se realizan cambios en los modelos:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

---

# ✅ Verificar Estado del Sistema

Comprobar que Django no detecte errores:

```bash
docker compose exec web python manage.py check
```

Verificar migraciones:

```bash
docker compose exec web python manage.py showmigrations
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
├── .env.example
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

Ver logs:

```bash
docker compose logs -f
```

Detener:

```bash
docker compose down
```

Reiniciar:

```bash
docker compose restart
```

Reconstrucción completa:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

# 📦 Variables de Entorno

El archivo `.env` contiene secretos del proyecto y no debe subirse al repositorio.

Se incluye `.env.example` como plantilla.

Generar archivo local:

### Windows

```powershell
copy .env.example .env
```

### Linux

```bash
cp .env.example .env
```

---

# ❗ Solución de Problemas

## Error: password authentication failed for user

Si cambiaste credenciales después de crear el volumen:

```bash
docker compose down
docker volume rm mirenalapp_postgres_data
docker compose up --build
```

---

## Error: SECRET_KEY not found

Verificar que exista `.env` y tenga:

```env
SECRET_KEY=your-secret-key
```

---

## Error: nginx-proxy-network not found

Crear la red:

```bash
docker network create nginx-proxy-network
```

---

## Error: archivos estáticos no cargan

Ejecutar:

```bash
docker compose exec web python manage.py collectstatic --noinput
docker compose restart
```

---

# 🔒 Seguridad

* Nunca subir el archivo `.env`.
* Mantener `.env` incluido en `.gitignore`.
* Configurar `DEBUG=False` en producción.
* Utilizar una `SECRET_KEY` segura.
* Configurar correctamente `ALLOWED_HOSTS`.
* Configurar `CSRF_TRUSTED_ORIGINS`.
* Utilizar HTTPS en producción.

---

# 📄 Licencia

Proyecto académico desarrollado con fines educativos y de investigación.