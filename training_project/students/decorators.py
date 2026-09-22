from functools import wraps

from django.shortcuts import redirect, render
from .models import UserProfile


def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                profile = request.user.profile

            except UserProfile.DoesNotExist:
                return render(
                    request,
                    '403.html',
                    status=403
                )

            if profile.role not in allowed_roles:
                return render(
                    request,
                    '403.html',
                    status=403
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator