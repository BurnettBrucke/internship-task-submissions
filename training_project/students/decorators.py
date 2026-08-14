from functools import wraps

from django.core.exceptions import PermissionDenied

from .models import UserProfile


def role_required(*allowed_roles):
    """
    Allow access only to users having one
    of the specified roles.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                raise PermissionDenied

            if request.user.profile.role not in allowed_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator