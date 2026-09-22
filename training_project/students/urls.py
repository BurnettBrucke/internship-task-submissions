from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,  reverse_lazy
from students import views

admin.site.site_header = "Student Management Admin"
admin.site.site_title = "Student Management Admin portal"
admin.site.index_title = "Welcome to the admin"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("students", views.student_list, name="students_list"),

    path("students/add/", views.add_student, name="add_students"),
    path("students/<int:id>/", views.student_detail, name="student_detail"),
    path("students/<int:id>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:id>/delete/", views.delete_student, name="delete_student"),

    path("trainer/register/", views.trainer_register, name="trainer_register"),
    path("login/", views.login_backend, name="login"),
    path("logout/", views.logout_backend, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("trainer/dashboard/", views.trainer_dashboard, name="trainer_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    path("students/set-password/<uidb64>/<token>/", views.set_student_password, name="set_student_password"),

    path("trainers/<int:id>/approve/", views.approve_trainer, name="approve_trainer"),
    path("trainers/<int:id>/reject/", views.reject_trainer, name="reject_trainer"),

    path("trainer/enrollment/<int:id>/marks/", views.update_marks, name="update_marks"),
    path("trainer/enrollment/<int:id>/edit", views.create_feedback, name="create_feedback"),
    path("trainer/feedback/<int:id>/edit/", views.edit_feedback, name="edit_feedback"),

    path("student/profile/edit/", views.edit_student_profile, name="edit_student_profile"),
    path("courses/add/", views.add_course, name="add_course"),

    path("courses/<int:id>/edit/", views.edit_course, name="edit_course"),
    path("courses/<int:id>/toggle/", views.toggle_course_status, name="toggle_course_status"),

    # Change Password

    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html",
        success_url=reverse_lazy("password_change_done"),
    ), name="password_change"),

    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="registration/password_change_done.html",
    ), name="password_change_done"),

    # Password Reset

    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.txt",
        subject_template_name="registration/password_reset_subject.txt",
        success_url=reverse_lazy("password_reset_done"),
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html",
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete"),
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),

    path("users/<int:id>/activate/", views.activate_user, name="activate_user"),
    path("users/<int:id>/deactivate/", views.deactivate_user, name="deactivate_user"),

    path("audit-logs/", views.audit_logs, name="audit_logs"),

    path("trainers/<int:id>/", views.trainer_detail, name="trainer_detail"),
    path("trainers/<int:id>/assign-course/", views.assign_trainer_course, name="assign_trainer_course"),
    path("trainers/<int:id>/delete/", views.delete_trainer, name="delete_trainer"),
]