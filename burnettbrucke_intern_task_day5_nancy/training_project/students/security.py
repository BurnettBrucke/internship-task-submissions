"""Cache-based failed-login tracking and temporary account lockout.

Design (and its limitations) are documented in README.md under
"Login protection - known limitations". Short version: this uses Django's
cache framework as the fast/live counter (cleared on process restart with
the default LocMemCache backend -- a real deployment should use Redis or
memcached so the lockout survives restarts and is shared across workers),
and separately writes every attempt to the AuditLog model (students.models)
so the history is never lost even though the live counter can reset.
"""
from django.core.cache import cache

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 15 * 60  # 15 minutes
ATTEMPT_WINDOW_SECONDS = 15 * 60  # failed attempts older than this stop counting


def _attempts_key(username):
    return f"login_attempts:{username.lower()}"


def _lockout_key(username):
    return f"login_locked:{username.lower()}"


def is_locked_out(username):
    if not username:
        return False
    return cache.get(_lockout_key(username)) is not None


def register_failed_attempt(username):
    """Call after an authentication failure. Returns the new attempt count
    and locks the account once MAX_ATTEMPTS is reached."""
    if not username:
        return 0
    key = _attempts_key(username)
    attempts = cache.get(key, 0) + 1
    cache.set(key, attempts, ATTEMPT_WINDOW_SECONDS)
    if attempts >= MAX_ATTEMPTS:
        cache.set(_lockout_key(username), True, LOCKOUT_SECONDS)
    return attempts


def reset_attempts(username):
    """Call after a successful login."""
    if not username:
        return
    cache.delete(_attempts_key(username))
    cache.delete(_lockout_key(username))
