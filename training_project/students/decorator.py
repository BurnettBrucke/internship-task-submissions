from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def role_required(*roles):
    
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            profile = getattr(request.user, "profile", None)

            if profile is None or profile.role not in roles:
                return HttpResponseForbidden(
                    "403 Forbidden: You do not have permission to access this page."
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
