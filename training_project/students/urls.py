from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import CustomPasswordChangeView


urlpatterns = [

    # =========================
    # Dashboard
    # =========================
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # =========================
    # Students
    # =========================
    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/<int:id>/",
        views.student_detail,
        name="student_detail"
    ),

    path(
        "students/<int:id>/edit/",
        views.edit_student,
        name="edit_student"
    ),

    path(
        "students/<int:id>/delete/",
        views.delete_student,
        name="delete_student"
    ),

    # =========================
    # Authentication
    # =========================
    path(
        "register/",
        views.register_user,
        name="register"
    ),

    path(
        "login/",
        views.login_user,
        name="login"
    ),

    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),

    # =========================
    # Role Dashboards
    # =========================
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "trainer-dashboard/",
        views.trainer_dashboard,
        name="trainer_dashboard"
    ),

    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    # =========================
    # Password Change
    # =========================
    path(
        "password-change/",
        CustomPasswordChangeView.as_view(),
        name="password_change"
    ),

    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done"
    ),

    # =========================
    # Password Reset
    # =========================
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    # =========================
    # Feedback
    # =========================
    path(
        "feedback/add/",
        views.add_feedback,
        name="add_feedback"
    ),

    path(
        "feedback/",
        views.feedback_list,
        name="feedback_list"
    ),

    path(
        "feedback/<int:id>/edit/",
        views.edit_feedback,
        name="edit_feedback"
    ),

    # =========================
    # Marks
    # =========================
    path(
        "students/<int:id>/update-marks/",
        views.update_marks,
        name="update_marks"
    ),

    path(
        "students/<int:id>/marks-history/",
        views.marks_history,
        name="marks_history"
    ),

    # =========================
    # Audit Logs
    # =========================
    path(
        "audit_log_list/",
        views.audit_log_list,
        name="audit_log_list"
    ),
]