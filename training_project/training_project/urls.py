"""
URL configuration for training_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin # type: ignore
from django.urls import path,include
from django.shortcuts import render

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500(request):
    return render(request, "errors/500.html", status=500)


handler403 = "training_project.urls.custom_403"
handler404 = "training_project.urls.custom_404"
handler500 = "training_project.urls.custom_500"


urlpatterns = [

        path("admin/", admin.site.urls),
        path("",include("student.urls")),
       
]
