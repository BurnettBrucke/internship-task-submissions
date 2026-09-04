
from django.urls import path # type: ignore

from  . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("about/",views.about,name='about'),
    path("student/",views.student_list,name='student_list'),
    path("student/add/",views.add_student,name='add_student'),
]
