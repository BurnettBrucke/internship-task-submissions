from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.views import redirect_to_login

def role_required(*roles):
    """
    Decorator for views that checks if the logged-in user has any of the specified roles.
    Raises PermissionDenied (resulting in a 403 Forbidden page) if they do not.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            
            # Superusers and staff users are automatically authorized
            if request.user.is_superuser or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            if not hasattr(request.user, 'profile') or request.user.profile.role not in roles:
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
