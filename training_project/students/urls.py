
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('about/', views.about),
    
    path("", views.dashboard, name="dashboard"),

    path("students/", views.student_list, name="student_list"),

    path("students/<int:id>/", views.student_detail, name="student_detail"),

    path("students/add/", views.student_add, name="student_add"),

    path("students/<int:id>/edit/", views.student_edit, name="student_edit"),

    path("students/<int:id>/delete/", views.student_delete, name="student_delete"),

    path("register/",views.register,name="register"),

    path("login/",views.user_login,name="login"),

    path("logout/",views.user_logout,name="logout"),
]