from django.contrib import admin
from django.urls import path , include
from students import views

admin.site.site_header = "Student Management Admin"
admin.site.site_title = "Student Management Admin portal"
admin.site.index_title = "Welcome to the admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , views.home ,name = "home"),
    path("about" , views.about , name = "about"),
    path("students", views.student_list , name = "students_list"),
    path("students/add/" , views.add_student ,name= "add_students"),
    path("students/<int:id>/" , views.student_detail , name = "student_detail"),#
    path("students/<int:id>/edit/" , views.edit_student , name = "edit_student"),
    path("students/<int:id>/delete/" , views.delete_student ,name = "delete_student" )
]