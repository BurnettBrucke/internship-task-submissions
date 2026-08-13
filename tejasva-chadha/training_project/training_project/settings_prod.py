"""
Production settings for training_project.
Extend base settings and enforce production security defaults.
"""
import os
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is required in production!")

ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()
]

# Security hardening settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False').lower() in ('true', '1')
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
