from django.contrib import admin
from .models import Student, Department, Course, StudentProfile


admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(StudentProfile)

