from django.urls import path

from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    # Student CRUD URLs
    path('students/', views.student_list, name='student_list'),

    path('students/<int:id>/', views.student_detail, name='student_detail'),

    path('students/add/', views.add_student, name='add_student'),

    path('students/<int:id>/edit/', views.edit_student, name='edit_student'),

    path('students/<int:id>/delete/', views.delete_student, name='delete_student'),

]