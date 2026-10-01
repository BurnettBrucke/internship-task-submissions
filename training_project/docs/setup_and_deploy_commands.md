# Django Setup and Deployment Commands

## Setup

### 1. Navigate to the Project

```powershell
cd training_project
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

If `requirements.txt` does not exist:

```powershell
pip install django
```

### 5. Apply Database Migrations

```powershell
python manage.py migrate
```

### 6. Check the Project

```powershell
python manage.py check
```

### 7. Create Superuser

```powershell
python manage.py createsuperuser
```

### 8. Create Demo Data

```powershell
python manage.py seed_demo_data
```

### Demo Credentials

```text
Admin:
admin.demo@example.com
DemoAdmin123!

Trainer:
trainer1.demo@example.com
DemoTrainer123!

Student:
student01.demo@example.com
DemoStudent123!
```

### Reset Demo Data

Deletes existing demo data and recreates it:

```powershell
python manage.py seed_demo_data --reset-demo --yes
```

### Delete Demo Data

Deletes only demo data:

```powershell
python manage.py seed_demo_data --delete-demo --yes
```

A database backup is created before destructive demo-data operations.

### 9. Run Development Server

```powershell
python manage.py runserver
```

Application:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# Deployment Settings

Before production deployment, update the following settings in `settings.py`.

## DEBUG

```python
DEBUG = False
```

Do not use `DEBUG = True` in production.

## SECRET_KEY

Do not hard-code the production secret key.

Use an environment variable:

```python
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
```

## ALLOWED_HOSTS

Configure the production domain or server IP:

```python
ALLOWED_HOSTS = [
    "your-domain.com",
    "www.your-domain.com",
]
```

For local testing:

```python
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
```

## Database

SQLite can be used for local development.

For production, configure a production database such as PostgreSQL.

## Static Files

Configure the static files directory:

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Then collect static files:

```powershell
python manage.py collectstatic
```

## Security Settings

For HTTPS production deployments, enable appropriate security settings:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

These should only be enabled when HTTPS is correctly configured.

---

# Deployment Checks

Run Django's deployment checks:

```powershell
python manage.py check --deploy
```

Fix all important warnings before deploying.

---

# Production Commands

## Install Production Dependencies

```powershell
pip install -r requirements.txt
```

## Apply Migrations

```powershell
python manage.py migrate
```

## Collect Static Files

```powershell
python manage.py collectstatic
```

## Deployment Check

```powershell
python manage.py check --deploy
```

---

# WSGI Deployment

The Django WSGI application is:

```text
training_project.wsgi:application
```

Using Gunicorn:

```bash
gunicorn training_project.wsgi:application
```

---

# ASGI Deployment

The Django ASGI application is:

```text
training_project.asgi:application
```

Using Uvicorn:

```bash
uvicorn training_project.asgi:application
```

---

# Important Production Rules

- Do not use Django's `runserver` in production.
- Set `DEBUG = False`.
- Use a secure production `SECRET_KEY`.
- Configure `ALLOWED_HOSTS`.
- Use HTTPS.
- Configure production static files.
- Use a production database.
- Keep passwords and secrets out of source control.
- Do not use demo credentials in production.
- Run `python manage.py check --deploy` before deployment.
- Run migrations before starting the production server.
- Run `collectstatic` before serving the application.
