from functools import wraps
from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request,*args, **kwargs):
            if request.user.profile.role==role:
                return view_func(request,*args,**kwargs)
            return HttpResponseForbidden('403 forbidden')
        return wrapper
    return decorator
            