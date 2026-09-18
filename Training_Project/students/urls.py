from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import (
    home,
    about,
    register_user,
    login_user,
    logout_user,
    dashboard,
    admin_dashboard,
    trainer_dashboard,
    student_dashboard,
    student_list,
    student_detail,
    add_student,
    edit_student,
    delete_student,
    trainer_update_student,
)


urlpatterns = [

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('register/', views.register_user, name='register'),

    path('login/', views.login_user, name='login'),
    
    path('logout/', views.logout_user, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('audit-logs/', views.audit_logs, name='audit_logs'),

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),

    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),

    # Student CRUD URLs
    path('students/', views.student_list, name='student_list'),

    # Trainer CRUD URLs

    path('trainers/', views.trainer_list, name='trainer_list'),

    path('trainers/<int:id>/', views.trainer_detail, name='trainer_detail'),

    path('trainers/add/', views.add_trainer, name='add_trainer'),

    path('trainers/<int:id>/edit/', views.edit_trainer, name='edit_trainer'),

    path('trainers/<int:id>/delete/', views.delete_trainer, name='delete_trainer'),

    path(
        'trainers/<int:id>/approve/',
        views.approve_trainer,
        name='approve_trainer'
    ),

    path(
        'trainers/<int:id>/toggle-status/',
        views.toggle_trainer_status,
        name='toggle_trainer_status'
    ),

    path('students/<int:id>/', views.student_detail, name='student_detail'),

    path('students/add/', views.add_student, name='add_student'),

    path('students/<int:id>/edit/', views.edit_student, name='edit_student'),

    path('students/<int:id>/delete/', views.delete_student, name='delete_student'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html',
            success_url='/dashboard/'
        ),
        name='password_change'
    ),

    path(
        'students/<int:id>/trainer-update/',
        trainer_update_student,
        name='trainer_update_student'
    ),

]