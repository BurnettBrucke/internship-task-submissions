
from django.urls import path # type: ignore

from  . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("about/",views.about,name='about'),
    path("student/",views.student_list,name='student_list'),
    path("student/add/",views.add_student,name='add_student'),
    path("update_student/<int:id>/",views.update_student,name='update_student'),
    path("delete_confirmation/<int:id>",views.delete_student,name='delete_student'),
    
    path('<int:id>/', views.single_student, name='single_student'),

    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    
    path('dashboard/',views.dashboard,name='dashboard')

]
