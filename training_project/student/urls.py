from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Landing & Public
    path('',        views.landing, name='landing'),
    path('about/',  views.about,   name='about'),

    # Authentication
    path('register/',         views.register_view,         name='register'),
    path('register/trainer/', views.register_trainer_view, name='register_trainer'),
    path('login/',            views.login_view,            name='login'),
    path('admin-login/',      views.admin_login_view,      name='admin_login'),
    path('logout/',           views.logout_view,           name='logout'),

    # Password Management
    # /password-change/ — logged-in user changes own password
    path('password-change/', views.password_change_view, name='password_change'),

    # Django built-in password reset flow (4 URLs):
    # 1) User enters email → gets reset link printed to console (dev)
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
    ), name='password_reset'),

    # 2) "Email sent" confirmation page
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
    ), name='password_reset_done'),

    # 3) User clicks the emailed link → enters new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
    ), name='password_reset_confirm'),

    # 4) "Password reset complete" page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html',
    ), name='password_reset_complete'),

    # Student Portal
    path('student/',              views.student_portal,      name='student_portal'),
    path('student/edit-profile/', views.student_self_edit,   name='student_self_edit'),
    path('student/<int:pk>/',     views.student_detail_view, name='student_detail'),

    # Trainer Portal
    path('trainer/',                                          views.trainer_dashboard,     name='trainer_dashboard'),
    path('trainer/students/<int:pk>/marks/',                  views.trainer_marks_update,  name='trainer_marks_update'),
    path('trainer/students/<int:student_pk>/feedback/add/',   views.trainer_feedback_add,  name='trainer_feedback_add'),
    path('trainer/feedback/<int:pk>/edit/',                   views.trainer_feedback_edit, name='trainer_feedback_edit'),

    # Admin Portal
    path('admin-portal/', views.admin_dashboard, name='admin_dashboard'),

    # Admin: Student CRUD
    path('admin-portal/students/add/',                views.admin_student_add,    name='admin_student_add'),
    path('admin-portal/students/<int:pk>/edit/',      views.admin_student_edit,   name='admin_student_edit'),
    path('admin-portal/students/<int:pk>/delete/',    views.admin_student_delete, name='admin_student_delete'),
    path('admin-portal/students/<int:pk>/marks/',     views.admin_update_marks,   name='admin_update_marks'),

    # Admin: Department Management
    path('admin-portal/departments/',                  views.admin_department_list,   name='admin_department_list'),
    path('admin-portal/departments/add/',              views.admin_department_add,    name='admin_department_add'),
    path('admin-portal/departments/<int:pk>/edit/',    views.admin_department_edit,   name='admin_department_edit'),
    path('admin-portal/departments/<int:pk>/delete/',  views.admin_department_delete, name='admin_department_delete'),

    # Admin: Course Management
    path('admin-portal/courses/',                  views.admin_course_list,   name='admin_course_list'),
    path('admin-portal/courses/add/',              views.admin_course_add,    name='admin_course_add'),
    path('admin-portal/courses/<int:pk>/edit/',    views.admin_course_edit,   name='admin_course_edit'),
    path('admin-portal/courses/<int:pk>/delete/',  views.admin_course_delete, name='admin_course_delete'),

    # Admin: Audit Logs
    path('admin-portal/audit-logs/', views.admin_audit_log, name='admin_audit_log'),

    # Admin: User Account Management
    path('admin-portal/users/',                          views.admin_user_list,     name='admin_user_list'),
    path('admin-portal/users/<int:user_pk>/activate/',   views.admin_activate_user, name='admin_activate_user'),

    # Admin: Trainer Management
    path('admin-portal/trainers/',                    views.admin_trainer_list,   name='admin_trainer_list'),
    path('admin-portal/trainers/add/',                views.admin_trainer_add,    name='admin_trainer_add'),
    path('admin-portal/trainers/<int:pk>/edit/',      views.admin_trainer_edit,   name='admin_trainer_edit'),
    path('admin-portal/trainers/<int:pk>/delete/',    views.admin_trainer_delete, name='admin_trainer_delete'),
]