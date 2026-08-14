from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path(
        "dashboard/admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "dashboard/trainer/",
        views.trainer_dashboard,
        name="trainer_dashboard"
    ),

    path(
        "dashboard/student/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    # Authentication
    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "users/",
        views.user_management,
        name="user_management",
    ),

    path(
        "users/<int:user_id>/toggle-status/",
        views.toggle_user_status,
        name="toggle_user_status",
    ),

# Feedback
path(
    "feedback/add/<int:student_id>/",
    views.add_feedback,
    name="add_feedback",
),

path(
    "feedback/<int:feedback_id>/edit/",
    views.edit_feedback,
    name="edit_feedback",
),

path(
    "feedback/",
    views.student_feedback,
    name="student_feedback",
),

path(
    "feedback/admin/",
    views.admin_feedback,
    name="admin_feedback",
),
# Marks

path(
    "marks/update/<int:student_id>/<int:course_id>/",
    views.update_marks,
    name="update_marks",
),

path(
    "marks/history/<int:student_id>/<int:course_id>/",
    views.marks_history,
    name="marks_history",
),

# Audit Logs

path(
    "audit-logs/",
    views.audit_log_list,
    name="audit_log_list",
),
path(
    "orm-challenges/",
    views.orm_challenges,
    name="orm_challenges",
),

    # Student CRUD
    path(
        "",
        views.student_list,
        name="student_list"
    ),

    path(
        "add/",
        views.add_student,
        name="add_student"
    ),

    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.edit_student,
        name="edit_student"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_student,
        name="delete_student"
    ),
]