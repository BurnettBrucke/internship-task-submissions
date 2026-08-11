"""Connects Django's built-in auth signals to the audit log and the
failed-login lockout counter. Imported once from StudentsConfig.ready() so
the receivers are registered exactly once per process.
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import AuditLog, get_client_ip, log_action
from .security import register_failed_attempt


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    log_action(
        user,
        f"User '{user.username}' logged in.",
        action_type=AuditLog.ACTION_LOGIN,
        object_repr=f"User: {user.username}",
        request=request,
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    # `user` can be None if the session had already expired.
    username = user.username if user else 'unknown'
    log_action(
        user if user else username,
        f"User '{username}' logged out.",
        action_type=AuditLog.ACTION_LOGOUT,
        object_repr=f"User: {username}",
        request=request,
    )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request=None, **kwargs):
    username = credentials.get('username', 'unknown')
    attempts = register_failed_attempt(username)
    log_action(
        username,
        f"Failed login attempt #{attempts} for '{username}'.",
        action_type=AuditLog.ACTION_LOGIN_FAILED,
        object_repr=f"User: {username}",
        request=request,
    )
