from django.contrib import admin
from .models import Student, Department, StudentProfile, Course


admin.site.register(Student)
admin.site.register(Department)
admin.site.register(StudentProfile)
admin.site.register(Course)