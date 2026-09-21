
from django.urls import path # type: ignore

from  . import views
from django.contrib.auth import views as auth_views
from .views import (
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    audit_log_list,
    custom_login,
    custom_logout,
    trainer_list,
    approve_trainer,
    activate_account,
    deactivate_account,
)

urlpatterns = [
    path("",views.home,name="home"),

    # Authentication
    path("login/",custom_login,name="login"),
    path("logout/",custom_logout,name="logout"),
    path("register/",views.register_view,name="register"),

    # Password Change
    path("password-change/",CustomPasswordChangeView.as_view(
        template_name="registration/password_change.html"),name="password_change",),
    path("password-change/done/",CustomPasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),name="password_change_done",),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html",email_template_name="registration/password_reset_email.html",success_url="/password-reset/done/"),name="password_reset",),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",success_url="/reset/done/"),name="password_reset_confirm",),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),

    # Dashboards
    path("dashboard/admin/",views.admin_dashboard,name="admin_dashboard"),
    path("dashboard/trainer/",views.trainer_dashboard,name="trainer_dashboard"),
    path("dashboard/student/",views.student_dashboard,name="student_dashboard"),


    # Student
    path("students/",views.student_list,name="student_list"),
    path("students/add/",views.student_create,name="student_create"),
    path("students/<int:pk>/",views.student_detail,name="student_detail"),
    path("students/<int:pk>/edit/",views.student_update,name="student_edit"),
    path("students/<int:pk>/delete/",views.student_delete,name="student_delete"),


    # courses
    path("courses/<int:pk>/assign-trainer/",views.assign_trainer,name="assign_trainer"),


    # Admin
    path("audit-logs/",audit_log_list, name="audit_log_list"),
    path("trainers/",trainer_list,name="trainer_list"),
    path("accounts/<int:user_id>/activate/",activate_account,name="activate_account"),
    path("accounts/<int:user_id>/deactivate/",deactivate_account,name="deactivate_account"),



    
    #  account information when created and last used
    path("account-information/",views.account_information,name="account_information"),
    
    # trainer
    path(
        "trainers/<int:user_id>/approve/",
        approve_trainer,
        name="approve_trainer"
    ),

    # marks
    path(
        "courses/<int:course_id>/students/<int:student_id>/marks/update/",
        views.update_course_marks,
        name="update_course_marks",
        ),

    path(
        "courses/<int:course_id>/students/<int:student_id>/marks/history/",
        views.marks_history,
        name="marks_history",
      ),


    # feedback
    path(
        "courses/<int:course_id>/students/<int:student_id>/feedback/add/",
        views.feedback_create,
        name="feedback_create",
        ),

    path(
        "feedback/<int:feedback_id>/edit/",
        views.feedback_edit,
        name="feedback_edit",
      ),

    path(
        "feedback/",
        views.feedback_list,
        name="feedback_list",
      ),


    # 




                

    ]


