from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

from .models import UserProfile


def role_required(*allowed_roles):
    """
    Allow access only to users whose UserProfile role
    matches one of the supplied roles.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # User is not logged in
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            # User has no UserProfile
            profile = getattr(request.user, "profile", None)

            if profile is None:
                return HttpResponseForbidden(
                    "Your account does not have a valid role."
                )

            # User's role is not allowed
            if profile.role not in allowed_roles:
                return HttpResponseForbidden(
                    "You are not authorized to access this page."
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator