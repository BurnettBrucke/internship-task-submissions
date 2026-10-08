from .settings import *
import os


DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is required in production."
    )

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / "staticfiles"