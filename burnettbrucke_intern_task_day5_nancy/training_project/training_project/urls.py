"""
URL configuration for training_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from students.forms import (
    BootstrapPasswordChangeForm,
    BootstrapPasswordResetForm,
    BootstrapSetPasswordForm,
    LockoutAwareAuthenticationForm,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication ---
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=LockoutAwareAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- Password change (while logged in) ---
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            form_class=BootstrapPasswordChangeForm,
            success_url='/password-change/done/',
        ),
        name='password_change',
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change.html'),
        name='password_change_done',
    ),

    # --- Password reset (forgotten password) ---
    # URL shapes match the workbook exactly: /password-reset/,
    # /password-reset/done/, /reset/<uidb64>/<token>/, /reset/done/.
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            form_class=BootstrapPasswordResetForm,
            success_url='/password-reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            form_class=BootstrapSetPasswordForm,
            success_url='/reset/done/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),

    path('', include('students.urls')),
]

# Custom 403 page (wired to students.views.permission_denied_view). Django
# only uses this when DEBUG = False; during development the readable
# traceback page is shown instead, which is expected.
handler403 = 'students.views.permission_denied_view'
