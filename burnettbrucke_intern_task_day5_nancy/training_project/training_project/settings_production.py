"""
Production settings EXAMPLE for training_project.

This file is NOT wired up as the active settings module by default --
`manage.py` and `wsgi.py`/`asgi.py` still point at `training_project.settings`
(the development settings) unless you explicitly point DJANGO_SETTINGS_MODULE
at this file instead:

    export DJANGO_SETTINGS_MODULE=training_project.settings_production

It exists to demonstrate the specific changes a real deployment needs on top
of the development settings -- it is NOT a complete, drop-in production
config (there's no real database, cache, or email backend wired in below;
you'd point DATABASE_URL/REDIS_URL/etc. at your actual infrastructure).

Everything not overridden here is inherited unchanged from settings.py.
"""
import os

from .settings import *  # noqa: F401,F403 -- inherit the base config, override below

# ---------------------------------------------------------------------------
# Secrets and debug flag -- NEVER hardcode these in a committed file.
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]  # raises KeyError loudly if missing -- better than silently insecure
DEBUG = False

# Comma-separated in the environment, e.g. "example.com,www.example.com"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

# ---------------------------------------------------------------------------
# Database -- read connection info from the environment instead of hardcoding
# sqlite. Example assumes PostgreSQL; adjust ENGINE/params for your database.
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DJANGO_DB_NAME", "training_project"),
        "USER": os.environ.get("DJANGO_DB_USER", "training_project"),
        "PASSWORD": os.environ["DJANGO_DB_PASSWORD"],
        "HOST": os.environ.get("DJANGO_DB_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DB_PORT", "5432"),
    }
}

# ---------------------------------------------------------------------------
# Cookies / sessions -- now safe (and required) to lock down, because a real
# deployment is expected to be served over HTTPS. See settings.py for the
# explanation of why these stay False in local development.
# ---------------------------------------------------------------------------
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days; raise once confident HTTPS is stable
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# If running behind a reverse proxy / load balancer that terminates TLS and
# forwards over plain HTTP internally, Django needs to know which header to
# trust to determine the original request was HTTPS:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------------------------------
# Static files -- collected once at deploy time (see `collectstatic` in the
# release checklist below) and served by whitenoise/nginx/a CDN, not by
# Django's dev server.
# ---------------------------------------------------------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"

# ---------------------------------------------------------------------------
# Cache -- swap the default in-memory cache for something shared across
# worker processes. This matters specifically for students/security.py's
# login-lockout counter (see README "Login protection - known limitations")
# -- LocMemCache is per-process, so a real deployment with multiple gunicorn
# workers needs a shared backend like Redis for the lockout to actually work
# across all of them.
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/1"),
    }
}

# ---------------------------------------------------------------------------
# Email -- replace the console backend with a real provider.
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

# ---------------------------------------------------------------------------
# Logging -- surface errors somewhere durable instead of only stdout.
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
