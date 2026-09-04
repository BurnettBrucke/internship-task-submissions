from django.contrib import admin
from django.urls import path , include
from students import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , views.home ,name = "home"),
    path("about" , views.about , name = "about"),
    path("students", views.student_list , name = "students_list"),
    path("students/add/" , views.add_student ,name= "add_students")

]