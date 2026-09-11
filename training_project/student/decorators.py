# from functools import wraps
# from django.http import HttpResponseForbidden
# from django.shortcuts import redirect

# def role_required(allowed_roles):

#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request,*args,**kwargs):
#             if not request.user.is_authenticated:
#                 return redirect('login')
#             profile=getattr(request.user,"userprofile",None)
#             if profile is None:
#                 return HttpResponseForbidden(
#                     "User Profile Not Found"
#                 )
#             if profile.role not in allowed_roles:
#                 return HttpResponseForbidden(
#                     "You do not have the permisson to access this !!"
#                 )

#             return view_func(request,*args,**kwargs)
#         return wrapper
#     return decorator

