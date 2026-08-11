from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post-login/', views.post_login_redirect, name='post_login_redirect'),

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),

    path('register/', views.register_view, name='register'),
    path('register/trainer/', views.trainer_register_view, name='trainer_register'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:pk>/marks/', views.update_marks, name='update_marks'),
    path('students/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
    path('feedback/<int:pk>/edit/', views.edit_feedback, name='edit_feedback'),

    path('admin-tools/users/', views.manage_users, name='manage_users'),
    path('admin-tools/users/<int:pk>/toggle-active/', views.toggle_user_active, name='toggle_user_active'),
    path('admin-tools/trainers/<int:pk>/approve/', views.approve_trainer, name='approve_trainer'),
    path('admin-tools/audit-log/', views.audit_log_view, name='audit_log'),
    path('admin-tools/reports/', views.reports_view, name='reports'),
]
