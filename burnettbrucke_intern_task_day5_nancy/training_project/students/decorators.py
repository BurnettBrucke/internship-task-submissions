"""Reusable permission helpers for role-based access control.

Using a decorator (rather than only hiding buttons in templates) means
unauthorized requests are rejected in the view layer itself -- someone
typing a URL directly, or replaying a form POST, is blocked just as much
as someone clicking a hidden link would have been.
"""
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Restrict a view to users whose UserProfile.role is in `roles`.

    Usage:
        @role_required('admin')
        def some_admin_only_view(request):
            ...

        @role_required('admin', 'trainer')
        def some_shared_view(request):
            ...

    Unauthenticated users are sent to the login page (like @login_required).
    Authenticated users with the wrong role get an HTTP 403.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            profile = getattr(request.user, 'profile', None)
            if profile is None or profile.role not in roles:
                raise PermissionDenied("You do not have permission to view this page.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def get_role(user):
    """Safe helper: returns the role string, or None if no profile/anonymous."""
    if not getattr(user, 'is_authenticated', False):
        return None
    profile = getattr(user, 'profile', None)
    return profile.role if profile else None
