from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/',views.change_password,name='change_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-feedback/',views.admin_feedback_list,name='admin_feedback_list'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/',views.student_detail,name='student_detail'),
    path('students/<int:pk>/edit/',views.edit_student,name='edit_student'),
    path('students/<int:pk>/delete/',views.delete_student,name='delete_student'),
    path('students/<int:pk>/marks-history/',views.marks_history,name='marks_history'),

    path('trainers/<int:trainer_id>/approve/',views.approve_trainer,name='approve_trainer'),
    path('trainers/',views.trainer_list,name='trainer_list'),
    path('trainers/add/',views.add_trainer,name='add_trainer'),
    path('trainers/<int:pk>/edit/',views.edit_trainer,name='edit_trainer'),
    path('trainers/<int:pk>/delete/',views.delete_trainer,name='delete_trainer'),
    path('trainer/students/',views.trainer_students,name='trainer_students'),

    path('courses/',views.course_list,name='course_list'),
    path('courses/add/',views.add_course,name='add_course'),
    path('courses/<int:pk>/edit/',views.edit_course,name='edit_course'),
    path('courses/<int:pk>/delete/',views.delete_course,name='delete_course'),

    path('students/<int:pk>/update-marks/',views.update_marks,name='update_marks'),
    path('students/<int:pk>/add-feedback/',views.add_feedback,name='add_feedback'),
    path('feedback/<int:pk>/edit/',views.edit_feedback,name='edit_feedback'),

    path('audit-logs/',views.audit_log_list,name='audit_log_list'),

   path('users/',views.user_list,name='user_list'),
   path('users/add/',views.add_user,name='add_user'),
   path('users/<int:pk>/edit/',views.edit_user,name='edit_user'),
   path('users/<int:pk>/delete/',views.delete_user,name='delete_user'),
   path('users/<int:user_id>/toggle-status/',views.toggle_user_status,name='toggle_user_status'),
   path('users/<int:pk>/unlock/',views.unlock_user,name='unlock_user'),


   path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'
    ),
    name='password_reset'
),

   path(
     'password-reset/done/',
      auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),
    name='password_reset_done'
    ),

   path(
     'reset/<uidb64>/<token>/',
      auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
    ),

   path(
      'reset/done/',
       auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),
    name='password_reset_complete'
    ),
]