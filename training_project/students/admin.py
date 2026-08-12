from django.contrib import admin
from .models import Student, Department, Course, StudentProfile, UserProfile
# Register your models here.
from .models import AuditLog
from .models import Feedback
from .models import MarksHistory

admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(StudentProfile)
admin.site.register(UserProfile)
admin.site.register(AuditLog)
admin.site.register(Feedback)
admin.site.register(MarksHistory)