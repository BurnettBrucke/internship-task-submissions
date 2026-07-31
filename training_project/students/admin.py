from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(TrainerCourse)
admin.site.register(AuditLog)