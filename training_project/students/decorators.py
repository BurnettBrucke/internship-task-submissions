from functools import wraps
from django.shortcuts import render


def role_required(role):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.is_authenticated:

                if request.user.profile.role == role:
                    return view_func(request, *args, **kwargs)

            return render(request, "403.html", status=403)

        return wrapper

    return decorator